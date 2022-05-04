"""
Helper script to install only a project's dependencies

NOTE:20220412:this became necessary while working on a work issue where
dependencies declared against GitLab were misbehaved on a system that does
not have its git configured to authenticate with an internal GitLab instance.

This caused `pip install .[dev]` to fail in CI and the best workaround seems to
be to parse out the non-GitLab requirements and install them as normal, then
install the finicky ones by hand in the Jenkins script, and install the
project itself with the `--no-deps` option.
"""
import subprocess
import sys
from configparser import ConfigParser
from pathlib import Path
import typing

from packaging.requirements import Requirement


HERE = Path(__file__).parent.resolve()
SETUP_CFG = HERE.parent.joinpath("setup.cfg")


def _requirements(cfg_file: Path) -> List[Requirement]:
    """Parse a setuptools setup.cfg and extract a list of Requirements corresponding to install_requires"""
    if not cfg_file.exists():
        raise RuntimeError(f"File does not exist: {cfg_file}")

    config = ConfigParser()
    config.read(cfg_file)

    reqs_txt = config["options"]["install_requires"].strip().split("\n")
    return [Requirement(r) for r in reqs_txt if r]


if __name__ == "__main__":
    reqs = _requirements(SETUP_CFG)

    print(f"Installing {len(reqs_filtered)} requirements (out of {len(reqs)})")
    for req in reqs:
        cmd = [sys.executable, "-m", "pip", "install", str(req)]
        print(f"Running command {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
