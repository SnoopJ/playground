from textwrap import indent

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AcmeSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ACME_")

    data: int = Field(default=42)
    # NOTE:This field's associated environment variable does not follow the prefix convention
    somefield: str = Field(default="", alias=AliasChoices("ACME_SOMEFIELD_ALTERNATE_NAME"))


print(f'{AcmeSettings() = }')
try:
    print(f'{AcmeSettings(somefield="test") = }')  # error due to an "extra" field
except Exception as exc:
    print(f"Failed to create AcmeSettings, error was:")
    print(indent(repr(exc), prefix="\t> "))
print(f'{AcmeSettings(ACME_SOMEFIELD_ALTERNATE_NAME="test") = }')  # "works", but confusing and undesirable
