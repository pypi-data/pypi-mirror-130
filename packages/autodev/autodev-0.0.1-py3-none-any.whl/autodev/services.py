"""Gather all the orchestration functionality required by the program to work.

Classes and functions that connect the different domain model objects with the adapters
and handlers to achieve the program's purpose.
"""

import json
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Tuple

from repository_orm import Repository

from .model import GitRepository

if TYPE_CHECKING:
    from .adapters.abstract import GitServers


def get_file_path(
    filename: str, starting_path: Optional[Path] = None
) -> Optional[Path]:
    """Search for a file by traversing up the tree from a path.

    Args:
        filename: the name of the file to search for
        starting_path: an optional path from which to start searching

    Returns:
        The `Path` to the file if it exists or `None` if it doesn't
    """
    start = starting_path or Path.cwd()

    for path in [start, *start.parents]:
        file_path = path / filename
        if file_path.is_file():
            return file_path

    return None


def get_cruft_template(cruft_file: Path) -> Tuple[str, str]:
    """Get the cruft template repository url and current commit."""
    with open(cruft_file, "r") as file_descriptor:
        cruft_data = json.loads(file_descriptor.read())

    return cruft_data["template"], cruft_data["commit"]


def update_git_repositories(repo: Repository, adapters: "GitServers") -> None:
    """Update the information of the monitored git repositories."""
    update_git_repo_workflows(repo, adapters)


def update_git_repo_workflows(repo: Repository, adapters: "GitServers") -> None:
    """Update the workflows of the workflow monitored git repositories."""
    git_repos = repo.search({"monitor_workflows": True}, [GitRepository])
    for git_repo in git_repos:
        adapter = adapters[git_repo.provider_id]
        workflows = adapter.get_repo_workflows(git_repo)
        for workflow in workflows:
            workflow = repo.add(workflow)  # sets the id_
            workflow_runs = adapter.get_workflow_runs(workflow)
            for workflow_run in workflow_runs:
                repo.add(workflow_run)
            workflow.update_state(workflow_runs)
            repo.add(workflow)
        git_repo.update_state(workflows)
        repo.add(git_repo)
        repo.commit()
