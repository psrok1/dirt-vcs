import click

from dirt.libs import log

from dirt_plugins.vcs import repository


@click.command("rollback", help="Rollback all pending or committed changes from specified point")
@click.option("--commit", "-c", default=None)
@click.pass_context
def vcs_rollback_command(ctx, commit):
    current = ctx.obj["INCIDENT"]

    # Store tags and relations before rollback
    previous_tags = set(current.tags)
    previous_relations = set(current.meta.get("relations", set()))

    repository.rollback(current, commit)
    current.load()

    # Store state after rollback and recover temporarily
    current_tags = set(current.tags)
    current_relations = set(current.meta.get("relations", set()))
    current.tags = previous_tags
    current.meta["relations"] = previous_relations

    for added_tag in current_tags.difference(previous_tags):
        log.info("ROLLBACK: Added tag #{}".format(added_tag))
        current.add_tag(added_tag)
    for removed_tag in previous_tags.difference(current_tags):
        log.info("ROLLBACK: Removed tag #{}".format(removed_tag))
        current.add_tag(removed_tag)

    for added_relation in current_relations.difference(previous_relations):
        log.info("ROLLBACK: Added relation with {}".format(added_relation))
        current.add_relation(added_relation)
    for removed_relation in previous_relations.difference(current_relations):
        log.info("ROLLBACK: Removed relation with {}".format(removed_relation))
        current.remove_relation(removed_relation)

    # Reload once again (not necessary, but left in case of further changes)
    current.load()
    log.success("Rollbacked successfully!")


SUBCOMMAND = vcs_rollback_command
