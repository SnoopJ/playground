import logging
from typing import Tuple

from sopel import plugin


LOGGER = logging.getLogger(__name__)


def _parse_subcmd(bot, trigger, subcmd_prefix: str) -> Tuple[str, str]:
    cmd, sep, subcmd = trigger.group(0).partition(subcmd_prefix)
    N_prefix = len(bot.settings.core.prefix)
    prefix, cmd = cmd[:N_prefix-1], cmd[N_prefix-1:]

    return cmd, subcmd


def _dispatch_subcmd(bot, trigger, *func_args, subcmd_prefix: str = ":", **func_kwargs) -> bool:
    """Dispatch the given trigger to a subcommand, if one is available.

    Returns ``False`` if a subcommand handler could not be located, ``True``
    otherwise.

    Note: ``func_args, func_kwargs`` will be passed to the handler as-is.
    Note: this helper passes all exceptions from the handler to the caller.
    """
    cmd, subcmd = _parse_subcmd(bot, trigger, subcmd_prefix=subcmd_prefix)

    try:
        funcname = f"{cmd}_{subcmd}"
        # NOTE:this does restrict us to defining handlers at the module level…
        func = globals()[funcname]
    except LookupError:
        LOGGER.debug("Cannot find subcommand handler %r", funcname)
        return False

    func(bot, trigger, *func_args, **func_kwargs)
    return True


def dummy_subcmd1(bot, trigger, *args, **kwargs):
    bot.say(f"dummy:subcmd1 subcommand (args={args!r}, kwargs={kwargs!r})")


def dummy_subcmd2(bot, trigger, *args, **kwargs):
    bot.say(f"dummy:subcmd2 subcommand (args={args!r}, kwargs={kwargs!r})")


@plugin.commands(
        "dummy",
        "dummy:subcmd1",
        "dummy:subcmd2",
        "dummy:fakesub",  # this pattern has no dedicated handler, we will use the base
)
def dummy(bot, trigger):
    data = 42
    moredata = "Twas brillig and the slithy toves"

    if _dispatch_subcmd(bot, trigger, data, moredata=moredata):
        return

    # we don't *have* to pass data to the handler if ``bot, trigger`` is enough
    # if _dispatch_subcmd(bot, trigger):
    #     return

    bot.say(f"base command, invoked as {trigger.group(0)!r}")
