import os

import click

from dirt.libs import log


@click.command("ignore", help="Modify list of untracked files (.gitignore)")
@click.pass_context
def vcs_ignore_command(ctx):
    current = ctx.obj["INCIDENT"]
    readme_path = os.path.join(current.dirpath, ".gitignore")
    click.edit(filename=readme_path)
    log.success("Note successfully saved in {path}", path=readme_path)


SUBCOMMAND = vcs_ignore_command
