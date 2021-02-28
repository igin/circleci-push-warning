import sys
import verify_circle_ci_status as testee
import pytest


def test_calls_should_push_with_git_url(mocker):
    should_push = mocker.patch.object(testee, 'should_push')
    git_url = "git@github.com:igin/some-test-repo.git"
    testargs = ["asdf", "asdf", git_url]
    mocker.patch.object(sys, 'argv', testargs)
    testee.main()
    should_push.assert_called_with(remote_url=git_url)


def test_exits_with_exit_code_1_if_should_push_returns_false(mocker):
    should_push = mocker.patch.object(testee, 'should_push')
    should_push.return_value = False
    git_url = "git@github.com:igin/some-test-repo.git"
    testargs = ["asdf", "asdf", git_url]
    mocker.patch.object(sys, 'argv', testargs)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        testee.main()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_shows_error_for_non_github_urls(capsys, mocker):
    git_url = "git@somewhere.com:igin/some-test-repo.git"
    testargs = ["asdf", "asdf", git_url]
    mocker.patch.object(sys, 'argv', testargs)
    testee.main()
    captured = capsys.readouterr()
    assert "Currently only github repos are supported" in captured.err
