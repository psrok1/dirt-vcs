import click

from dirt.libs import log

from dirt_plugins.vcs.repository import get_repository


@click.command("log", help="List of commits")
@click.pass_context
def vcs_log_command(ctx):
    current = ctx.obj["INCIDENT"]
    repo = get_repository(current)
    log.echo(repo.git.log())


SUBCOMMAND = vcs_log_command
