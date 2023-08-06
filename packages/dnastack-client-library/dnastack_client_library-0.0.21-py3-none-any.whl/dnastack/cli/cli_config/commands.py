import click
import yaml
import json

from dnastack.constants import *
from dnastack.cli.utils import *


class ConfigHelp(click.Command):
    def format_help(self, ctx, formatter):
        click.echo("Usage: dnastack config set [OPTIONS] KEY VALUE")
        click.echo("Options:")
        click.echo(" --help  Show this message and exit.")
        click.echo("Accepted Keys: ")
        for key in ACCEPTED_CONFIG_KEYS:
            click.echo(f"\t{key}")


@click.group()
@click.pass_context
def config(ctx):
    pass


@config.command(name="list")
@click.pass_context
def config_list(ctx):
    click.echo(json.dumps(ctx.obj, indent=4))
    return


@config.command()
@click.pass_context
@click.argument("key")
def get(ctx, key):
    assert_config(ctx, key)

    click.echo(json.dumps(ctx.obj[key], indent=4))
    return


@config.command()
@click.pass_context
@click.argument("key")
@click.argument("value", required=False, default=None, nargs=-1)
def set(ctx, key, value):

    assert_config_key(key)

    if len(value) == 1:
        value = value[0]
    elif len(value) == 2:
        value = {value[0]: value[1]}
    else:
        click.secho(
            f"Invalid value [{' '.join(value)}] provided for configuration key [{key}].",
            fg="red",
        )
        sys.exit(1)

    set_config(ctx, key, value)

    with open(config_file_path, "w") as config_file:
        yaml.dump(ctx.obj, config_file)

    click.echo(json.dumps(ctx.obj, indent=4))
