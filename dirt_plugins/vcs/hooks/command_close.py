import click

from dirt.hooks import pre_hook, post_hook
from dirt.commands.close import close_command
from dirt.libs.log import warning, info
from dirt.libs.incident import choose_incident

from dirt_plugins.vcs import repository


@pre_hook(close_command)
def pre_hook_close_command(ctx, incident_id, *args, **kwargs):
    """
    Pre-hook on "dirt close" command.
    We need to be sure that all changes are committed before closing repository
    """
    incident = choose_incident(incident_id)
    if incident is None:
        return  # Let dirt handle it
    if not repository.uncommitted_files(incident):
        return
    warning("Uncommitted changes left in incident you want to close. They will be committed automatically")
    if not click.confirm("Are you sure?"):
        ctx.abort()


@post_hook(close_command)
def post_hook_close_command(ctx, *args, **kwargs):
    current = ctx.obj["INCIDENT"]
    repository.commit(current, message="Closed incident")
    info("Changes committed to repository")
