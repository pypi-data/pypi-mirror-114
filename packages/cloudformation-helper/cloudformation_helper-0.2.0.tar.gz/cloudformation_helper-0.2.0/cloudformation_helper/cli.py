"""Console script for cloudformation_helper."""
import sys
import click

import cloudformation_helper.commands.deploy as deployModule
from cloudformation_helper.utils.config import read_config


@click.group()
@click.option("--config", default="stacks.cfh")
@click.pass_context
def cfhelper(ctx, config):
    ctx.obj = read_config(config)


@cfhelper.command()
@click.argument("stack_alias")
@click.pass_obj
def deploy(config, stack_alias):
    stack_name, stack_file, use_changesets, capabilities = config.get_stack(stack_alias)
    deployModule.deploy_or_update(stack_name, stack_file, use_changesets, capabilities)


def run():
    sys.exit(cfhelper(auto_envvar_prefix="CFHELPER"))  # pragma: no cover


if __name__ == "__main__":
    run()
