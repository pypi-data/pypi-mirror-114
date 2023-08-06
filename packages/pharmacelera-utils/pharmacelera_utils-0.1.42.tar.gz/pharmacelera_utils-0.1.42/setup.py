from setuptools import setup, find_packages

setup(
    name="pharmacelera_utils",
    version="0.1.42",
    description="Utility functions to execute pharmacelera scripts",
    url="https://bitbucket.org/pharmacelera/pharmqsar-examples.git",
    author="Pharmacelera developers",
    author_email="support@pharmacelera.com",
    license="Mozilla Public License Version 2.0",
    packages=find_packages(where="src"),
    install_requires=["requests==2.25.1", "PyYAML==5.4.1", "boto3==1.17.76", "botocore==1.20.112"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    py_modules=[
        "launch",
        "services",
        "utils",
        "errors",
        "commands",
        "__init__",
    ],
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "pharmacelera-launch=pharmacelera_utils.launch:run",
            "pharmacelera-cmd=pharmacelera_utils.commands:run",
        ]
    },
)