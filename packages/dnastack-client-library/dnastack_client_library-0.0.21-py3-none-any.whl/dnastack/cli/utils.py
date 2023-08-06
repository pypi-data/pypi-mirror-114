import sys
import click
import yaml
from dnastack.constants import config_file_path, ACCEPTED_CONFIG_KEYS


# Getters
def get_config(ctx, var_name, val_type=None, do_assert=False):
    # assert that the config is there
    if do_assert:
        assert_config(ctx, var_name, val_type=val_type)

    return ctx.obj.get(var_name)


# Setters


def set_config(ctx, var_name: str, value):
    if type(value) == dict:
        ctx.obj[var_name] = {}
        for key, val in zip(value.keys(), value.values()):
            ctx.obj[var_name][key] = val

    set_configs(ctx, [var_name], [value])


def set_configs(ctx, var_names: list, values: list):
    for key, val in zip(var_names, values):
        ctx.obj[key] = val

    with open(config_file_path, "w") as config_file:
        yaml.dump(ctx.obj, config_file)


# Checks


def is_config_key(var_name):
    return var_name in ACCEPTED_CONFIG_KEYS


def has_config(ctx, var_name):
    return var_name in ctx.obj.keys() and ctx.obj[var_name]


def has_type(ctx, var_name, val_type):
    return type(ctx.obj[var_name]) == val_type if val_type is not None else True


# Assertions


def assert_config(ctx, var_name, val_type=None):
    assert_config_key(var_name)
    if not has_config(ctx, var_name):
        click.secho(
            f"The {var_name} configuration variable is not set. Run dnastack config set {var_name} [{var_name.upper()}] to configure it",
            fg="red",
        )
        sys.exit(1)
    elif not has_type(ctx, var_name, val_type):
        click.secho(
            f"The {var_name} configuration variable is not a {val_type.__name__} type. Run dnastack config set {var_name} [{var_name.upper()}] to reconfigure it",
            fg="red",
        )
        sys.exit(1)


def assert_config_key(key):
    if not is_config_key(key):
        click.secho(f"{key} is not an accepted configuration key.", fg="red")
        click.secho(f"Accepted configuration keys:", fg="red")
        for key in ACCEPTED_CONFIG_KEYS:
            click.secho(f"\t{key}", fg="red")
        sys.exit(1)
