import click
import yaml
import os
from dnastack.cli import *
import dnastack
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context


def load_config_from_file(ctx):
    ctx.obj = {}

    # create the cli directory if necessary
    if not os.path.exists(cli_directory):
        os.mkdir(cli_directory)

    # create the config file if necessary
    if not os.path.exists(config_file_path):
        with open(config_file_path, "w+") as config_file:
            yaml.dump(ctx.obj, config_file)

    # create the downloads directory if necessary
    if not os.path.exists(downloads_directory):
        os.mkdir(downloads_directory)

    with open(config_file_path, "r+") as config_file:
        data = yaml.safe_load(config_file)
        if data:
            for key in data.keys():
                ctx.obj[key] = data[key]


@click.group()
def dnastack():
    load_config_from_file(click.get_current_context())


dnastack.add_command(dataconnect_commands.dataconnect)
dnastack.add_command(config_commands.config)
dnastack.add_command(file_commands.files)
dnastack.add_command(collections_commands.collections)

if __name__ == "__main__":
    dnastack.main(prog_name="dnastack")
