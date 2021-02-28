import verify_circle_ci_status as testee


def test_returns_false_with_failed_build_and_user_saying_no(mocker):
    test_remote_url = 'git@github.com:owner/repo.git'
    mocker.patch.object(testee, 'get_project_state',
                        return_value=testee.ProjectState(
                            build_in_progress=False,
                            last_finished_build_state='error'
                        ))
    mocker.patch('builtins.input', return_value='n')
    assert not testee.should_push(remote_url=test_remote_url)


def test_returns_true_with_failed_build_and_user_saying_yes(mocker):
    test_remote_url = 'git@github.com:owner/repo.git'
    mocker.patch.object(testee, 'get_project_state',
                        return_value=testee.ProjectState(
                            build_in_progress=False,
                            last_finished_build_state='error'
                        ))
    mocker.patch('builtins.input', return_value='y')
    assert testee.should_push(remote_url=test_remote_url)


def test_returns_false_with_build_in_progress_and_user_saying_no(mocker):
    test_remote_url = 'git@github.com:owner/repo.git'
    mocker.patch.object(testee, 'get_project_state',
                        return_value=testee.ProjectState(
                            build_in_progress=False,
                            last_finished_build_state='error'
                        ))
    mocker.patch('builtins.input', return_value='n')
    assert not testee.should_push(remote_url=test_remote_url)


def test_returns_true_with_build_in_progress_and_user_saying_yes(mocker):
    test_remote_url = 'git@github.com:owner/repo.git'
    mocker.patch.object(testee, 'get_project_state',
                        return_value=testee.ProjectState(
                            build_in_progress=False,
                            last_finished_build_state='error'
                        ))
    mocker.patch('builtins.input', return_value='n')
    assert not testee.should_push(remote_url=test_remote_url)
