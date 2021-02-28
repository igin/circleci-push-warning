from typing import Any, Dict, Literal, Protocol
import verify_circle_ci_status as testee


def test_returns_success_if_last_pipeline_was_successful(mocker):
    project = testee.CircleCIProject(
        owner='someowner', repo_name='someproject')
    setup_ci_api(mocker=mocker,
                 project=project,
                 last_pipeline_state='success')
    project_state = testee.get_project_state(
        project=project)
    assert project_state.last_finished_build_state == 'success'


def test_returns_error_if_last_pipeline_had_error(mocker):
    project = testee.CircleCIProject(
        owner='someowner', repo_name='someproject')
    setup_ci_api(mocker=mocker,
                 project=project,
                 last_pipeline_state='error')
    project_state = testee.get_project_state(
        project=project)
    assert project_state.last_finished_build_state == 'error'


def setup_ci_api(*,
                 mocker,
                 project: testee.CircleCIProject,
                 last_pipeline_state: Literal['success', 'error']):
    project_slug = f'gh/{project.owner}/{project.repo_name}'
    pipeline_id = "497f6eca-6276-4993-bfeb-53cbbbba6f08"
    mocker.patch.object(testee, 'api_get_request', side_effect=fake_get({
        f'/api/v2/project/{project_slug}/pipeline': {
            "items": [
                {
                    "id": pipeline_id,
                    "errors": [],
                    "project_slug": project_slug,
                    "updated_at": "2019-08-24T14:15:22Z",
                    "number": 0,
                    "state": "created",
                    "created_at": "2019-08-24T14:15:22Z",
                    "trigger": {},
                    "vcs": {}
                }
            ],
        },
        f'/api/v2/pipeline/{pipeline_id}/workflow': {
            "items": [
                {
                    "pipeline_id": pipeline_id,
                    "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
                    "name": "build-and-test",
                    "project_slug": project_slug,
                    "errored_by": "c6e40f70-a80a-4ccc-af88-8d985a7bc622",
                    "tag": "setup",
                    "status": last_pipeline_state,
                    "started_by": "03987f6a-4c27-4dc1-b6ab-c7e83bb3e713",
                    "pipeline_number": 0,
                    "created_at": "2019-08-24T14:15:22Z",
                    "stopped_at": "2019-08-24T14:15:22Z"
                }
            ],
        }
    }))


class ApiGetRequestHandler(Protocol):
    def __call__(self, *, endpoint: str) -> Dict: ...


def fake_get(result_map: Dict[str, Any]) -> ApiGetRequestHandler:
    def get(*, endpoint: str) -> Dict:
        return result_map.get(endpoint, None)

    return get
