import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from textwrap import indent

import requests

ANSI_BOLD = "\x1b[1m"
ANSI_RED = "\x1b[31m"
ANSI_GREEN = "\x1b[32m"
ANSI_YELLOW = "\x1b[33m"
ANSI_RESET = "\x1b[0m"


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("files", nargs="+")


def info(msg: str, additional="") -> None:
    print(f"{ANSI_GREEN}{msg}{ANSI_RESET}")
    if additional:
        addtxt = indent(additional, prefix=" >  ")
        print(f"{ANSI_GREEN}{addtxt}{ANSI_RESET}")


def warn(msg: str, additional: str = "") -> None:
    print(f"{ANSI_BOLD}{ANSI_YELLOW}{msg}{ANSI_RESET}")
    if additional:
        addtxt = indent(additional, prefix=" >  ")
        print(f"{ANSI_YELLOW}{addtxt}{ANSI_RESET}")


def error(msg: str, exitcode: int = 1, additional: str = "") -> None:
    print(f"{ANSI_BOLD}{ANSI_RED}{msg}{ANSI_RESET}")
    if additional:
        addtxt = indent(additional, prefix="  ")
        print(f"{ANSI_RED}{addtxt}{ANSI_RESET}")

    sys.exit(exitcode)


def main(args):
    if not shutil.which("docker"):
        warn("Docker is not available, NOT linting modified Groovy files")
        sys.exit(0)

    filelist = ",".join(args.files)

    # NOTE:2025-01-13:see list of tags on DockerHub: https://hub.docker.com/r/codenarc/codenarc/tags
    # this is current the latest tag that supports Groovy 2.x (our Jenkins currently runs 2.4.21)
    # this Docker image is ~200 MB in size
    CODENARC_TAG = "2.2.0-groovy2.5.14"

    uid = os.getuid()
    cwd = os.getcwd()

    cmd = (
        "docker run --rm -v "
        f"{cwd}:/ws "
        f"--user {uid}:{uid} "
        f"codenarc/codenarc:{CODENARC_TAG} "
        f"-report=text:stdout -basedir=jenkins"
    ).split()
    cmd.append(f"-includes={filelist}")

    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    if "Compilation failed" in proc.stdout:
        error(f"Compilation failure while linting Groovy file(s)", additional=proc.stdout)
    elif proc.returncode != 0:
        error(f"Groovy lint failed", additional=proc.stdout, exitcode=proc.returncode)
    else:
        info("Groovy lint OK")


if __name__ == "__main__":
    args = parser.parse_args()

    main(args)
