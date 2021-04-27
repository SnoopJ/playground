from functools import wraps
import logging
from typing import Optional

import attr


logger = logging.getLogger(__name__)


def _ensure_set(val):
    if isinstance(val, str):
        return {val}
    else:
        return set(val)


DEFAULT_TAG = "<NO TAG>"


@attr.s
class TagFilter(logging.Filter):
    """Filter LogRecords based on the associated tag"""

    tags = attr.ib(type=set, converter=_ensure_set)
    pass_untagged = attr.ib(type=bool, default=True)

    def filter(self, record):
        tag = str(getattr(record, "tag", DEFAULT_TAG))
        allow = (tag in self.tags) or (self.pass_untagged and tag == DEFAULT_TAG)

        return allow


def _ensure_tag(f):
    @wraps(f)
    def _wrapper(*args, **kwargs):
        prev = kwargs.get("extra", {})
        kwargs["extra"] = {"tag": DEFAULT_TAG, **prev}
        return f(*args, **kwargs)

    return _wrapper


class TagLogger(logging.Logger):
    """Logger subclass that supports tag-driven logging"""

    log = _ensure_tag(logging.Logger.log)
    info = _ensure_tag(logging.Logger.info)
    debug = _ensure_tag(logging.Logger.debug)
    warning = _ensure_tag(logging.Logger.warning)
    error = _ensure_tag(logging.Logger.error)
    critical = _ensure_tag(logging.Logger.critical)

    def log_tag(self, tag: str, msg: str, *args, **kwargs):
        """
        Log a message with the given tag

        Parameters
        ----------
        tag: str
            The name of the tag
        msg: str
            The logging message

        *args, **kwargs are passed to `logging.Logger.log()`

        If `level` is not given in `kwargs`, this logger's current level is used
        """
        prev = kwargs.get("extra", {})
        kwargs["extra"] = {"tag": tag, **prev}
        lvl = kwargs.pop("level", self.getEffectiveLevel())
        return self.log(lvl, msg, *args, **kwargs)
