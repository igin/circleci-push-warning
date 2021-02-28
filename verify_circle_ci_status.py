#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from typing import Dict, Literal
import http.client as http_client
import json
import os


def main():
    origin_url = sys.argv[2]
    try:
        if not should_push(remote_url=origin_url):
            exit(1)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)


def should_push(*, remote_url: str) -> bool:
    print(f"Checking status of remote: {remote_url}")
    origin = parse_project_from_url(origin_url=remote_url)
    print(f"Owner: {origin.owner}; Repo: {origin.repo_name}")
    state = get_project_state(project=origin)
    state.print()
    if state.build_in_progress or state.last_finished_build_state != 'success':
        should_continue = input('Would you like to continue the push? (y/n)')
        if should_continue.lower().strip() != 'y':
            print('Aborting push.')
            return False

    print('Push will continue.')
    return True


@dataclass
class CircleCIProject:
    owner: str
    repo_name: str


GITHUB_HTTPS_PREFIX = 'https://github.com/'
GITHUB_GIT_PREFIX = 'git@github.com:'


def parse_project_from_url(*, origin_url: str) -> CircleCIProject:
    if origin_url.startswith(GITHUB_HTTPS_PREFIX):
        path = origin_url.removeprefix(GITHUB_HTTPS_PREFIX)
    elif origin_url.startswith(GITHUB_GIT_PREFIX):
        path = origin_url.removeprefix(GITHUB_GIT_PREFIX)
    else:
        raise ValueError("Currently only github repos are supported")

    parts = path.split('/')
    owner = parts[0]
    repo_name = '/'.join(parts[1:]).removesuffix('.git')
    return CircleCIProject(owner=owner, repo_name=repo_name)


@dataclass
class ProjectState:
    build_in_progress: bool
    last_finished_build_state: Literal['success', 'error', 'canceled']

    def print(self):
        print("Project State:")
        if self.build_in_progress:
            print("Build is currently in progress.")
        else:
            print("No build is currently in progress.")
        print(f"Last finished build state: {self.last_finished_build_state}")


def get_project_state(*, project: CircleCIProject) -> ProjectState:
    pipelines = api_get_request(
        endpoint=f"/api/v2/project/gh/{project.owner}/"
        f"{project.repo_name}/pipeline")
    workflows = api_get_request(
        endpoint=f"/api/v2/pipeline/{pipelines['items'][0]['id']}/workflow")

    last_workflow = workflows['items'][0]
    last_build_status = last_workflow['status']
    return ProjectState(
        build_in_progress=False,
        last_finished_build_state=last_build_status
    )


CIRCLECI_HOST = "circleci.com"


def api_get_request(*, endpoint) -> Dict:
    conn = http_client.HTTPSConnection(CIRCLECI_HOST)
    headers = {'Circle-Token': get_circle_ci_token()}
    conn.request("GET", endpoint, headers=headers)
    res = conn.getresponse()
    try:
        data = res.read()
        return json.loads(data.decode("utf-8"))
    except Exception as e:
        raise RuntimeError(
            f"Failure to parse response for request: {endpoint}, "
            f"Error: {str(e)}")


TOKEN_ENV_VARIABLE = 'PRE_PUSH_CIRCLE_CI_TOKEN'


def get_circle_ci_token():
    return os.environ.get(TOKEN_ENV_VARIABLE)


if __name__ == '__main__':
    main()
