import argparse
import textwrap
import time
from typing import Optional

import requests
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version


HEADERS = {"Accept": "application/vnd.pypi.simple.v1+json"}


parser = argparse.ArgumentParser(description="Query the PyPI JSON APIs for information about a package's requirements across multiple versions")
parser.add_argument("pkg", type=str, help="The name of a package to query")
parser.add_argument("-r", "--requirement", action="append", dest="reqs", help="Optional name of a requirement to query across each version. May be given multiple times")
parser.add_argument("--pre", action="store_true", help="If given, show pre-release versions")
parser.add_argument("--min", type=Version, help="If given, minimum package version to consider")
parser.add_argument("--max", type=Version, help="If given, maximum package version to consider")
parser.add_argument("--rate-limit", type=float, default=100, help="Maximum number of requests/sec to make to PyPI")


def _pkg_versions(pkg: str, min: Optional[Version], max: Optional[Version]) -> list[Version]:
    r = requests.get(f"https://pypi.org/simple/{pkg}/", headers=HEADERS)
    r.raise_for_status()
    doc = r.json()
    versions = []
    for ver in doc.get("versions", []):
        v = Version(ver)
        if min and v < min:
            continue
        if max and v > max:
            continue
        versions.append(v)

    return sorted(versions)


def _reqs(pkg: str, version: Version) -> Optional[list[str]]:
    r = requests.get(f"https://pypi.org/pypi/{pkg}/{str(version)}/json")
    r.raise_for_status()
    doc = r.json()

    reqs = doc.get("info", {}).get("requires_dist")

    if reqs:
        reqs = [Requirement(r) for r in reqs]

    return sorted(reqs, key=lambda r: r.name.casefold())


def _report(pkg: str, version: Version, reqs: Optional[list[Requirement]], filter_reqs: Optional[list[str]]) -> None:
    if not reqs:
        print(f"{pkg}=={version} - [no requirements listed]")
        return

    if filter_reqs:
        reqs = [str(r) for r in reqs if r.name in filter_reqs]
        print(f"{pkg}=={version} - {reqs}")
    else:
        print(f"{pkg}=={version}\n---")
        reqinfo = textwrap.indent("\n".join(str(r) for r in reqs), " "*4)
        print(reqinfo)
        print()


def main():
    args = parser.parse_args()
    if args.reqs:
        filter_reqs = [canonicalize_name(r) for r in args.reqs]
    else:
        filter_reqs = None

    versions = _pkg_versions(args.pkg, min=args.min, max=args.max)
    if not args.pre:
        versions = [ver for ver in versions if not ver.is_prerelease]

    for ver in versions:
        reqs = _reqs(args.pkg, ver)
        _report(args.pkg, ver, reqs, filter_reqs)
        # this is a naive way to rate-limit, but it's simple and guarantees we don't exceed the limit
        time.sleep(1/args.rate_limit)


if __name__ == "__main__":
    main()
