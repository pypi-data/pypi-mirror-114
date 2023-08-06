from dnastack.cli.utils import assert_config
from dnastack.client import *
from .tables import commands as tables_commands


@click.group()
@click.pass_context
def collections(ctx):
    assert_config(ctx, "collections-url", str)


@collections.command(name="list")
@click.pass_context
def list_collections(ctx):
    try:
        click.echo(
            json.dumps(
                collections_client.list_collections(ctx.obj["collections-url"]),
                indent=4,
            )
        )
    except:
        click.secho(
            f"Error occurred while listing collections from collection [{ctx.obj['collections-url']}]",
            fg="red",
        )
        sys.exit(1)


@collections.command(name="query")
@click.pass_context
@click.argument("collection_name")
@click.argument("query")
@click.option(
    "-f",
    "--format",
    type=click.Choice(["json", "csv"]),
    show_choices=True,
    default="json",
    show_default=True,
)
def query_collection(ctx, collection_name, query, format="json"):
    try:
        click.echo(
            collections_client.query(
                ctx.obj["collections-url"],
                collection_name,
                query,
                format=format,
            )
        )
    except:
        click.secho(
            f"Error occurred while querying collection [{collection_name}] from collections-url [{ctx.obj['collections-url']}]",
            fg="red",
        )
        sys.exit(1)


collections.add_command(tables_commands.tables)
