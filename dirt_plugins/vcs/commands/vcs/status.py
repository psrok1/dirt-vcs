import click

from dirt.libs import log

from dirt_plugins.vcs.repository import get_repository


@click.command("status", help="Get repository status")
@click.pass_context
def vcs_status_command(ctx):
    current = ctx.obj["INCIDENT"]
    repo = get_repository(current)
    log.echo(repo.git.status())


SUBCOMMAND = vcs_status_command
