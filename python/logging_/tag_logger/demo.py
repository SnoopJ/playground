import logging
from typing import List

from logtag import TagFilter, TagLogger


logging.basicConfig(format="[%(levelname)s:%(tag)s] %(message)s")  # set up stream output

logging.setLoggerClass(TagLogger)  # tell the logging module it should use our class
logger = logging.getLogger(__name__)
print(f"Created logger of type {type(logger)}")
logger.setLevel(logging.DEBUG)


def make_noise():
    """A helper to spit out a bunch of logging messages"""
    # log all known tags
    for tag in KNOWN_TAGS:
        logger.log_tag(tag, "Known tag, with implicit level")
        logger.log_tag(tag, "Known tag, with explicit level\n", level=logging.ERROR)

    # Normal logger use is fine, messages are untagged
    logger.info("Untagged INFO message")
    logger.debug("Untagged DEBUG message\n")

    # produce messages with unknown tags
    for tag in ["UnknownTag1", "UnknownTag2"]:
        logger.log_tag(tag, "Unknown tag")


def example(tags: List[str], pass_untagged: bool = True):
    flt = TagFilter(tags, pass_untagged=pass_untagged)
    logger.addFilter(flt)

    # for demo purposes only!
    print(f"\n\N{WHITE MEDIUM STAR}{flt}\n==============")

    make_noise()
    logger.removeFilter(flt)


if __name__ == "__main__":
    KNOWN_TAGS = ["Tag1", "Tag2", "Tag3"]      # our filter is aware of such-and-such tags

    example(KNOWN_TAGS)                        # we can include untagged messages…
    example(KNOWN_TAGS, pass_untagged=False)   # … or exclude them

    example("Tag1")                            # we can filter by single tags…
    example("Tag2")                            #
    example(["Tag1", "Tag2"])                  # …or multiple tags
    print()
