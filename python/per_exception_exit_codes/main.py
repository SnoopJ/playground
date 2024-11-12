import argparse
import sys
import traceback


parser = argparse.ArgumentParser()
parser.add_argument("--fail-first", action="store_true", help="Fail the first step")
parser.add_argument("--fail-second", action="store_true", help="Fail the second step")
parser.add_argument("--fail-acme", action="store_true", help="Produce a generic Acme failure")
parser.add_argument("--fail-general", action="store_true", help="Produce a generic failure")


class AcmeException(Exception):
    """Base class for exceptions specific to the Acme application"""
    # NOTE: We leave some room at the bottom for more generic exit codes. For
    # example, argparse exits with code 2 if an unrecognized option is specified.
    exit_code = 32


class FirstStepFailure(AcmeException):
    """Raised when the first step fails"""
    exit_code = AcmeException.exit_code + 1


class SecondStepFailure(AcmeException):
    """Raised when the second step fails"""
    exit_code = AcmeException.exit_code + 2


def first_step(fail: bool = False):
    if fail:
        raise FirstStepFailure("The first step has failed")

    print("Running the first step")


def second_step(fail: bool = False):
    if fail:
        raise SecondStepFailure("The second step has failed")

    print("Running the second step")


def install_acme_excepthook():
    old_excepthook = sys.excepthook

    def acme_excepthook(type, value, tb):
        if issubclass(type, AcmeException):
            # NOTE: since Python 3.10 this could be just `print_exception(value)`,
            # but we use the backwards-compatible spelling here
            traceback.print_exception(type, value, tb)
            sys.exit(value.exit_code)

        # Otherwise, this isn't our exception, let the other excepthook handle it
        old_excepthook(type, value, traceback)

    sys.excepthook = acme_excepthook


def main(args):
    install_acme_excepthook()

    if args.fail_general:
        raise RuntimeError("This is a general failure caused by an exception outside the Python exception hierarchy")
    elif args.fail_acme:
        raise AcmeException("This is a general Acme failure not associated with a specific failure mode")

    first_step(fail=args.fail_first)
    second_step(fail=args.fail_second)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
