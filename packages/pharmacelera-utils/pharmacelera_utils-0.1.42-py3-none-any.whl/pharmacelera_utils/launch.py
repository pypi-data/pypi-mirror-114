#!/usr/bin/env python

import os
import sys
import time
import yaml
import time
import uuid
import boto3
import shutil
import logging
import zipfile
from pathlib import Path
from .utils import Colors, Utils
from .errors import Errors
from .services import Calls

#
# Copyright (c) 2021 Pharmacelera S.L.
# All rights reserved.
#
# Description: Script to launch multiple PharmQSAR experiments and select the best model
#
# Usage: Define the desired experiments in the config.yaml file and run this script
#


class Configs:
    """Read pharmQSAR config file, and parse Yaml configs"""

    path: str = Path().absolute()

    def __init__(self) -> None:
        self.error = Errors()

    def get_from_s3(self, statics):
        """Download selected model from S3.

        Args:
            config (dict): Experiment configuration from yaml
        """
        s3 = boto3.resource("s3")
        filename = statics.get("FILENAME", None)
        if not filename:
            self.error.fileNameException()
        s3_bucket = statics.get("S3_BUCKET", None)
        if not s3_bucket:
            self.error.bucketNameException()
        s3_folder = statics.get("S3_FOLDER", None)
        if not s3_folder:
            self.error.S3FolderPathException()
        zip_path = os.path.join(self.path, "inputs")
        try:
            s3.Bucket(s3_bucket).download_file(s3_folder + "/" + filename, os.path.join(zip_path, "tmp.zip"))
            folder, _, filenames = next(os.walk(zip_path))
            for f in filenames:
                if f.endswith(".zip"):
                    with zipfile.ZipFile(os.path.join(folder, f)) as zipped:
                        zipped.extractall(zip_path)
            shutil.move(os.path.join(zip_path, "custom.yaml"), os.path.join(self.path, "custom.yaml"))
            os.remove(os.path.join(zip_path, "tmp.zip"))
            logging.info("Downloaded files and config.")
            return True
        except Exception as exp:
            self.error.S3Exception(exp)
            return False

    def read(self, configFile):
        """Read and parse file."""
        try:
            with open(configFile, "r") as s:
                return yaml.safe_load(s)
        except Exception as exp:
            logging.error(exp)
        return None

    def custom_config(self):
        """Read and parse file."""
        try:
            with open("custom.yaml", "r") as s:
                return yaml.safe_load(s)
        except Exception as exp:
            logging.error(exp)
        return None

    def s3_config(self, statics):
        """Replace input molecule name of experiment1.
        Args:
            dict: default config.yaml configuration of Case4
        """
        config = self.custom_config()
        input_name = statics.get("EXP_1_INPUT", None)
        if not input_name:
            self.error.inputFileNameException()
        config["experiment1"]["files"]["input"] = input_name
        return config


class Initialize:
    """Define params."""

    utils: Utils = None
    client: Calls = None
    path: str = Path().absolute()

    def __init__(self, config):
        self.utils = Utils()
        self.error = Errors()
        self._set_params(config)
        self.client = Calls(config)

    def _set_params(self, config):
        # define which binary will be executing
        self.__endpoint = config.pop("endpoint")

        # set all input files
        files = config.pop("files")
        try:
            self.__files = {key: open(os.path.join(self.path, value), "rb") for (key, value) in files.items()}
        except Exception:
            self.error.inputFilesException(files)
        self.__parameters = config

    def launch(self):
        """Call launch API endpoint with defined parameters
        to start the experiment.
        """
        response = self.client.launch(self.__endpoint, self.__parameters, self.__files)
        if response:
            if response["statusCode"] == 200:
                exp = response["body"]
                if exp.get("env", None) != "batch":
                    logging.info(f"{exp['msg']}")
                    if exp["msg"].startswith("there is"):
                        logging.info(f"Pending/Running experiments: {exp['pendingExperimentIds']}")
                return self.exp_getter(exp["id"])
            else:
                logging.error(f"{Colors.FAIL}Experiment failed, {response.get('body')}{Colors.ENDC}")
        else:
            logging.error("Experiment could not start")
        for _, open_file in self.__files.items():
            open_file.close()
        return False

    def exp_getter(self, id):
        """Watch status and progress of the experiment and
        download files when it is done.
        """
        logging.info(f"experiment id: {id}")
        status = "pending"
        progress = "0%"
        while True:
            if status != "finished" and status != "error":
                response = self.client.get(id)
                id = response["body"]["id"]
                env = response["body"].get("env", "unknown")
                status = response["body"]["status"]
                command = response["body"].get("command", None)
                folder = self.utils.get_name(command)
                if status == "running":
                    if progress != response["body"]["progress"]:
                        progress = response["body"]["progress"]
                        logging.info(f"{Colors.OKBLUE}Status: {status}, Progress: {progress}{Colors.ENDC}")
                elif status == "pending":
                    logging.info(f"Status: {status}, experiment id: {id}, running environment: {env}")
                elif status == "finished":
                    logging.info(f"{Colors.OKGREEN}{Colors.UNDERLINE}Experiment finished!{Colors.ENDC}")
                elif status == "error" or status == "stopped":
                    logging.error(f"{Colors.FAIL}Experiment finished with Error.")
                    logging.error(f"{response['body'].get('msg', 'unknown')}{Colors.ENDC}")
                    # download experiment
                    self.client.download(id, folder, self.path)
                    logging.info(f"Experiment id: {id} downloaded in outputs folder as ZIP")
                    return False
                time.sleep(5)
            else:
                # download experiment
                self.client.download(id, folder, self.path)
                logging.info(f"Experiment with id: {id} downloaded in outputs folder as ZIP")
                return True

    def clear(self):
        try:
            shutil.rmtree(os.path.join(self.path, "tmp"))
            os.remove(os.path.join(self.path, "custom.yaml"))
        except Exception:
            pass


def run():
    logging.basicConfig(level=logging.INFO)
    reader = Configs()
    args = sys.argv
    if len(args) < 2:
        print("Please define yaml configuration file")
        sys.exit(0)
    config = reader.read(args[1])
    start = time.time()
    if config:
        statics = config.pop("static")
        get_conf = statics.get("GET_CONF_FROM_S3", None)
        if get_conf:
            if not reader.get_from_s3(statics):
                sys.exit()
            config = reader.s3_config(statics)
        statics["MODEL_NAME"] = f'{uuid.uuid4().hex}_{statics.get("MODEL_NAME", "")}'
        for k, v in config.items():
            # Run each experiment synchronously from configuration
            logging.info(f" - - - - Starting experiment with {k} params - - - -")
            statics["jobName"] = v["name"]
            params = {**statics, **v}
            init = Initialize(params)
            result = init.launch()
            if not result and not get_conf:
                sys.exit(0)

        if statics.get("UPLOAD_S3", None):
            # select best model
            init.utils.best_model_selector(init.path, statics, config)
        # clear input and out folders from API container
        init.client.clearFiles()
        # clear temporary files
        init.clear()
        logging.info("done")
    else:
        logging.error("Could not load experiments from config")
    print(f"total elapsed time: {time.time() - start:.5f}")