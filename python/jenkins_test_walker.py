"""
A helper script for trawling through Jenkins Test Reports in JSON format
"""
import argparse
import json
import re
import sys

import requests


parser = argparse.ArgumentParser(description="Jenkins testReport helper")
parser.add_argument("--debug", action="store_true")
parser.add_argument("--no-details", action="store_true", help="Suppress details on matching filters")
parser.add_argument("--url", default=None, help="A Jenkins job URL")
parser.add_argument("--json", default=None, help="Path to a Jenkins testReport in JSON format")
parser.add_argument("--status", default=None, type=str.upper, choices=["PASSED", "FAILED", "SKIPPED"], help="Only handle test cases with the given status")
parser.add_argument("--class-name", default=None, help="If given, regex filter over className field")
parser.add_argument("--name", default=None, help="If given, regex filter over name field")
parser.add_argument("--stdout", default=None, help="If given, regex filter over stdout field")
parser.add_argument("--stderr", default=None, help="If given, regex filter over stderr field")
parser.add_argument("--error-details", default=None, help="If given, regex filter over errorDetails field")
parser.add_argument("--error-stack-trace", default=None, help="If given, regex filter over errorStackTrace field")


def should_skip(case, args):
    if args.status and case.get("status") != args.status:
        return True

    for argname, case_field in _regex_filters(case).items():
        pattern = getattr(args, argname)
        if not pattern:
            continue

        if not case_field:
            return True

        if case_field:
            m = re.search(pattern, case_field)
            if not m:
                return True

    return False


def _testReport_json(args):
    if args.json:
        with open(args.json, "r") as f:
            report = json.load(f)
    elif args.url:
        JENKINS_JOB_PATT = r"(?P<job_root>http.*/job/(?P<job_name>[^/]+)/(?P<job_id>\d+)).*"
        m = re.match(JENKINS_JOB_PATT, args.url)
        if not m:
            raise ValueError(f"URL does not look like a Jenkins job: {args.url!r}")

        testReport_url = m.group("job_root") + "/testReport/api/json"
        job_name = m.group("job_name")
        job_id = m.group("job_id")

        response = requests.get(testReport_url, allow_redirects=True)
        if not response.ok:
            raise ValueError(f"Could not get testReport information from {job_name!r} #{job_id} (this job may not have run any tests)")

        report = response.json()
    else:
        report = None

    return report


def _check_args(args):
    if sum([bool(args.url), bool(args.json)]) != 1:
        parser.exit(status=2, message="Must pass exactly one of --url or --json\n")


def _regex_filters(case):
    return {
        "name": case.get("name") or "",
        "class_name": case.get("className") or "",
        "stdout": case.get("stdout") or "",
        "stderr": case.get("stderr") or "",
        "error_details": case.get("errorDetails") or "",
        "error_stack_trace": case.get("errorStackTrace") or "",
    }


def main(args):
    _check_args(args)

    report = _testReport_json(args)
    if not report:
        raise ValueError("Could not get testReport JSON")

    suites = {}
    cases = []

    for suite in report.get("suites", []):
        class_name = suite.get("name", "<UNKNOWN className>")
        if args.class_name and not re.search(args.class_name, class_name):
            continue

        for case in suite.get("cases", []):
            if should_skip(case, args=args):
                continue

            cases.append(case)

        suites[class_name] = cases.copy()
        cases.clear()

    for suite_name, cases in suites.items():
        if cases:
            print(suite_name)

        for case in cases:
            case_name = case.get("name", "<UNKNOWN name>")
            print("\t" + case_name)

            if not args.no_details:
                for argname, case_field in _regex_filters(case).items():
                    arg_value = getattr(args, argname)
                    if arg_value:
                        print(f"{argname}: {case_field!r}")


if __name__ == "__main__":
    args = parser.parse_args()
    try:
        main(args)
    except Exception as exc:
        if args.debug:
            # full stack trace for debug mode
            raise exc
        else:
            sys.exit(repr(exc))
