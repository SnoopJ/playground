import logging


class AcmeFormatter(logging.Formatter):
    def formatStack(self, stack_info: str) -> str:
        lines = stack_info.splitlines()
        acc = lines[:1]
        for line in lines[1:]:
            if line.lstrip().startswith("File"):
                acc.append(line)
        return "\n".join(acc)


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
fmt = "[%(levelname)s]: %(message)s"

logging.basicConfig(
    level=logging.INFO,
    handlers=[handler],
    format=fmt,
)

def func(msg, level: int = 0):
    if level > 0:
        func(msg, level - 1)
    else:
        logger.info(msg, stack_info=True)


func("This is a logger message with a verbose stack", level=3)

formatter = AcmeFormatter(fmt)
handler.setFormatter(formatter)

func("This is a logger message with a concise stack", level=3)
