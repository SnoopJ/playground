import os.path
import logging
import sys
from pathlib import Path
from zipfile import BadZipFile, ZipFile


try:
    # use fancy progress bar if tqdm is present
    from tqdm import tqdm as with_progress_bar
except ImportError:
    def with_progress_bar(it):
        yield from it


PIP_CACHE = Path("~/.cache/pip/").expanduser()


logger = logging.getLogger(__name__)


def cached_packages(cache_dir: Path):
    candidates = list(cache_dir.glob("**/*.body"))
    for pth in with_progress_bar(candidates):
        try:
            zf = ZipFile(pth)
            # NOTE: this is being a little lazy, there could technically be another file named METADATA that is *not* the dist-info entry
            metadata_file_entry = next((f for f in zf.filelist if Path(f.filename).name == "METADATA"), None)
            if not metadata_file_entry:
                logger.warning(f"File is a ZIP but does not have a METADATA entry, skipping: {pth}", stacklevel=-1)
                continue
            metadata = zf.read(metadata_file_entry).decode().splitlines()
            pkg_name = next(line for line in metadata if line.startswith("Name: ")).removeprefix("Name: ")
            pkg_version = next(line for line in metadata if line.startswith("Version: ")).removeprefix("Version: ")
            yield (pkg_name, pkg_version, pth)
        except BadZipFile as exc:
            # not a zip file, move on
            continue


if __name__ == "__main__":
    logging.basicConfig()

    pkgs = sorted(cached_packages(PIP_CACHE))
    if not pkgs:
        print("Cannot find pre-built wheels in pip HTTP cache")
        sys.exit(0)

    formatted_pkgs = [(f"{name}=={ver}", pth) for name, ver, pth in pkgs]
    pad_width = max(len(req) for req, pth in formatted_pkgs) + 3

    print("\nFound wheels in pip HTTP cache:")
    print("-------------------------------")
    for (req, pth) in formatted_pkgs:
        print(f"{req: >{pad_width}}  {pth}")
