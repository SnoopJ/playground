from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AcmeSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ACME_")

    data: int = Field(default=42)
    # NOTE: if the field's aliases do not include the name itself (it feels silly to call this an alias), then attempting
    # to populate this field with its name will cause an error, as Pydantic treats it as "extra" data
    somefield: str = Field(default="", alias=AliasChoices("somefield", "ACME_SOMEFIELD_ALTERNATE_NAME"))


print(f'{AcmeSettings() = }')
print(f'{AcmeSettings(somefield="test") = }')

# We don't really *need* to populate by the alias used to expose an alternative environment variable, but it is a thing
# that becomes possible with this aliasing scheme.
print(f'{AcmeSettings(ACME_SOMEFIELD_ALTERNATE_NAME="test") = }')
