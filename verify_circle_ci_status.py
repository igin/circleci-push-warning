#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from typing import Dict, Iterator, List, Literal, Optional
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
    last_finished_build_state: Literal[
        "success", "running", "not_run", "failed",
        "error", "failing", "on_hold", "canceled", "unauthorized"]

    def print(self):
        print("Project State:")
        if self.build_in_progress:
            print("Build is currently in progress.")
        else:
            print("No build is currently in progress.")
        print(f"Last finished build state: {self.last_finished_build_state}")


def get_project_state(*, project: CircleCIProject) -> ProjectState:
    project_workflows = get_project_workflows(project=project)
    running_workflow = None
    last_finished_workflow = None
    for workflow in project_workflows:
        if workflow.state == 'running' or workflow.state == 'failing':
            running_workflow = workflow
        elif workflow.state != 'canceled':
            last_finished_workflow = workflow
            break

    project_state = last_finished_workflow.state if last_finished_workflow \
        else 'error'

    return ProjectState(
        build_in_progress=running_workflow is not None,
        last_finished_build_state=project_state)


@dataclass
class WorkflowState:
    state: Literal["success", "running", "not_run", "failed",
                   "error", "failing", "on_hold", "canceled", "unauthorized"]


def get_project_workflows(*, project: CircleCIProject) -> Iterator[
        WorkflowState]:
    pipelines = api_get_request(
        endpoint=f"/api/v2/project/gh/{project.owner}/"
        f"{project.repo_name}/pipeline")

    for pipeline in pipelines['items']:
        pipeline_workflows = get_pipeline_workflows(pipeline=pipeline)
        for workflow in pipeline_workflows:
            yield workflow


def get_pipeline_workflows(*, pipeline) -> List[WorkflowState]:
    pipeline_id = pipeline['id']
    workflows = api_get_request(
        endpoint=f"/api/v2/pipeline/{pipeline_id}/workflow")
    workflow_states = [
        WorkflowState(state=workflow['status'])
        for workflow in workflows['items']
    ]
    return workflow_states


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
