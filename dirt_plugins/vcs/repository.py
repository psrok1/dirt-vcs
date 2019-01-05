import os
import git

"""
Here you can found all utilities needed to properly handle Git repository
"""


def get_gitignore_path(incident):
    return os.path.join(incident.dirpath, ".gitignore")


def get_repository(incident):
    try:
        return git.Repo(incident.dirpath)
    except git.InvalidGitRepositoryError:
        return git.Repo.init(incident.dirpath)


def uncommitted_files(incident):
    repo = get_repository(incident)
    return [item.a_path for item in repo.index.diff(None)] + repo.untracked_files


def commit(incident, message):
    repo = get_repository(incident)
    changes = uncommitted_files(incident)
    if not changes:
        return False
    repo.git.add(all=True)
    repo.git.commit(message=message)
    return True


def rollback(incident, commit=None):
    repo = get_repository(incident)
    repo.git.clean("-df")
    repo.head.reset(commit or "HEAD", index=True, working_tree=True)


def get_commits_list(incident):
    repo = get_repository(incident)
    return list(repo.iter_commits())
