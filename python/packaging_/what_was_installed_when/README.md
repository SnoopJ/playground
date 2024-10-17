This program scans through the visible Python sites to find [`INSTALLER` files]
and reports the associated distributions sorted by creation time of the `INSTALLER`
file, which is a decent proxy for when the distribution was installed.

[`INSTALLER` files]: https://packaging.python.org/en/latest/specifications/recording-installed-packages/#the-installer-file

```
$ python3 what_was_installed_when.py
Found 2 sites:
        /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/.direnv/python-3.9.16/lib/python3.9/site-packages
        /home/snoopjedi/.local/lib/python3.9/site-packages

Installation history
--------------------
astpretty==2.1.0                     installed 2022-01-20 at 23:37
mpmath==1.2.1                        installed 2022-02-23 at 17:28
setuptools==58.1.0                   installed 2024-06-04 at 14:41
pip==22.0.4                          installed 2024-06-04 at 14:41
altgraph==0.17.4                     installed 2024-06-04 at 14:42
zipp==3.19.2                         installed 2024-06-04 at 14:42
packaging==24.0                      installed 2024-06-04 at 14:42
importlib_metadata==7.1.0            installed 2024-06-04 at 14:42
pyinstaller-hooks-contrib==2024.6    installed 2024-06-04 at 14:42
pyinstaller==6.7.0                   installed 2024-06-04 at 14:42
lxml==5.2.2                          installed 2024-07-17 at 00:41
numpy==2.0.1                         installed 2024-07-26 at 15:43
tomli==2.0.1                         installed 2024-08-26 at 22:05
pluggy==1.5.0                        installed 2024-08-26 at 22:05
iniconfig==2.0.0                     installed 2024-08-26 at 22:05
exceptiongroup==1.2.2                installed 2024-08-26 at 22:05
pytest==8.3.2                        installed 2024-08-26 at 22:05
q==2.7                               installed 2024-08-26 at 22:08
wcwidth==0.2.13                      installed 2024-08-26 at 22:11
typing_extensions==4.12.2            installed 2024-08-26 at 22:11
Pygments==2.18.0                     installed 2024-08-26 at 22:11
parso==0.8.4                         installed 2024-08-26 at 22:11
urwid==2.6.15                        installed 2024-08-26 at 22:11
jedi==0.19.1                         installed 2024-08-26 at 22:11
urwid_readline==0.14                 installed 2024-08-26 at 22:11
pudb==2024.1.2                       installed 2024-08-26 at 22:11
pyproject_hooks==1.1.0               installed 2024-09-04 at 17:14
build==1.2.1                         installed 2024-09-04 at 17:14
urllib3==2.2.3                       installed 2024-09-13 at 13:11
sniffio==1.3.1                       installed 2024-09-13 at 13:11
pydantic_core==2.23.3                installed 2024-09-13 at 13:11
idna==3.8                            installed 2024-09-13 at 13:11
h11==0.14.0                          installed 2024-09-13 at 13:11
charset-normalizer==3.3.2            installed 2024-09-13 at 13:11
certifi==2024.8.30                   installed 2024-09-13 at 13:11
annotated-types==0.7.0               installed 2024-09-13 at 13:11
uvicorn==0.30.6                      installed 2024-09-13 at 13:11
requests==2.32.3                     installed 2024-09-13 at 13:11
pydantic==2.9.1                      installed 2024-09-13 at 13:11
anyio==4.4.0                         installed 2024-09-13 at 13:11
starlette==0.38.5                    installed 2024-09-13 at 13:11
fastapi==0.114.1                     installed 2024-09-13 at 13:11
appdirs==1.4.4                       installed 2024-10-17 at 11:04
toml==0.10.2                         installed 2024-10-17 at 11:04
python-magic==0.4.27                 installed 2024-10-17 at 11:04
click==7.1.2                         installed 2024-10-17 at 11:04
steck==0.7.0                         installed 2024-10-17 at 11:04
opencv-python==4.10.0.84             installed 2024-10-17 at 18:14
```
