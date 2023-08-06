#!/usr/bin/env python

import sys
import argparse
from typing import List
from pathlib import Path
from .utils import Colors
from .services import Calls


class ArgumentParser:
    def __init__(self) -> None:
        self.init_arguments()

    def init_arguments(self):
        """Define cmd input arguments."""
        parser = argparse.ArgumentParser("")
        parser.add_argument(
            "--option",
            help="Type of the command to call Pharmacelera endpoint. Possible options: get, list, download, kill, remove. Default: get. Note: list option supports filter by status, eg: list?status=running.",
            type=str,
            default="get",
        )
        parser.add_argument("--id", help="Unique id of the experiment", type=str)
        parser.add_argument(
            "--uri", help="Host name of the endpoint. Default: http://localhost", type=str, default="http://localhost"
        )
        parser.add_argument("--port", help="endpoint port number. Default: 8080", type=str, default="8080")
        self.args = parser.parse_args()


class AppConfiguration:
    client: Calls
    args: argparse.Namespace
    path: str = Path().absolute()
    printables: List = ["id", "msg", "status", "progress", "end_date", "experiment_type", "folder"]

    def __init__(self, args) -> None:
        params = {"PORT": args.port, "URI": args.uri}
        self.client = Calls(params)
        self.args = args

    def get(self):
        id = self.args.id
        response = self.client.get(id)
        if not response:
            return
        if response.get("statusCode", None) == 200:
            body = response.get("body")
            self.print([body])
            return body
        else:
            print(f"{Colors.FAIL}No experiment found with the given id.{Colors.ENDC}")
        return None

    def list(self, query_param):
        print(f"{Colors.BOLD}Listing experiments ...{Colors.ENDC}")
        response = self.client.list(query_param)
        if not response:
            return
        body = response.get("body", None)
        if len(body):
            self.print(body)
        else:
            print(f"{Colors.FAIL}No experiment found.{Colors.ENDC}")

    def download(self):
        print(f"{Colors.BOLD}Starts downloading ...{Colors.ENDC}")
        experiment = self.get()
        if not experiment:
            return
        if experiment.get("status") not in ("finished", "stopped", "error"):
            print(f"{Colors.FAIL}Experiment is still running{Colors.ENDC}")
            return
        folder = experiment.get("folder").split("/")[-1]
        id = self.args.id
        self.client.download(id, folder, self.path, outputs="")
        print(f"{Colors.BOLD}Download finished.{Colors.ENDC}")

    def kill(self):
        print(f"{Colors.BOLD}Killing experiment ...{Colors.ENDC}")
        id = self.args.id
        experiment = self.get()
        if not experiment:
            return
        self.client.kill(id)
        print(f"Done.")

    def remove(self):
        print(f"{Colors.BOLD}Removing experiment ...{Colors.ENDC}")
        id = self.args.id
        experiment = self.get()
        if not experiment:
            return
        self.client.remove(id)
        print(f"Done.")

    def print(self, experiment_lists):
        for index, experiment in enumerate(experiment_lists):
            print(f"{Colors.OKBLUE}Count: {index + 1}{Colors.ENDC}")
            print(120 * "-")
            single_list_experiment = list(experiment.items())
            single_list_experiment.sort(key=self.get_length)
            sorted_single_experiment = {str(elem[0]): str(elem[1]) for elem in single_list_experiment}
            colon_distance = str(len(list(sorted_single_experiment)[-1]))
            row_format = "{:<" + colon_distance + "} : {:<30}"
            for key, value in sorted_single_experiment.items():
                if key in self.printables:
                    print(f"{Colors.OKGREEN}{row_format.format(key, value)}{Colors.ENDC}")
            print(120 * "-" + "\n")

    def get_length(self, key):
        return len(key[0])

    def redirect(self, option: str):
        option = option.split("?")
        query_param = option[1] if len(option) > 1 else None
        if option[0] == "get":
            return self.get()
        elif option[0] == "list":
            return self.list(query_param)
        elif option[0] == "download":
            return self.download()
        elif option[0] == "kill":
            return self.kill()
        elif option[0] == "remove":
            return self.remove()
        else:
            print("Option value is unknown.")


def run():
    parser = ArgumentParser()
    app = AppConfiguration(parser.args)
    if len(sys.argv) > 1:
        app.redirect(app.args.option)
    else:
        print("No argument parameter is present. Please, use --help to get more information")