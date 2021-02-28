import os
from verify_circle_ci_status import api_get_request, get_circle_ci_token, \
    http_client


def test_sets_token_header_from_env(mocker):
    test_token = 'testtoken'
    mocker.patch.dict(os.environ, {'PRE_PUSH_CIRCLE_CI_TOKEN': test_token})
    mocked_request = mocker.patch.object(http_client, 'HTTPSConnection')
    mocked_request.return_value.getresponse \
        .return_value.read \
        .return_value.decode.return_value = '{}'
    test_endpoint = 'some-endpoint/somewhere'
    api_get_request(endpoint=test_endpoint)
    mocked_request.return_value.request.assert_called_with(
        "GET", test_endpoint, headers={
            'Circle-Token': test_token
        })


def test_gets_token_from_env(mocker):
    testtoken = 'testtoken'
    mocker.patch.dict(os.environ, {'PRE_PUSH_CIRCLE_CI_TOKEN': testtoken})
    token = get_circle_ci_token()
    assert token == testtoken
