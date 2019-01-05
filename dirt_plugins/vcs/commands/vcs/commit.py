import click

from dirt.libs import log

from dirt_plugins.vcs import repository


@click.command("commit", help="Commit all changes")
@click.option("--message", "-m", default=None)
@click.pass_context
def vcs_commit_command(ctx, message):
    current = ctx.obj["INCIDENT"]
    changes = repository.uncommitted_files(current)
    default_message = "(empty)"

    if not changes:
        log.error("No pending changes!")
        ctx.abort()

    if not message:
        if not log.QUIET_MODE:
            log.warning("Empty commit message. Please provide commit description.")
            message = click.prompt("Description:", default=default_message)
        else:
            message = default_message

    repository.commit(current, message)

    log.echo("Changed files:", ignore_short=True)
    for path in changes:
        log.echo("* {path}", path=path, ignore_short=True)

    log.success("Changes committed successfully!")


SUBCOMMAND = vcs_commit_command
