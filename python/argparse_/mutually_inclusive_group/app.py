import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--param", type=int, required=True)

grp = parser.add_argument_group("mygroup", description="Must pass ALL arguments in this group or NONE of them")
grp.add_argument("--foo", type=str, default=None)
grp.add_argument("--bar", type=str, default=None)


def validate_grp(args):
    dests = [act.dest for act in grp._group_actions]

    opt_values = [getattr(args, d) for d in dests]
    non_nulls = [opt for opt in opt_values if opt is not None]

    if len(non_nulls) not in (0, len(opt_values)):
        nulls = {d for d in dests if getattr(args, d) is None}
        raise argparse.ArgumentError(None, f"Must pass ALL group options or NONE of them. Missing values: {nulls}")


if __name__ == "__main__":
    args = parser.parse_args()
    validate_grp(args)

    print("OK")
