This sample demonstrates a confusing problem I discovered when migrating an application from Pydantic v1 over to v2.

In particular, the v1 version of the application has some config fields that do not follow the general prefix convention
for the rest of the fields: the environment variables for these fields are set explicitly. While it is possible to change
the sites of use of these environment variables, it's a compatibility nuisance.

It turns out that the fix for this behavior is that the field must contain _its own name_ in the list of aliases. This
is incredibly counterintuitive, but I'm just glad that there is a fix for what I feared was irreconcilable breakage.


### `broken.py` behavior

```
$ ACME_SOMEFIELD_ALTERNATE_NAME="asdf" python3 broken.py
AcmeSettings() = AcmeSettings(data=42, somefield='asdf')
Failed to create AcmeSettings, error was:
    > 1 validation error for AcmeSettings
    > somefield
    >   Extra inputs are not permitted [type=extra_forbidden, input_value='test', input_type=str]
    >     For further information visit https://errors.pydantic.dev/2.11/v/extra_forbidden
AcmeSettings(ACME_SOMEFIELD_ALTERNATE_NAME="test") = AcmeSettings(data=42, somefield='test')
```

### `working.py` behavior

```
$ ACME_SOMEFIELD_ALTERNATE_NAME="asdf" python3 scratch.py
AcmeSettings() = AcmeSettings(data=42, somefield='asdf')
AcmeSettings(somefield="test") = AcmeSettings(data=42, somefield='test')
AcmeSettings(ACME_SOMEFIELD_ALTERNATE_NAME="test") = AcmeSettings(data=42, somefield='test')
```
