from verify_circle_ci_status import parse_project_from_url
import pytest


class TestHttpsUrlParsing:
    def test_owner(self):
        sample_owner = 'sampleowner'
        sample_https_url = f'https://github.com/{sample_owner}/samplerepo.git'
        p = parse_project_from_url(origin_url=sample_https_url)
        assert p.owner == sample_owner

    def test_repo_name(self):
        sample_repo_name = 'sample-repo-name'
        sample_https_url = 'https://github.com/sample_owner/' \
            f'{sample_repo_name}.git'
        p = parse_project_from_url(origin_url=sample_https_url)
        assert p.repo_name == sample_repo_name


class TestGitUrlParsing:
    def test_owner(self):
        sample_owner = 'sampleowner'
        sample_https_url = f'git@github.com:{sample_owner}/samplerepo.git'
        p = parse_project_from_url(origin_url=sample_https_url)
        assert p.owner == sample_owner

    def test_repo_name(self):
        sample_repo_name = 'sample-repo-name'
        sample_https_url = 'git@github.com:sample_owner/' \
            f'{sample_repo_name}.git'
        p = parse_project_from_url(origin_url=sample_https_url)
        assert p.repo_name == sample_repo_name


class TestNonGithubUrlParsing:
    def test_fails_for_non_github_url(self):
        with pytest.raises(ValueError):
            parse_project_from_url(
                origin_url='https://nongithub.com/owner/repo')
