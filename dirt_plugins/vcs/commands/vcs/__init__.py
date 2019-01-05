import click

from dirt.libs import extensions, incident, log

import sys
current_module = sys.modules[__name__]


@click.group("vcs", help="Incident version control")
@click.option("--incident_id", "-i", default="current")
@click.pass_context
def vcs_command(ctx, incident_id):
    """
    Here we're adding new command to dirt - vcs
    """
    current = incident.choose_incident(incident_id)
    if current is None:
        log.error("No incident found.")
        ctx.abort()
    ctx.obj["INCIDENT"] = current


# Our new command has also some subcommands
extensions.register_subcommands(vcs_command, [current_module], "SUBCOMMAND")


COMMAND = vcs_command
