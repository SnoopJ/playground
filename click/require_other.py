import click

def require(*opts: str):
    """Require a Click flag to be set"""
    def _validate(ctx, param, value):
        if value:
            for opt in opts:
                if not ctx.params.get(opt):
                    raise click.UsageError(f"Parameter {param.name} requires {opt}, but not found")

        return value

    return _validate

@click.command()
@click.option("--foo", is_flag=True, is_eager=True)
@click.option("--bar", callback=require("foo"), is_flag=True)
@click.option("--baz", callback=require("foo", "bar"), is_flag=True)
def cli(foo, bar, baz):
    print(f"{foo=}, {bar=}, {baz=}")
    pass

if __name__ == "__main__":
    cli()
