from collections import defaultdict
from pathlib import Path
import shutil
from typing import Tuple, Iterator, List, Optional, Union, Dict
import subprocess
import asyncio
from asyncio import Task
import pygit2
from datetime import datetime
from watchgod import awatch
import typer

from tym import constants
from tym.models import RepoError
from tym.adapter import Adapter


def has_git() -> bool:
    result = subprocess.run(
        ["git", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return result.returncode == 0


def has_set_git_config_name() -> bool:
    result = subprocess.run(
        ["git", "config", "user.name"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def has_set_git_config_email() -> bool:
    result = subprocess.run(
        ["git", "config", "user.email"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


async def run_command(cmd) -> Tuple[int, bytes, bytes]:
    # Given command, returns returncode, stdout, and stderr
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()
    return proc.returncode, stdout, stderr


def loop_through_remotes(
    tym_remotes: List[str], repo_remotes: pygit2.remote.RemoteCollection
) -> Iterator[str]:
    for tym_remote_name in tym_remotes:
        try:
            repo_remotes[tym_remote_name]
            yield tym_remote_name
        except KeyError:
            raise RepoError(
                {
                    "detail": f"Your configured tym remote <{tym_remote_name}> cannot be found in the remotes list."
                }
            )


def is_local_shadow_branch_name(local_branch_name: str) -> bool:
    branch_name_split = local_branch_name.split("/")
    if len(branch_name_split) < 2:
        return False
    return branch_name_split[1] == constants.SHADOW_BRANCH_PREFIX


def ref_name_to_local_branch_name(ref_name: str) -> str:
    local_branch_name = ref_name
    if ref_name.startswith(constants.REFS_HEAD_PREFIX):
        local_branch_name = ref_name[len(constants.REFS_HEAD_PREFIX) :]
    return local_branch_name


def local_branch_name_to_ref_name(local_branch_name: str) -> str:
    return constants.REFS_HEAD_PREFIX + local_branch_name


def local_branch_name_to_shadow_branch_name(
    local_branch_name: str, username: str
) -> str:
    return f"{username}/{constants.SHADOW_BRANCH_PREFIX}/{local_branch_name}"


def split_shadow_branch_name(shadow_branch_name: str) -> Tuple[str]:
    shadow_branch_name_parts = shadow_branch_name.split("/")
    if len(shadow_branch_name_parts) < 2:
        return "", shadow_branch_name
    username, _, *branch_name_parts = shadow_branch_name_parts
    return username, "/".join(branch_name_parts)


def create_shadow_branch(
    repo: pygit2.Repository, current_branch: pygit2.Branch, adapter: Adapter
) -> Tuple[pygit2.Branch, List[Task]]:
    shadow_branch_name = local_branch_name_to_shadow_branch_name(
        current_branch.branch_name, adapter.username
    )
    base_commit = repo.get(current_branch.target)
    shadow_branch = repo.branches.local.create(shadow_branch_name, base_commit)
    # Create first commit for shadow branch - points to the same tree
    commit_message = constants.SHADOW_BRANCH_INITIAL_COMMIT_MESSAGE
    user = repo.default_signature
    tree = base_commit.tree.oid
    parents = [base_commit.oid]
    repo.create_commit(
        local_branch_name_to_ref_name(shadow_branch_name),
        user,
        user,
        commit_message,
        tree,
        parents,
    )
    # Update shadow branch to contain the latest commit
    shadow_branch = repo.branches.local.get(shadow_branch.branch_name)
    tasks = []
    tasks.append(asyncio.create_task(adapter.create_branch(shadow_branch_name)))
    for tym_remote in loop_through_remotes(adapter.repo.tym_remotes, repo.remotes):
        tasks.append(
            asyncio.create_task(
                run_command(f"git push {tym_remote} {shadow_branch_name}")
            )
        )
    return shadow_branch, tasks


def save_changes_to_shadow_branch(
    repo: pygit2.Repository,
    adapter: Adapter,
    current_branch: pygit2.Branch,
    shadow_branch: pygit2.Branch,
    print_message: bool = False,
    commit_message: str = "",
) -> List[Task]:
    if (
        len(repo.diff(shadow_branch.target, flags=pygit2.GIT_DIFF_INCLUDE_UNTRACKED))
        == 0
    ):
        return []
    if print_message:
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"{current_time} - Changes detected. Syncing... ", end="", flush=True)
    # Commit changes to shadow branch tip
    shadow_branch_name = shadow_branch.branch_name
    shadow_branch_ref_name = shadow_branch.name
    commit_message = constants.SHADOW_COMMIT_MESSAGE_PREFIX + commit_message
    index = repo.index
    index.add_all()
    tree = index.write_tree()
    user = repo.default_signature
    parents = [shadow_branch.target]
    base_oid = repo.merge_base(current_branch.target, shadow_branch.target)
    if base_oid != current_branch.target:
        parents.append(current_branch.target)
    repo.create_commit(
        shadow_branch_ref_name, user, user, commit_message, tree, parents
    )
    # Push notify firestore of changes + push
    tasks = []
    tasks.append(asyncio.create_task(adapter.update_branch(shadow_branch_name)))
    for tym_remote in loop_through_remotes(adapter.repo.tym_remotes, repo.remotes):
        tasks.append(
            asyncio.create_task(
                run_command(f"git push {tym_remote} {shadow_branch_name}")
            )
        )
    return tasks


async def tym_save(repo: pygit2.Repository, adapter: Adapter):
    # Leave HEAD is detached OR HEAD is unborn
    current_time = datetime.now().strftime("%H:%M:%S")
    if repo.head_is_detached or repo.head_is_unborn:
        typer.echo(
            f"{current_time} - Tym will not save state because HEAD is detached."
        )
        return
    # Leave if git is on a shadow branch
    current_branch_name = ref_name_to_local_branch_name(repo.head.name)
    current_branch = repo.branches.local.get(current_branch_name)
    if current_branch == None or not current_branch.is_head():
        raise RepoError(
            {
                "detail": f"Current branch of name <{current_branch_name}> is None or is not head."
            }
        )
    if is_local_shadow_branch_name(current_branch_name):
        typer.echo(
            f"{current_time} - Tym will not save state because you are on a shadow branch."
        )
        return
    # Get or create shadow branch
    shadow_branch_name = local_branch_name_to_shadow_branch_name(
        current_branch_name, adapter.username
    )
    shadow_branch = repo.branches.local.get(shadow_branch_name)
    # Save current workspace state to shadow branch
    tasks: List[Task] = []
    if shadow_branch == None:
        shadow_branch, creation_tasks = create_shadow_branch(
            repo, current_branch, adapter
        )
        tasks += creation_tasks
    else:
        await asyncio.sleep(0.1)
    new_tasks = save_changes_to_shadow_branch(
        repo, adapter, current_branch, shadow_branch, True
    )
    tasks += new_tasks
    # TODO: Allow tym to queue push requests so they are not blocked
    await asyncio.gather(*tasks, return_exceptions=True)
    if len(new_tasks) > 0:
        typer.secho("Done", fg=typer.colors.GREEN)


async def watch_for_changes(repo: pygit2.Repository, adapter: Adapter):
    async for _ in awatch(repo.workdir, normal_sleep=600):
        if adapter.run_watcher:
            try:
                await tym_save(repo, adapter)
            except KeyError as e:
                typer.echo(
                    f"Watcher faced a Key Error <{e}>. Tym will continue to function."
                )
            except Exception as e:
                typer.echo(
                    f"Watcher faced an exception <{e}>. Tym should continue to function but we recommend that you restart Tym. Sorry!"
                )


def get_file_blob(
    repo: pygit2.Repository, commit_id: str, full_file_name: str
) -> Optional[pygit2.Blob]:
    commit = repo.get(commit_id)
    try:
        git_obj = commit.tree[full_file_name]
        if git_obj.type_str == "tree":
            return None
        return git_obj
    except KeyError:
        return None


def get_file_tree_helper(tree: pygit2.Tree, max_depth: int) -> Union[dict, int]:
    if max_depth == 0:
        return 0
    file_tree = {}
    for obj in tree:
        if obj.type_str == "tree":
            file_tree[obj.name] = get_file_tree_helper(obj, max_depth - 1)
        if obj.type_str == "blob":
            file_tree[obj.name] = 1
    return file_tree


def get_file_tree(
    repo: pygit2.Repository, commit_id: str, starting_dir: str, max_depth: int
) -> Optional[dict]:
    """
    Create a file tree where 1 is a file while 0 is an unfilled directory
    """
    commit = repo.get(commit_id)
    starting_tree = commit.tree
    if len(starting_dir) > 0:
        try:
            starting_tree = starting_tree[starting_dir]
        except KeyError:
            return None
    file_tree = get_file_tree_helper(starting_tree, max_depth)
    return file_tree


def remove_file_or_dir(path: Path):
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(str(path), ignore_errors=True)
    if path.is_file():
        path.unlink()


def compute_branch_maps(
    repo: pygit2.Repository,
) -> Tuple[Dict[str, List[dict]], Dict[str, dict]]:
    short_to_all = defaultdict(list)
    all_to_short = {}
    for branch_name in repo.branches.local:
        if is_local_shadow_branch_name(branch_name):
            shadow_username, local_branch_name = split_shadow_branch_name(branch_name)
            branch_info = {
                "short_name": local_branch_name,
                "full_name": branch_name,
                "remote_name": None,
                "shadow_username": shadow_username,
            }
            short_to_all[local_branch_name].append(branch_info)
            all_to_short[branch_name] = branch_info
        else:
            branch_info = {
                "short_name": branch_name,
                "full_name": branch_name,
                "remote_name": None,
                "shadow_username": None,
            }
            short_to_all[branch_name].append(branch_info)
            all_to_short[branch_name] = branch_info
    for remote_branch_name in repo.branches.remote:
        remote_branch = repo.branches.remote.get(remote_branch_name)
        remote_name = remote_branch.remote_name
        branch_name = remote_branch_name[len(remote_name + "/") :]
        if is_local_shadow_branch_name(branch_name):
            shadow_username, local_branch_name = split_shadow_branch_name(branch_name)
            branch_info = {
                "short_name": local_branch_name,
                "full_name": remote_branch_name,
                "remote_name": remote_name,
                "shadow_username": shadow_username,
            }
            short_to_all[local_branch_name].append(branch_info)
            all_to_short[remote_branch_name] = branch_info
        else:
            branch_info = {
                "short_name": branch_name,
                "full_name": remote_branch_name,
                "remote_name": remote_name,
                "shadow_username": None,
            }
            short_to_all[branch_name].append(branch_info)
            all_to_short[remote_branch_name] = branch_info
    return short_to_all, all_to_short


def create_local_branch_from_remote_branch(
    repo: pygit2.Repository, remote_branch_name: str, remote_name: str
) -> pygit2.Branch:
    local_branch_name = remote_branch_name[len(remote_name) :]
    remote_branch = repo.branches.remote.get(remote_branch_name)
    next_branch_commit = repo.get(remote_branch.target)
    next_branch = repo.branches.local.create(local_branch_name, next_branch_commit)
    next_branch.upstream = remote_branch
    return next_branch


async def tym_switch(
    repo: pygit2.Repository,
    adapter: Adapter,
    next_branch_name: str,
    remote_name: Optional[str] = None,
):
    # Check if next branch is valid
    if next_branch_name not in repo.branches:
        error_message = (
            f"Cannot switch to branch <{next_branch_name}> because it cannot be found."
        )
        typer.echo(error_message)
        raise RepoError({"detail": error_message})

    next_branch = repo.branches.local.get(next_branch_name)
    if next_branch == None:
        if remote_name == None:
            error_message = f"Cannot switch to branch <{next_branch_name}> because it is a remote but remote name is not provided."
            typer.echo(error_message)
            raise RepoError({"detail": error_message})
        next_branch = create_local_branch_from_remote_branch(
            repo, next_branch_name, remote_name
        )

    current_branch_name = ref_name_to_local_branch_name(repo.head.name)
    if (
        repo.head_is_detached
        or repo.head_is_unborn
        or is_local_shadow_branch_name(current_branch_name)
    ):
        # repo not in a valid branch BUT does not have uncommitted changes,
        # then we can still perform the switch
        if len(repo.diff("HEAD", flags=pygit2.GIT_DIFF_INCLUDE_UNTRACKED)) > 0:
            error_message = "Cannot switch branch since there are uncommitted changes that are not tracked by Tym."
            typer.echo(error_message)
            raise RepoError({"detail": error_message})
    else:
        # Save all uncommitted changes into the shadow branch and stop the watcher
        # Then clear all uncommitted changes (including untracked) and then perform a checkout
        adapter.run_watcher = False
        await tym_save(repo, adapter)
        repo.reset(repo.head.target, pygit2.GIT_RESET_HARD)
        diff = repo.diff(repo.head.target, flags=pygit2.GIT_DIFF_INCLUDE_UNTRACKED)
        # Clear untracked files
        repo_workdir = Path(repo.workdir)
        for patch in diff:
            if patch.delta.old_file.size > 0:
                continue
            file_path = repo_workdir / patch.delta.new_file.path
            remove_file_or_dir(file_path)
    # Check out to next branch
    next_ref = repo.lookup_reference(next_branch.name)
    repo.checkout(next_ref)
    # If shadow branch for next branch exists, then set the workspace to be that workspace
    next_shadow_branch_name = local_branch_name_to_shadow_branch_name(
        next_branch.branch_name, adapter.username
    )
    next_shadow_branch = repo.branches.local.get(next_shadow_branch_name)
    if next_shadow_branch != None:
        original_oid = repo.head.target
        repo.reset(next_shadow_branch.target, pygit2.GIT_RESET_HARD)
        repo.reset(original_oid, pygit2.GIT_RESET_MIXED)
    # Resume watcher
    adapter.run_watcher = True


async def tym_jump(repo: pygit2.Repository, adapter: Adapter, commit_id: str):
    if repo.head_is_detached or repo.head_is_unborn:
        error_message = f"Cannot jump because HEAD is detached."
        typer.echo(error_message)
        raise RepoError({"detail": error_message})
    current_branch_name = ref_name_to_local_branch_name(repo.head.name)
    current_branch = repo.branches.local.get(current_branch_name)
    shadow_branch_name = local_branch_name_to_shadow_branch_name(
        current_branch_name, adapter.username
    )
    shadow_branch = repo.branches.local.get(shadow_branch_name)
    if is_local_shadow_branch_name(current_branch_name) or shadow_branch == None:
        error_message = (
            f"Cannot jump because current branch does not have a shadow branch."
        )
        typer.echo(error_message)
        raise RepoError({"detail": error_message})
    # Check if commit is valid
    try:
        commit = repo.get(commit_id)
        if commit == None or commit.type_str != "commit":
            raise ValueError
    except ValueError:
        error_message = (
            f"Cannot jump to commit <{commit_id}> because it cannot be found."
        )
        typer.echo(error_message)
        raise RepoError({"detail": error_message})
    # Perform jump
    original_oid = repo.head.target
    repo.reset(commit.oid, pygit2.GIT_RESET_HARD)
    repo.reset(original_oid, pygit2.GIT_RESET_MIXED)
    # Save changes if any
    commit_message = f" jump {commit_id}"
    tasks = save_changes_to_shadow_branch(
        repo, adapter, current_branch, shadow_branch, commit_message=commit_message
    )
    asyncio.gather(*tasks)


def list_shadow_commits(
    repo: pygit2.Repository, branch_name: str, exclusive_start_commit_id: Optional[str]
) -> List[dict]:
    shadow_branch = repo.branches.get(branch_name)
    if shadow_branch == None:
        return []
    walker = repo.walk(shadow_branch.target)
    walker.simplify_first_parent()
    commits_list = []
    for commit in walker:
        if exclusive_start_commit_id == str(commit.oid):
            break
        message = commit.message
        is_initial_commit = message == constants.SHADOW_BRANCH_INITIAL_COMMIT_MESSAGE
        parent_ids = [str(parent_id) for parent_id in commit.parent_ids]
        shadow_parent_id = None
        official_parent_id = None
        if is_initial_commit:
            official_parent_id = parent_ids[0]
        else:
            shadow_parent_id = parent_ids[0]
            if len(commit.parent_ids) == 2:
                official_parent_id = parent_ids[1]
        shadow_commit = {
            "id": str(commit.oid),
            "message": message,
            "author": commit.author.name,
            "timestamp": commit.commit_time,
            "parent_ids": parent_ids,
            "shadow_parent_id": shadow_parent_id,
            "official_parent_id": official_parent_id,
        }
        commits_list.append(shadow_commit)
        if is_initial_commit:
            break
    commits_list.reverse()
    return commits_list


def list_commits(
    repo: pygit2.Repository, branch_name: str, exclusive_start_commit_id: Optional[str]
) -> List[dict]:
    branch = repo.branches.get(branch_name)
    if branch == None:
        return []
    walker = repo.walk(branch.target)
    walker.simplify_first_parent()
    commits_list = []
    for commit in walker:
        if exclusive_start_commit_id == str(commit.oid):
            break
        parent_ids = [str(parent_id) for parent_id in commit.parent_ids]
        repo_commit = {
            "id": str(commit.oid),
            "message": commit.message,
            "author": commit.author.name,
            "timestamp": commit.commit_time,
            "parent_ids": parent_ids,
        }
        commits_list.append(repo_commit)
    commits_list.reverse()
    return commits_list
