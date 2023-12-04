# -*- coding: UTF-8 -*-
"""
This is a helper script designed to run the `ProcDump` tool [1] from
Sysinternals without a lot of user intervention. It's designed to allow the
user to drag and drop their target program onto this one from the GUI.

[1] https://learn.microsoft.com/en-us/sysinternals/downloads/procdump
"""
import argparse
import os
import runpy
import ssl
import subprocess
import sys
import time
import urllib.request
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile


HERE = Path(__file__).parent
PROCDUMP_DIR = HERE.joinpath("procdump")
PROCDUMP_EXE = PROCDUMP_DIR.joinpath("procdump.exe")

PROCDUMP_ZIP_URL = "https://download.sysinternals.com/files/Procdump.zip"


parser = argparse.ArgumentParser()
parser.add_argument("--insecure", action="store_true", help="Disable verification of SSL certificates")
parser.add_argument("python_program", help="Python program to run using procdump")
parser.add_argument("python_program_args", nargs="*", help="Arguments passed to the target program")


def download_procdump(insecure: bool = False) -> bytes:
    ctx = ssl.create_default_context()
    if insecure:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

    response = urllib.request.urlopen(PROCDUMP_ZIP_URL, context=ctx)
    assert response.status == 200, f"Got unexpected HTTP response status {response.status}"
    response_data = BytesIO(response.read())
    zf = ZipFile(response_data)
    PROCDUMP_DIR.mkdir(exist_ok=True)
    zf.extractall(path=PROCDUMP_DIR)


if __name__ == "__main__":
    if sys.platform != "win32":
        print(f"This helper is designed to run on platform 'win32', but found platform {sys.platform!r}")
        raise SystemExit(1)

    args = parser.parse_args()

    if not PROCDUMP_EXE.exists():
        print("Downloading procdump.zip from sysinternals.com")
        download_procdump(insecure=args.insecure)

    assert PROCDUMP_EXE.exists(), f"{str(PRODDUMP_EXE)!r} does not exist!"

    # This is a fairly simple procdump invocation looking for generating a minidump on any "first chance" exception
    # Advanced users might want to change this
    # TODO: allow changing the procdump flags from the commandline?
    procdump_cmd = [str(PROCDUMP_EXE), "-e", "1", str(os.getpid())]
    print(f"Running procdump: {procdump_cmd!r}")
    subprocess.Popen(procdump_cmd)
    # sleep for a moment to be sure that procdump has actually started up and attached to this process
    time.sleep(3)

    print(f"Running target program: {args.python_program} {args.python_program_args}")
    sys.argv[1:] = args.python_program_args
    runpy.run_path(args.python_program, run_name="__main__")
