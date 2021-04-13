import pytest
import foo


def test_print_it(capfd):
    for s in ("hey", "\N{SNAKE}", "猫", "\N{BLACK FLAG}\N{ZERO WIDTH JOINER}\N{SKULL AND CROSSBONES}\N{VARIATION SELECTOR-16}"):
        foo.print_it(s);
        captured = capfd.readouterr()
        assert captured.out == f"{s}\n"


def test_get_it():
    assert foo.get_it() == "猫 nyaa"
