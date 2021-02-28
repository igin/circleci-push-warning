from verify_circle_ci_status import main
import sys
import os


def test_verify(mocker):
    git_url = "git@github.com:onlinedoctor-ch/management-ui.git"
    testargs = ["asdf", "asdf", git_url]
    mocker.patch.object(sys, 'argv', testargs)
    mocker.patch.dict(os.environ, {
                      'PRE_PUSH_CIRCLE_CI_TOKEN': 'df5ed9cab7132aee5b2282ba97764c4e3c16da7d'})
    main()
