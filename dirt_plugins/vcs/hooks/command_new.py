from dirt.hooks import post_hook
from dirt.commands.new import new_command
from dirt.libs.log import info

from dirt_plugins.vcs import repository


@post_hook(new_command)
def hook_new_command(ctx, *args, **kwargs):
    """
    Post-hook on "dirt new" command.
    We want to create repository now and notify user about it
    """
    incident = ctx.obj["INCIDENT"]
    repository.get_repository(incident)
    incident.store()
    repository.commit(incident, "Initial commit")
    info("Created new git repository.")
