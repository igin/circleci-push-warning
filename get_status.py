#!/usr/bin/env python
import http.client
import json
from typing import Dict, Literal, Union

conn = http.client.HTTPSConnection("circleci.com")

API_TOKEN = 'TOKEN'

headers = {'Circle-Token': API_TOKEN}

PROJECT_SLUG = 'REPO_SLUG


def get_project_state(project_slug) -> Union[Literal['success'], Literal['error']]:
    pipelines = api_get_request(f"/api/v2/project/{project_slug}/pipeline")
    workflows = api_get_request(
        f"/api/v2/pipeline/{pipelines['items'][0]['id']}/workflow")

    last_workflow = workflows['items'][0]
    if last_workflow['status'] == 'success':
        return 'success'
    else:
        return 'error'


def api_get_request(endpoint) -> Dict:
    conn.request("GET", endpoint, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))


print(get_project_state(PROJECT_SLUG))
