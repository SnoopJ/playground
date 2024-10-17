import logging
import site
from datetime import datetime
from itertools import chain
from pathlib import Path


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig()

    site_paths = [Path(entry) for entry in (*site.getsitepackages(), site.getusersitepackages())]
    gen = chain.from_iterable(pth.glob("*.dist-info/INSTALLER") for pth in site_paths)
    installer_files = sorted(gen, key=lambda pth: pth.stat().st_ctime)

    pkginfo = []

    for pkg_installer_pth in installer_files:
        metadata_pth = pkg_installer_pth.parent.joinpath("METADATA")
        if not metadata_pth.exists():
            logger.warning("INSTALLER file does not have corresponding METADATA, skipping: %r", str(pkg_installer_pth))

        metadata = metadata_pth.read_text().splitlines()

        pkg_name = next(line for line in metadata if line.startswith("Name: ")).removeprefix("Name: ")
        pkg_version = next(line for line in metadata if line.startswith("Version: ")).removeprefix("Version: ")
        req = f"{pkg_name}=={pkg_version}"
        pkg_installed_time = datetime.fromtimestamp(pkg_installer_pth.stat().st_ctime)

        pkginfo.append((req, pkg_installed_time))


    pad_width = max(len(req) for req, _ in pkginfo) + 3

    sites_report = "\n\t".join([str(pth) for pth in site_paths])
    print(f"Found {len(site_paths)} sites:\n\t{sites_report}\n")

    print("Installation history")
    print("--------------------")

    for req, install_time in pkginfo:
        t_fmt = install_time.strftime("%Y-%m-%d at %H:%M")
        print(f"{req: <{pad_width}} installed {t_fmt}")
