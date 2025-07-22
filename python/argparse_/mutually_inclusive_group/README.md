This example illustrates how to check that options in an `argparse` group are either unspecified, or ALL specified.

```
$ python3 app.py --param 42
OK

$ python3 app.py --param 42 --foo 1 --bar 2
OK

$ python3 app.py --param 42 --foo 1
Traceback (most recent call last):
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/argparse_/mutually_inclusive_group/app.py", line 25, in <module>
    validate_grp(args)
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/argparse_/mutually_inclusive_group/app.py", line 20, in validate_grp
    raise argparse.ArgumentError(None, f"Must pass ALL group options or NONE of them. Missing values: {nulls}")
argparse.ArgumentError: Must pass ALL group options or NONE of them. Missing values: {'bar'}

$ python3 app.py --param 42 --bar 2
Traceback (most recent call last):
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/argparse_/mutually_inclusive_group/app.py", line 25, in <module>
    validate_grp(args)
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/argparse_/mutually_inclusive_group/app.py", line 20, in validate_grp
    raise argparse.ArgumentError(None, f"Must pass ALL group options or NONE of them. Missing values: {nulls}")
argparse.ArgumentError: Must pass ALL group options or NONE of them. Missing values: {'foo'}

```
