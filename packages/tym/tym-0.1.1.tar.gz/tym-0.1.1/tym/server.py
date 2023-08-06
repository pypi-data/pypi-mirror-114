import base64
import pygit2
from typing import Set
import random
import asyncio
from multidict import MultiDictProxy
from aiohttp import web
import aiohttp_cors

import tym
from tym import constants
from tym.models import ServerError, RepoError
from tym.git_helpers import *
from tym.adapter import Adapter


routes = web.RouteTableDef()


def assert_params_exist(params: MultiDictProxy[str], expected_params: Set[str]):
    for p in expected_params:
        if p not in params:
            raise ServerError(f"Missing {p} parameter")


@routes.get("/")
async def is_alive(_) -> web.Response:
    return web.json_response({"alive": True})


@routes.get("/version")
async def get_tym_version(_) -> web.Response:
    return web.json_response({"version": tym.__version__})


@routes.get("/username")
async def get_username(request: web.BaseRequest) -> web.Response:
    adapter = request.app["adapter"]
    return web.json_response({"username": adapter.username})


@routes.get("/commit_file_content")
async def get_commit_file_content(request: web.BaseRequest) -> web.Response:
    try:
        repo = request.app["repo"]
        query_params = request.query
        assert_params_exist(query_params, {"commit_id", "file_name"})
        commit_id = query_params["commit_id"]
        file_name = query_params["file_name"]
        blob = get_file_blob(repo, commit_id, file_name)
        is_binary = False
        if blob == None:
            content = None
        elif blob.is_binary:
            content = base64.b64encode(blob.data).decode("utf8")
            is_binary = True
        else:
            content = blob.data.decode("utf8")
        return web.json_response({"content": content, "is_binary": is_binary})
    except ServerError as e:
        return web.json_response({"detail": str(e)}, status=400)
    except ValueError:
        return web.json_response({"detail": "Commit ID cannot be found."}, status=400)


@routes.get("/commit_file_tree")
async def get_commit_file_tree(request: web.BaseRequest) -> web.Response:
    try:
        repo = request.app["repo"]
        query_params = request.query
        assert_params_exist(query_params, {"commit_id"})
        commit_id = query_params["commit_id"]
        starting_dir = (
            query_params["starting_dir"] if "starting_dir" in query_params else ""
        )
        max_depth = query_params["max_depth"] if "max_depth" in query_params else 10
        tree = get_file_tree(repo, commit_id, starting_dir, max_depth)
        return web.json_response(tree)
    except ServerError as e:
        return web.json_response({"detail": str(e)}, status=400)
    except ValueError:
        return web.json_response({"detail": "Commit ID cannot be found."}, status=400)


@routes.get("/current_branch")
async def get_current_branch(request: web.BaseRequest) -> web.Response:
    repo = request.app["repo"]
    if repo.head_is_detached:
        return web.json_response({"branch_name": None, "detached": True})
    if repo.head_is_unborn:
        return web.json_response({"branch_name": None, "unborn": True})
    current_branch_name = ref_name_to_local_branch_name(repo.head.name)
    return web.json_response({"branch_name": current_branch_name})


@routes.post("/switch")
async def switch_branch(request: web.BaseRequest) -> web.Response:
    try:
        repo = request.app["repo"]
        adapter = request.app["adapter"]
        query_params = request.query
        assert_params_exist(query_params, {"branch"})
        next_branch_name = query_params["branch"]
        remote_name = (
            query_params["remote_name"] if "remote_name" in query_params else None
        )
        await tym_switch(repo, adapter, next_branch_name, remote_name)
        return web.json_response({"success": True})
    except ServerError as e:
        return web.json_response({"detail": str(e)}, status=400)
    except RepoError as e:
        return web.json_response(e.data, status=400)


@routes.get("/branches_maps")
async def get_branches_maps(request: web.BaseRequest) -> web.Response:
    repo = request.app["repo"]
    short_to_all, all_to_short = compute_branch_maps(repo)
    return web.json_response(
        {
            "short_to_all_branch_map": short_to_all,
            "all_branch_to_short_map": all_to_short,
        }
    )


@routes.get("/commits")
async def get_commits(request: web.BaseRequest) -> web.Response:
    try:
        repo = request.app["repo"]
        query_params = request.query
        assert_params_exist(query_params, {"branch", "exclusive_start_commit_id"})
        branch_name = query_params["branch"]
        exclusive_start_commit_id = query_params["exclusive_start_commit_id"]
        remote_name = query_params["remote"] if "remote" in query_params else None
        local_branch_name = (
            branch_name
            if remote_name == None
            else branch_name[len(remote_name + "/") :]
        )
        commits = None
        if is_local_shadow_branch_name(local_branch_name):
            commits = list_shadow_commits(repo, branch_name, exclusive_start_commit_id)
        else:
            commits = list_commits(repo, branch_name, exclusive_start_commit_id)
        return web.json_response(commits)
    except ServerError as e:
        return web.json_response({"detail": str(e)}, status=400)
    except RepoError as e:
        return web.json_response(e.data, status=400)


@routes.post("/jump")
async def shadow_branch_jump(request: web.BaseRequest) -> web.Response:
    try:
        repo = request.app["repo"]
        adapter = request.app["adapter"]
        query_params = request.query
        assert_params_exist(query_params, {"commit_id"})
        commit_id = query_params["commit_id"]
        await tym_jump(repo, adapter, commit_id)
        return web.json_response({"success": True})
    except ServerError as e:
        return web.json_response({"detail": str(e)}, status=400)
    except RepoError as e:
        return web.json_response(e.data, status=400)


def get_cors_config() -> dict:
    config = {}
    for origin in constants.ACCEPTED_ORIGINS:
        config[origin] = aiohttp_cors.ResourceOptions()
    return config


def create_app(adapter: Adapter, repo: pygit2.Repository) -> web.Application:
    app = web.Application()
    app["adapter"] = adapter
    app["repo"] = repo
    cors = aiohttp_cors.setup(app, defaults=get_cors_config())
    for route in app.add_routes(routes):
        cors.add(route)
    return app


def generate_random_port() -> int:
    return random.randint(constants.MIN_TCP_PORT_NUM, constants.MAX_TCP_PORT_NUM)
