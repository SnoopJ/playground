#!/usr/bin/env python3
import argparse
import os
import sys
import warnings
from pathlib import Path
from textwrap import indent
from urllib.parse import urlparse

import requests

ANSI_BOLD = "\x1b[1m"
ANSI_RED = "\x1b[31m"
ANSI_GREEN = "\x1b[32m"
ANSI_YELLOW = "\x1b[33m"
ANSI_RESET = "\x1b[0m"


def jenkins_hostname(hostname_or_url: str) -> str:
    parsed = urlparse(hostname_or_url)
    if parsed.scheme:
        return parsed.hostname
    else:
        # this isn't a URI, assume what the user gave us is the hostname in full
        return hostname_or_url


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--username", default=None, help="Jenkins username")
parser.add_argument("--token", default=None, help="Jenkins API token")
parser.add_argument(
    "--jenkins-instance",
    dest="jenkins_hostname",
    required=True,
    type=jenkins_hostname,
    help="Hostname or URL of Jenkins instance",
)
parser.add_argument(
    "--precommit-mode", action="store_true", help="Exit with code 0 if auth is not available, for use with pre-commit"
)
parser.add_argument("jenkinsfiles", nargs="+")


def lint_jenkinsfile(jenkins_hostname: str, fn: str, username: str, token: str) -> None:
    # See Jenkins documentation: https://www.jenkins.io/doc/book/pipeline/development/#linter
    URL = f"http://{username}:{token}@{jenkins_hostname}/pipeline-model-converter/validate"

    response = requests.post(URL, data={"jenkinsfile": Path(fn).read_bytes()})
    response.raise_for_status()

    JENKINS_SUCCESS_TEXT = "Jenkinsfile successfully validated."
    if response.text.strip() != JENKINS_SUCCESS_TEXT:
        raise ValueError(response.text)


def main(args):
    fail = False

    for fn in args.jenkinsfiles:
        try:
            lint_jenkinsfile(jenkins_hostname=args.jenkins_hostname, fn=fn, username=args.username, token=args.token)
        except ValueError as exc:
            fail = True
            errmsg = indent(exc.args[0], prefix="  > ").rstrip()
            print(f"{ANSI_BOLD}{ANSI_RED}Jenkins lint failed for file {fn!r}:\n{errmsg}{ANSI_RESET}")
        else:
            print(f"{ANSI_GREEN}Jenkins lint OK     for {fn!r}{ANSI_RESET}")

    if fail:
        sys.exit(1)


if __name__ == "__main__":
    args = parser.parse_args()

    if args.precommit_mode:
        if args.username or args.token:
            print(f"{ANSI_BOLD}{ANSI_RED}Must not use --username/--token with --precommit-mode, use JENKINS_AUTH instead{ANSI_RESET}")
            sys.exit(2)

        if "JENKINS_AUTH" not in os.environ:
            # NOTE:pre-commit does not give us a way to skip a hook or run it conditionally, so instead
            # we exit with code 0 and print as obvious a warning as we can
            print(f"{ANSI_BOLD}{ANSI_YELLOW}JENKINS_AUTH is not set, skipping Jenkins linter check{ANSI_RESET}")
            sys.exit(0)

    if args.username and args.token:
        # CLI specified username and token explicitly, nothing further required
        pass
    if (args.username and not args.token) or (args.token and not args.username):
        print(f"{ANSI_BOLD}{ANSI_RED}--username and --token must be specified together{ANSI_RESET}")
        sys.exit(1)
    elif not (args.username and args.token) and "JENKINS_AUTH" in os.environ:
        # Fall back on environment variable if possible
        args.username, sep, args.token = os.environ["JENKINS_AUTH"].partition(":")
    else:
        print(
            f"{ANSI_BOLD}{ANSI_RED}Jenkins authentication must be provided, either by --username and --token, or with "
            "the JENKINS_AUTH environment variable"
        )
        sys.exit(2)

    main(args)
