import logging
import timeit


# NOTE: we don't actually care where the output goes, so we use a dummy stream,
# but as far as logging knows, we are writing our messages to a 'real' file
devnull = open("/dev/null", "w")
logging.basicConfig(stream=devnull)
logger = logging.getLogger(__name__)

x = 42


def fstring_way():
    logger.debug(f"This line builds the output string every time this line runs, even if the message isn't emitted. x={x}")


def logging_way():
    logger.debug("This line builds the output string only if the message is going to be emitted. x=%s", x)


if __name__ == "__main__":
    N = 10_000
    REPEAT = 100

    print(f"All values given for repeat={REPEAT}, number={N}\n")

    for lvl in ("INFO", "DEBUG"):
        logger.setLevel(lvl)
        extra = " (may take a little while)" if lvl == "DEBUG" else ""
        print(f"Logging level {lvl}{extra}\n-----")

        fsw_timer = timeit.Timer(stmt="fstring_way()", globals=globals())
        # best of 5
        fsw_t = min(fsw_timer.repeat(repeat=REPEAT, number=N))
        print(f"f-string way: {fsw_t:.2e} sec")

        lgw_timer = timeit.Timer(stmt="logging_way()", globals=globals())
        # best of 5
        lgw_t = min(lgw_timer.repeat(repeat=REPEAT, number=N))
        print(f"logging way: {lgw_t:.2e} sec")

        # NOTE: this is just one way to talk about the relative difference between
        # these two styles of string formatting, but since we expect these to be
        # *similar* speeds this is a good way to do it.
        avg = (fsw_t + lgw_t) / 2
        diff = abs(fsw_t - lgw_t) / avg
        print(f"Relative difference: {100*diff:.1f}%\n")



# typical output:

# $ python3 formatting_perf.py
# All values given for repeat=100, number=10000
#
# Logging level INFO
# -----
# f-string way: 5.68e-03 sec
# logging way: 4.13e-03 sec
# Relative difference: 31.8%
#
# Logging level DEBUG (may take a little while)
# -----
# f-string way: 1.65e-01 sec
# logging way: 1.81e-01 sec
# Relative difference: 9.2%
