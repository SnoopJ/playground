from __future__ import annotations
import argparse
import logging
import re

from PyInstaller.__main__ import run as run_pyinstaller


parser = argparse.ArgumentParser()
parser.add_argument(
    "--promote-collection-warnings",
    action="store_true",
    help='Promote PyInstaller collection "is not a package" warnings to fatal exceptions'
)


class PromotionFilter(logging.Filter):
    """
    Promotes matching log records into exceptions
    """

    def __init__(self, name: str = "", levelno: int | None = None, message_pattern: re.Pattern | None = None):
        super().__init__(name)
        self.levelno = levelno
        self.message_pattern = message_pattern

    def filter(self, record) -> bool:
        if self.levelno and record.levelno != self.levelno:
            return True

        if self.message_pattern:
            msg = record.getMessage()
            if re.match(self.message_pattern, msg):
                raise Exception(record.getMessage())

        return True


def main(args):
    if args.promote_collection_warnings:
        promotion_filter = PromotionFilter(levelno=logging.WARNING, message_pattern=".*not a package.*")
        # NOTE:if the Filter is attached to a specific Logger, it applies only to records created by *that* logger
        # If the filter should instead apply to messages at multiple levels in a hierarchy, it should probably be
        # attached to the relevant handler(s), or to any logger to which it should apply
        target_logger = logging.getLogger("PyInstaller.utils.hooks")
        target_logger.addFilter(promotion_filter)

    # Invoke PyInstaller with instructions to collect all files for a package that does not exist, to simulate a real-world
    # case where some automation built a nonsense distribution because some of the necessary preconditions were not satisfied
    args = [
        "--clean",
        "--noconfirm",
        "--collect-all", "thispackagedoesnotexist",
        __file__,
    ]
    run_pyinstaller(args)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
