from configparser import ConfigParser
from packaging.requirements import Requirement
from pathlib import Path


HERE = Path(__file__).parent.resolve()

def _requirements(cfg_file: Path):
    """Parse a setuptools setup.cfg and extract a list of Requirements corresponding to install_requires"""
    if not cfg_file.exists():
        raise RuntimeError(f"File does not exist: {cfg_file}")

    config = ConfigParser()
    config.read(cfg_file)

    reqs_txt = config["options"]["install_requires"].strip().split("\n")
    return [Requirement(r) for r in reqs_txt]


if __name__ == "__main__":
    reqs = _requirements(HERE.joinpath("setup.cfg"))

    # filter out the enumerated packages, producing a new list of requirements
    IGNORE_PKGS = {"pkgB", "pkgD"}
    reqs_filtered = [req for req in reqs if req.name not in IGNORE_PKGS]

    result = "\n".join(str(req) for req in reqs_filtered)

    print(result)
