from tym.commons import typer_error
from typing import List
import typer
import pygit2
from pathlib import Path
from aiohttp import web
from asyncio import Task

from tym.adapter import Adapter
from tym.commons import schedule_periodic_function
from tym.server import create_app, generate_random_port
from tym.git_helpers import *


async def start(adapter: Adapter):
    repo_path = Path(pygit2.discover_repository("."))
    repo = pygit2.Repository(repo_path)
    tasks: List[Task] = []
    # Step - Setup http servers
    #   setup all APIs
    app = create_app(adapter, repo)
    runner = web.AppRunner(app)
    await runner.setup()
    port = None
    while True:
        port = generate_random_port()
        site = web.TCPSite(runner, "localhost", port)
        try:
            await site.start()
            typer.launch(f"{constants.LAUNCH_HOSTNAME}/repo/{adapter.repo.id}")
            break
        except OSError:
            pass
    tasks.append(asyncio.create_task(adapter.update_repo_client(port)))

    # Fetch regularly
    tasks.append(
        asyncio.create_task(
            schedule_periodic_function(60, run_command, "git fetch --all")
        )
    )
    # Update repo client so it knows that CLI is active
    tasks.append(
        asyncio.create_task(schedule_periodic_function(60, adapter.update_repo_client))
    )
    #   TODO: Clean up (merged branches etc...)

    # check if initial workspace has changes
    await tym_save(repo, adapter)
    # watch for changes in workspace
    tasks.append(asyncio.create_task(watch_for_changes(repo, adapter)))

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        pass
    except Exception as e:
        typer_error(str(e))
        raise e
    finally:
        print("\nTerminating tym and freeing up resources... ", end="", flush=True)
        for task in tasks:
            task.cancel()
        clean_up_tasks: List[Task] = []
        clean_up_tasks.append(asyncio.create_task(runner.cleanup()))
        clean_up_tasks.append(asyncio.create_task(adapter.update_repo_client(-1)))
        await asyncio.gather(*clean_up_tasks, return_exceptions=True)
        typer.secho("Done", fg=typer.colors.GREEN)
        typer.echo("Goodbye!")
