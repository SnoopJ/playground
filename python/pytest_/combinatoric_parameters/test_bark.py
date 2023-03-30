import pytest

from bark import bark


@pytest.mark.parametrize("speaker", ["猫", "😺"])
@pytest.mark.parametrize("message", ["meow", "にゃああああ〜"])
def test_oration(speaker, message):
    bark(speaker, message)
