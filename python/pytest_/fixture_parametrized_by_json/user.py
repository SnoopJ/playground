from dataclasses import dataclass


VALID_COLORS = {"Orange", "Purple", "Blue"}


@dataclass
class User:
    name: str
    favorite_color: str
