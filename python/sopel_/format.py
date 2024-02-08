import re

from sopel import plugin
import sopel.formatting


OPENER = r"\{"
CLOSER = r"(?<!\\)\}"  # users who want to embed a } in their text should escape it as \}
FIELDS = "|".join([
    'bold',
    'italic',
    'underline',
    'strikethrough',
    'monospace',
    'reverse',
])
FG = r"(?P<fg>[^, ]+)"
BG = r"(?P<bg>[^, ]+)"
COLOR_PATT = f"{OPENER}(?P<color_field>color)\({FG},\s*{BG}\):(?P<color_text>.*?){CLOSER}"
PATT = (
    f"{OPENER}(?P<field>{FIELDS}):(?P<text>.*?){CLOSER}" +
    "|" +
    COLOR_PATT
)


def _transform(match: re.Match) -> str:
    if match.group("color_field") == "color":
        text = match.group("color_text")
        fg = match.group("fg")
        bg = match.group("bg")

        return sopel.formatting.color(text, fg, bg)

    field = match.group("field")
    txt = match.group("text")

    if not hasattr(sopel.formatting, field):
        raise ValueError(f"No formatting converter for field of type {field!r}")

    return getattr(sopel.formatting, field)(txt)


def _expand_format(txt: str):
    return re.sub(PATT, _transform, txt)


@plugin.command("fmt")
@plugin.output_prefix("[fmt] ")
def fmt(bot, trigger):
    msg = trigger.group(2)
    if not msg or not msg.strip():
        return False

    bot.say(_expand_format(msg))
