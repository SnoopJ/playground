import sys

from setuptools import setup, find_packages


def determine_package_data():
    package_data = {}
    if sys.platform.startswith("linux"):
        package_data["mypkg"] = ["linux/*.dat"]
    elif sys.platform == "win32":
        package_data["mypkg"] = ["win32/*.dat"]
    else:
        raise ValueError(f"Unsupported platform: {os.platform!r}")

    return package_data


setup(
    packages=find_packages("mymodule"),
    package_dir={"": "mymodule"},
    package_data=determine_package_data(),
)
