# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Unit tests for all resource modules."""

from unittest.mock import Mock

import pytest

from oobeya.client import OobeyaClient
from oobeya.models import (
    ApiKeyRequestDTO,
    BulkAnalysisPrepareRequest,
    CreateBugRequest,
    CreateCoverageRequest,
    CreateDefectRequest,
    CreateExecutionRequest,
    DefectDetectionRequest,
    DeploymentRequestDTO,
    DeveloperRequestDTO,
    DoraAnalysisRequestDTO,
    GitAnalysisRequestDTO,
    JenkinsDoraAnalysisRequestDTO,
    OrganizationLevelDTO,
    QwiserAnalysisRequestDTO,
    SyncAnalysisTeamDTO,
    SyncGitAnalysisDTO,
    TeamAnalysisRequestDTO,
    TeamDTO,
    TeamPartialUpdateRequest,
    TeamScoreCardDTO,
)
from oobeya.resources.api_keys import ApiKeysResource
from oobeya.resources.bulk_operations import BulkOperationsResource
from oobeya.resources.defect_detection import DefectDetectionResource
from oobeya.resources.deployments import DeploymentsResource
from oobeya.resources.external_test import ExternalTestResource
from oobeya.resources.git_analysis import GitAnalysisResource
from oobeya.resources.members import MembersResource
from oobeya.resources.organization_level import OrganizationLevelResource
from oobeya.resources.qwiser import QwiserResource
from oobeya.resources.reports import ReportsResource
from oobeya.resources.system import SystemResource
from oobeya.resources.team_score_cards import TeamScoreCardsResource
from oobeya.resources.teams import TeamsResource


# --- Members Resource Tests ---
class TestMembersResource:
    """Test MembersResource methods."""

    @pytest.fixture
    def members_resource(self):
        """Create members resource with mocked client."""
        client = Mock(spec=OobeyaClient)
        return MembersResource(client)

    def test_list_members(self, members_resource):
        """Test listing members."""
        members_resource.client.get.return_value = {"contents": [], "totalElements": 0}
        result = members_resource.list(page=0, size=10)
        members_resource.client.get.assert_called_once()
        assert result is not None

    def test_list_members_none_response(self, members_resource):
        """Test listing members with None response."""
        members_resource.client.get.return_value = None
        result = members_resource.list()
        assert result is None

    def test_get_member(self, members_resource):
        """Test getting a member."""
        members_resource.client.get.return_value = {"id": "member-1", "name": "Test"}
        result = members_resource.get("member-1")
        members_resource.client.get.assert_called_once_with("/apis/v1/members/member-1")
        assert result is not None

    def test_get_member_none(self, members_resource):
        """Test getting member with None response."""
        members_resource.client.get.return_value = None
        result = members_resource.get("member-1")
        assert result is None

    def test_create_member(self, members_resource):
        """Test creating a member."""
        member = DeveloperRequestDTO(name="John", surname="Doe")
        members_resource.client.post.return_value = {"id": "member-1", "name": "John"}
        result = members_resource.create(member)
        members_resource.client.post.assert_called_once()
        assert result is not None

    def test_create_member_none(self, members_resource):
        """Test creating member with None response."""
        member = DeveloperRequestDTO(name="John")
        members_resource.client.post.return_value = None
        result = members_resource.create(member)
        assert result is None

    def test_update_member(self, members_resource):
        """Test updating a member."""
        member = DeveloperRequestDTO(id="member-1", name="John")
        members_resource.client.put.return_value = {"id": "member-1", "name": "John"}
        result = members_resource.update(member)
        members_resource.client.put.assert_called_once()
        assert result is not None

    def test_update_member_none(self, members_resource):
        """Test updating member with None response."""
        member = DeveloperRequestDTO(id="member-1")
        members_resource.client.put.return_value = None
        result = members_resource.update(member)
        assert result is None

    def test_delete_member(self, members_resource):
        """Test deleting a member."""
        members_resource.client.delete.return_value = {"id": "member-1"}
        result = members_resource.delete("member-1")
        members_resource.client.delete.assert_called_once_with("/apis/v1/members/member-1")
        assert result is not None

    def test_delete_member_none(self, members_resource):
        """Test deleting member with None response."""
        members_resource.client.delete.return_value = None
        result = members_resource.delete("member-1")
        assert result is None


# --- Teams Resource Tests ---
class TestTeamsResource:
    """Test TeamsResource methods."""

    @pytest.fixture
    def teams_resource(self):
        """Create teams resource with mocked client."""
        client = Mock(spec=OobeyaClient)
        return TeamsResource(client)

    def test_list_all_teams(self, teams_resource):
        """Test listing all teams."""
        teams_resource.client.get.return_value = [{"id": "team-1", "unitName": "Team One"}]
        result = teams_resource.list_all()
        teams_resource.client.get.assert_called_once_with("/apis/v1/teams/all")
        assert result is not None
        assert len(result) == 1

    def test_list_all_teams_none(self, teams_resource):
        """Test listing all teams with None response."""
        teams_resource.client.get.return_value = None
        result = teams_resource.list_all()
        assert result is None

    def test_list_all_teams_not_list(self, teams_resource):
        """Test listing all teams with non-list response."""
        teams_resource.client.get.return_value = {"error": "not a list"}
        result = teams_resource.list_all()
        assert result is None

    def test_create_team(self, teams_resource):
        """Test creating a team."""
        team = TeamDTO(unit_name="New Team")
        teams_resource.client.post.return_value = {"id": "team-1", "unitName": "New Team"}
        result = teams_resource.create(team)
        teams_resource.client.post.assert_called_once()
        assert result is not None

    def test_create_team_none(self, teams_resource):
        """Test creating team with None response."""
        team = TeamDTO(unit_name="New Team")
        teams_resource.client.post.return_value = None
        result = teams_resource.create(team)
        assert result is None

    def test_update_team(self, teams_resource):
        """Test updating a team."""
        team = TeamDTO(id="team-1", unit_name="Updated Team")
        teams_resource.client.put.return_value = {"id": "team-1", "unitName": "Updated Team"}
        result = teams_resource.update(team)
        teams_resource.client.put.assert_called_once()
        assert result is not None

    def test_update_team_none(self, teams_resource):
        """Test updating team with None response."""
        team = TeamDTO(id="team-1")
        teams_resource.client.put.return_value = None
        result = teams_resource.update(team)
        assert result is None

    def test_partial_update_team(self, teams_resource):
        """Test partial update of a team."""
        update = TeamPartialUpdateRequest(add_unit_members=["member-1"])
        teams_resource.client.patch.return_value = {"payload": True}
        result = teams_resource.partial_update("team-1", update)
        teams_resource.client.patch.assert_called_once()
        assert result is not None

    def test_partial_update_team_none(self, teams_resource):
        """Test partial update with None response."""
        update = TeamPartialUpdateRequest()
        teams_resource.client.patch.return_value = None
        result = teams_resource.partial_update("team-1", update)
        assert result is None

    def test_delete_team(self, teams_resource):
        """Test deleting a team."""
        teams_resource.client.delete.return_value = True
        result = teams_resource.delete("team-1")
        teams_resource.client.delete.assert_called_once_with("/apis/v1/teams/team-1")
        assert result is True

    def test_delete_team_none(self, teams_resource):
        """Test deleting team with None response."""
        teams_resource.client.delete.return_value = None
        result = teams_resource.delete("team-1")
        assert result is None

    def test_trigger_analysis(self, teams_resource):
        """Test triggering analysis."""
        request = TeamAnalysisRequestDTO(team_ids=["team-1"])
        teams_resource.client.post.return_value = True
        result = teams_resource.trigger_analysis(request)
        teams_resource.client.post.assert_called_once()
        assert result is True

    def test_trigger_analysis_none(self, teams_resource):
        """Test triggering analysis with None response."""
        request = TeamAnalysisRequestDTO()
        teams_resource.client.post.return_value = None
        result = teams_resource.trigger_analysis(request)
        assert result is None

    def test_sync_analysis(self, teams_resource):
        """Test sync analysis."""
        request = SyncAnalysisTeamDTO(team_id="team-1")
        teams_resource.client.post.return_value = True
        result = teams_resource.sync_analysis(request)
        teams_resource.client.post.assert_called_once()
        assert result is True

    def test_sync_analysis_none(self, teams_resource):
        """Test sync analysis with None response."""
        request = SyncAnalysisTeamDTO()
        teams_resource.client.post.return_value = None
        result = teams_resource.sync_analysis(request)
        assert result is None

    def test_replace_selection(self, teams_resource):
        """Test replace selection."""
        request = SyncAnalysisTeamDTO(team_id="team-1")
        teams_resource.client.put.return_value = True
        result = teams_resource.replace_selection(request)
        teams_resource.client.put.assert_called_once()
        assert result is True

    def test_replace_selection_none(self, teams_resource):
        """Test replace selection with None response."""
        request = SyncAnalysisTeamDTO()
        teams_resource.client.put.return_value = None
        result = teams_resource.replace_selection(request)
        assert result is None


# --- API Keys Resource Tests ---
class TestApiKeysResource:
    """Test ApiKeysResource methods."""

    @pytest.fixture
    def api_keys_resource(self):
        """Create API keys resource with mocked client."""
        client = Mock(spec=OobeyaClient)
        return ApiKeysResource(client)

    def test_list_all_api_keys(self, api_keys_resource):
        """Test listing all API keys."""
        api_keys_resource.client.get.return_value = [{"id": "key-1", "name": "Test Key"}]
        result = api_keys_resource.list_all()
        api_keys_resource.client.get.assert_called_once_with("/apis/v1/api-keys")
        assert result is not None
        assert len(result) == 1

    def test_list_all_api_keys_none(self, api_keys_resource):
        """Test listing all API keys with None response."""
        api_keys_resource.client.get.return_value = None
        result = api_keys_resource.list_all()
        assert result is None

    def test_list_all_api_keys_not_list(self, api_keys_resource):
        """Test listing all API keys with non-list response."""
        api_keys_resource.client.get.return_value = {"error": "not a list"}
        result = api_keys_resource.list_all()
        assert result is None

    def test_create_api_key(self, api_keys_resource):
        """Test creating an API key."""
        api_key = ApiKeyRequestDTO(name="New Key")
        api_keys_resource.client.post.return_value = {"id": "key-1", "name": "New Key"}
        result = api_keys_resource.create(api_key)
        api_keys_resource.client.post.assert_called_once()
        assert result is not None

    def test_create_api_key_none(self, api_keys_resource):
        """Test creating API key with None response."""
        api_key = ApiKeyRequestDTO(name="New Key")
        api_keys_resource.client.post.return_value = None
        result = api_keys_resource.create(api_key)
        assert result is None

    def test_delete_api_key(self, api_keys_resource):
        """Test deleting an API key."""
        api_keys_resource.client.delete.return_value = True
        result = api_keys_resource.delete("key-1")
        api_keys_resource.client.delete.assert_called_once_with("/apis/v1/api-keys/key-1")
        assert result is True

    def test_delete_api_key_none(self, api_keys_resource):
        """Test deleting API key with None response."""
        api_keys_resource.client.delete.return_value = None
        result = api_keys_resource.delete("key-1")
        assert result is None


# --- Git Analysis Resource Tests ---
class TestGitAnalysisResource:
    """Test GitAnalysisResource methods."""

    @pytest.fixture
    def git_analysis_resource(self):
        """Create git analysis resource with mocked client."""
        client = Mock(spec=OobeyaClient)
        return GitAnalysisResource(client)

    def test_list_analyses(self, git_analysis_resource):
        """Test listing analyses."""
        git_analysis_resource.client.get.return_value = [{"id": "analysis-1"}]
        result = git_analysis_resource.list(page=0, size=10)
        git_analysis_resource.client.get.assert_called_once()
        assert result is not None
        assert len(result) == 1

    def test_list_analyses_none(self, git_analysis_resource):
        """Test listing analyses with None response."""
        git_analysis_resource.client.get.return_value = None
        result = git_analysis_resource.list()
        assert result is None

    def test_list_analyses_not_list(self, git_analysis_resource):
        """Test listing analyses with non-list response."""
        git_analysis_resource.client.get.return_value = {"error": "not a list"}
        result = git_analysis_resource.list()
        assert result is None

    def test_create_analysis(self, git_analysis_resource):
        """Test creating analysis."""
        analysis = GitAnalysisRequestDTO(project_name="test-project")
        git_analysis_resource.client.post.return_value = {"id": "analysis-1"}
        result = git_analysis_resource.create(analysis)
        git_analysis_resource.client.post.assert_called_once()
        assert result is not None

    def test_create_analysis_none(self, git_analysis_resource):
        """Test creating analysis with None response."""
        analysis = GitAnalysisRequestDTO()
        git_analysis_resource.client.post.return_value = None
        result = git_analysis_resource.create(analysis)
        assert result is None

    def test_delete_analysis(self, git_analysis_resource):
        """Test deleting analysis."""
        git_analysis_resource.client.delete.return_value = True
        result = git_analysis_resource.delete("analysis-1")
        git_analysis_resource.client.delete.assert_called_once()
        assert result is True

    def test_delete_analysis_none(self, git_analysis_resource):
        """Test deleting analysis with None response."""
        git_analysis_resource.client.delete.return_value = None
        result = git_analysis_resource.delete("analysis-1")
        assert result is None

    def test_delete_commit(self, git_analysis_resource):
        """Test deleting commit from analysis."""
        git_analysis_resource.client.delete.return_value = True
        result = git_analysis_resource.delete_commit("analysis-1", "commit-1")
        git_analysis_resource.client.delete.assert_called_once()
        assert result is True

    def test_delete_commit_none(self, git_analysis_resource):
        """Test deleting commit with None response."""
        git_analysis_resource.client.delete.return_value = None
        result = git_analysis_resource.delete_commit("analysis-1", "commit-1")
        assert result is None

    def test_create_jenkins_dora_analysis(self, git_analysis_resource):
        """Test creating Jenkins DORA analysis."""
        request = JenkinsDoraAnalysisRequestDTO(ci_job_name="job-1")
        git_analysis_resource.client.post.return_value = True
        result = git_analysis_resource.create_jenkins_dora_analysis("analysis-1", request)
        git_analysis_resource.client.post.assert_called_once()
        assert result is True

    def test_create_jenkins_dora_analysis_none(self, git_analysis_resource):
        """Test creating Jenkins DORA analysis with None response."""
        request = JenkinsDoraAnalysisRequestDTO()
        git_analysis_resource.client.post.return_value = None
        result = git_analysis_resource.create_jenkins_dora_analysis("analysis-1", request)
        assert result is None

    def test_create_bulk_dora_analysis(self, git_analysis_resource):
        """Test creating bulk DORA analysis."""
        request = DoraAnalysisRequestDTO(branch="main")
        git_analysis_resource.client.post.return_value = True
        result = git_analysis_resource.create_bulk_dora_analysis(request)
        git_analysis_resource.client.post.assert_called_once()
        assert result is True

    def test_create_bulk_dora_analysis_none(self, git_analysis_resource):
        """Test creating bulk DORA analysis with None response."""
        request = DoraAnalysisRequestDTO()
        git_analysis_resource.client.post.return_value = None
        result = git_analysis_resource.create_bulk_dora_analysis(request)
        assert result is None

    def test_delete_bulk_dora_analysis(self, git_analysis_resource):
        """Test deleting bulk DORA analysis."""
        git_analysis_resource.client.delete.return_value = True
        result = git_analysis_resource.delete_bulk_dora_analysis()
        git_analysis_resource.client.delete.assert_called_once()
        assert result is True

    def test_delete_bulk_dora_analysis_none(self, git_analysis_resource):
        """Test deleting bulk DORA analysis with None response."""
        git_analysis_resource.client.delete.return_value = None
        result = git_analysis_resource.delete_bulk_dora_analysis()
        assert result is None

    def test_trigger_bulk_dora_analysis(self, git_analysis_resource):
        """Test triggering bulk DORA analysis."""
        git_analysis_resource.client.post.return_value = True
        result = git_analysis_resource.trigger_bulk_dora_analysis()
        git_analysis_resource.client.post.assert_called_once()
        assert result is True

    def test_trigger_bulk_dora_analysis_none(self, git_analysis_resource):
        """Test triggering bulk DORA analysis with None response."""
        git_analysis_resource.client.post.return_value = None
        result = git_analysis_resource.trigger_bulk_dora_analysis()
        assert result is None

    def test_get_dora_summary_metrics(self, git_analysis_resource):
        """Test getting DORA summary metrics."""
        git_analysis_resource.client.get.return_value = {"deploymentFrequency": {"value": 10}}
        result = git_analysis_resource.get_dora_summary_metrics(
            widgets=["DEPLOYMENT_FREQUENCY"],
            team_id="team-1",
            analysis_id=["analysis-1"],
            from_timestamp=1000,
            to_timestamp=2000,
        )
        git_analysis_resource.client.get.assert_called_once()
        assert result is not None

    def test_get_dora_summary_metrics_none(self, git_analysis_resource):
        """Test getting DORA summary metrics with None response."""
        git_analysis_resource.client.get.return_value = None
        result = git_analysis_resource.get_dora_summary_metrics(widgets=["DEPLOYMENT_FREQUENCY"])
        assert result is None


# --- Deployments Resource Tests ---
class TestDeploymentsResource:
    """Test DeploymentsResource methods."""

    @pytest.fixture
    def deployments_resource(self):
        """Create deployments resource with mocked client."""
        client = Mock(spec=OobeyaClient)
        return DeploymentsResource(client)

    def test_list_deployments(self, deployments_resource):
        """Test listing deployments."""
        deployments_resource.client.get.return_value = [{"id": "deployment-1"}]
        result = deployments_resource.list(page=0, size=10)
        deployments_resource.client.get.assert_called_once()
        assert result is not None
        assert len(result) == 1

    def test_list_deployments_none(self, deployments_resource):
        """Test listing deployments with None response."""
        deployments_resource.client.get.return_value = None
        result = deployments_resource.list()
        assert result is None

    def test_list_deployments_not_list(self, deployments_resource):
        """Test listing deployments with non-list response."""
        deployments_resource.client.get.return_value = {"error": "not a list"}
        result = deployments_resource.list()
        assert result is None

    def test_create_deployment(self, deployments_resource):
        """Test creating deployment."""
        deployment = DeploymentRequestDTO(analysis_id="analysis-1")
        deployments_resource.client.post.return_value = {"id": "deployment-1"}
        result = deployments_resource.create(deployment)
        deployments_resource.client.post.assert_called_once()
        assert result is not None

    def test_create_deployment_none(self, deployments_resource):
        """Test creating deployment with None response."""
        deployment = DeploymentRequestDTO()
        deployments_resource.client.post.return_value = None
        result = deployments_resource.create(deployment)
        assert result is None

    def test_delete_deployment(self, deployments_resource):
        """Test deleting deployment."""
        deployments_resource.client.delete.return_value = True
        result = deployments_resource.delete("deployment-1")
        deployments_resource.client.delete.assert_called_once()
        assert result is True

    def test_delete_deployment_none(self, deployments_resource):
        """Test deleting deployment with None response."""
        deployments_resource.client.delete.return_value = None
        result = deployments_resource.delete("deployment-1")
        assert result is None


# --- Reports Resource Tests ---
class TestReportsResource:
    """Test ReportsResource methods."""

    @pytest.fixture
    def reports_resource(self):
        """Create reports resource with mocked client."""
        client = Mock(spec=OobeyaClient)
        return ReportsResource(client)

    def test_get_member_qualities(self, reports_resource):
        """Test getting member qualities."""
        reports_resource.client.get.return_value = {"technicalDebt": {}}
        result = reports_resource.get_member_qualities("member-1", "2024-01-01", "2024-12-31")
        reports_resource.client.get.assert_called_once()
        assert result is not None

    def test_get_member_qualities_none(self, reports_resource):
        """Test getting member qualities with None response."""
        reports_resource.client.get.return_value = None
        result = reports_resource.get_member_qualities("member-1", "2024-01-01", "2024-12-31")
        assert result is None

    def test_get_member_pull_requests(self, reports_resource):
        """Test getting member pull requests."""
        reports_resource.client.get.return_value = {"statistic": {}}
        result = reports_resource.get_member_pull_requests("member-1", "2024-01-01", "2024-12-31")
        reports_resource.client.get.assert_called_once()
        assert result is not None

    def test_get_member_pull_requests_none(self, reports_resource):
        """Test getting member pull requests with None response."""
        reports_resource.client.get.return_value = None
        result = reports_resource.get_member_pull_requests("member-1", "2024-01-01", "2024-12-31")
        assert result is None

    def test_get_member_commits(self, reports_resource):
        """Test getting member commits."""
        reports_resource.client.get.return_value = {"statistic": {}}
        result = reports_resource.get_member_commits("member-1", "2024-01-01", "2024-12-31")
        reports_resource.client.get.assert_called_once()
        assert result is not None

    def test_get_member_commits_none(self, reports_resource):
        """Test getting member commits with None response."""
        reports_resource.client.get.return_value = None
        result = reports_resource.get_member_commits("member-1", "2024-01-01", "2024-12-31")
        assert result is None

    def test_get_team_qualities(self, reports_resource):
        """Test getting team qualities."""
        reports_resource.client.get.return_value = {"technicalDebt": {}}
        result = reports_resource.get_team_qualities("team-1", "2024-01-01", "2024-12-31")
        reports_resource.client.get.assert_called_once()
        assert result is not None

    def test_get_team_qualities_none(self, reports_resource):
        """Test getting team qualities with None response."""
        reports_resource.client.get.return_value = None
        result = reports_resource.get_team_qualities("team-1", "2024-01-01", "2024-12-31")
        assert result is None

    def test_get_team_pull_requests(self, reports_resource):
        """Test getting team pull requests."""
        reports_resource.client.get.return_value = {"statistic": {}}
        result = reports_resource.get_team_pull_requests("team-1", "2024-01-01", "2024-12-31")
        reports_resource.client.get.assert_called_once()
        assert result is not None

    def test_get_team_pull_requests_none(self, reports_resource):
        """Test getting team pull requests with None response."""
        reports_resource.client.get.return_value = None
        result = reports_resource.get_team_pull_requests("team-1", "2024-01-01", "2024-12-31")
        assert result is None

    def test_get_team_commits(self, reports_resource):
        """Test getting team commits."""
        reports_resource.client.get.return_value = {"statistic": {}}
        result = reports_resource.get_team_commits("team-1", "2024-01-01", "2024-12-31")
        reports_resource.client.get.assert_called_once()
        assert result is not None

    def test_get_team_commits_none(self, reports_resource):
        """Test getting team commits with None response."""
        reports_resource.client.get.return_value = None
        result = reports_resource.get_team_commits("team-1", "2024-01-01", "2024-12-31")
        assert result is None

    def test_get_team_member_qualities(self, reports_resource):
        """Test getting team member qualities."""
        reports_resource.client.get.return_value = {"technicalDebt": {}}
        result = reports_resource.get_team_member_qualities("team-1", "member-1", "2024-01-01", "2024-12-31")
        reports_resource.client.get.assert_called_once()
        assert result is not None

    def test_get_team_member_qualities_none(self, reports_resource):
        """Test getting team member qualities with None response."""
        reports_resource.client.get.return_value = None
        result = reports_resource.get_team_member_qualities("team-1", "member-1", "2024-01-01", "2024-12-31")
        assert result is None

    def test_get_team_member_pull_requests(self, reports_resource):
        """Test getting team member pull requests."""
        reports_resource.client.get.return_value = {"statistic": {}}
        result = reports_resource.get_team_member_pull_requests("team-1", "member-1", "2024-01-01", "2024-12-31")
        reports_resource.client.get.assert_called_once()
        assert result is not None

    def test_get_team_member_pull_requests_none(self, reports_resource):
        """Test getting team member pull requests with None response."""
        reports_resource.client.get.return_value = None
        result = reports_resource.get_team_member_pull_requests("team-1", "member-1", "2024-01-01", "2024-12-31")
        assert result is None

    def test_get_team_member_commits(self, reports_resource):
        """Test getting team member commits."""
        reports_resource.client.get.return_value = {"statistic": {}}
        result = reports_resource.get_team_member_commits("team-1", "member-1", "2024-01-01", "2024-12-31")
        reports_resource.client.get.assert_called_once()
        assert result is not None

    def test_get_team_member_commits_none(self, reports_resource):
        """Test getting team member commits with None response."""
        reports_resource.client.get.return_value = None
        result = reports_resource.get_team_member_commits("team-1", "member-1", "2024-01-01", "2024-12-31")
        assert result is None


# --- External Test Resource Tests ---
class TestExternalTestResource:
    """Test ExternalTestResource methods."""

    @pytest.fixture
    def external_test_resource(self):
        """Create external test resource with mocked client."""
        client = Mock(spec=OobeyaClient)
        return ExternalTestResource(client)

    def test_create_execution(self, external_test_resource):
        """Test creating execution."""
        request = CreateExecutionRequest(
            execution_id="exec-1",
            status="PASS",
            execution_time=100,
            execution_start_date="2024-01-01",
            execution_end_date="2024-01-01",
            action_date="2024-01-01",
        )
        external_test_resource.client.post.return_value = {"id": "exec-1"}
        result = external_test_resource.create_execution(request)
        external_test_resource.client.post.assert_called_once()
        assert result is not None

    def test_create_execution_none(self, external_test_resource):
        """Test creating execution with None response."""
        request = CreateExecutionRequest(
            execution_id="exec-1",
            status="PASS",
            execution_time=100,
            execution_start_date="2024-01-01",
            execution_end_date="2024-01-01",
            action_date="2024-01-01",
        )
        external_test_resource.client.post.return_value = None
        result = external_test_resource.create_execution(request)
        assert result is None

    def test_get_last_execution(self, external_test_resource):
        """Test getting last execution."""
        external_test_resource.client.get.return_value = {"executionId": "exec-1"}
        result = external_test_resource.get_last_execution("app-1")
        external_test_resource.client.get.assert_called_once()
        assert result is not None

    def test_get_last_execution_none(self, external_test_resource):
        """Test getting last execution with None response."""
        external_test_resource.client.get.return_value = None
        result = external_test_resource.get_last_execution("app-1")
        assert result is None

    def test_delete_execution(self, external_test_resource):
        """Test deleting execution."""
        external_test_resource.client.delete.return_value = True
        result = external_test_resource.delete_execution("exec-1", "scenario-1")
        external_test_resource.client.delete.assert_called_once()
        assert result is True

    def test_delete_execution_none(self, external_test_resource):
        """Test deleting execution with None response."""
        external_test_resource.client.delete.return_value = None
        result = external_test_resource.delete_execution("exec-1", "scenario-1")
        assert result is None

    def test_create_defect(self, external_test_resource):
        """Test creating defect."""
        from datetime import datetime

        request = CreateDefectRequest(
            application_id="app-1",
            problem_no="PROB-1",
            detected_date=datetime.now(),
            fixed_date=datetime.now(),
        )
        external_test_resource.client.post.return_value = {
            "applicationId": "app-1",
            "problemNo": "PROB-1",
            "detectedDate": "2024-01-01T00:00:00",
            "fixedDate": "2024-01-02T00:00:00",
        }
        result = external_test_resource.create_defect(request)
        external_test_resource.client.post.assert_called_once()
        assert result is not None

    def test_create_defect_none(self, external_test_resource):
        """Test creating defect with None response."""
        from datetime import datetime

        request = CreateDefectRequest(
            application_id="app-1",
            problem_no="PROB-1",
            detected_date=datetime.now(),
            fixed_date=datetime.now(),
        )
        external_test_resource.client.post.return_value = None
        result = external_test_resource.create_defect(request)
        assert result is None

    def test_get_last_defect(self, external_test_resource):
        """Test getting last defect."""
        external_test_resource.client.get.return_value = {
            "applicationId": "app-1",
            "problemNo": "PROB-1",
            "detectedDate": "2024-01-01T00:00:00",
            "fixedDate": "2024-01-02T00:00:00",
        }
        result = external_test_resource.get_last_defect("app-1")
        external_test_resource.client.get.assert_called_once()
        assert result is not None

    def test_get_last_defect_none(self, external_test_resource):
        """Test getting last defect with None response."""
        external_test_resource.client.get.return_value = None
        result = external_test_resource.get_last_defect("app-1")
        assert result is None

    def test_delete_defect(self, external_test_resource):
        """Test deleting defect."""
        external_test_resource.client.delete.return_value = True
        result = external_test_resource.delete_defect("app-1", "PROB-1")
        external_test_resource.client.delete.assert_called_once()
        assert result is True

    def test_delete_defect_none(self, external_test_resource):
        """Test deleting defect with None response."""
        external_test_resource.client.delete.return_value = None
        result = external_test_resource.delete_defect("app-1", "PROB-1")
        assert result is None

    def test_create_coverage(self, external_test_resource):
        """Test creating coverage."""
        request = CreateCoverageRequest(
            action_date="2024-01-01",
            application_id="app-1",
            coverage_id="cov-1",
            coverage_rate=80.5,
            total_line=1000,
            covered_line=805,
            uncovered_line=195,
        )
        external_test_resource.client.post.return_value = {"coverageId": "cov-1"}
        result = external_test_resource.create_coverage(request)
        external_test_resource.client.post.assert_called_once()
        assert result is not None

    def test_create_coverage_none(self, external_test_resource):
        """Test creating coverage with None response."""
        request = CreateCoverageRequest(
            action_date="2024-01-01",
            application_id="app-1",
            coverage_id="cov-1",
            coverage_rate=80.5,
            total_line=1000,
            covered_line=805,
            uncovered_line=195,
        )
        external_test_resource.client.post.return_value = None
        result = external_test_resource.create_coverage(request)
        assert result is None

    def test_get_last_coverage(self, external_test_resource):
        """Test getting last coverage."""
        external_test_resource.client.get.return_value = {"coverageId": "cov-1"}
        result = external_test_resource.get_last_coverage("app-1", "service-1")
        external_test_resource.client.get.assert_called_once()
        assert result is not None

    def test_get_last_coverage_none(self, external_test_resource):
        """Test getting last coverage with None response."""
        external_test_resource.client.get.return_value = None
        result = external_test_resource.get_last_coverage("app-1", "service-1")
        assert result is None

    def test_delete_coverage(self, external_test_resource):
        """Test deleting coverage."""
        external_test_resource.client.delete.return_value = True
        result = external_test_resource.delete_coverage("cov-1")
        external_test_resource.client.delete.assert_called_once()
        assert result is True

    def test_delete_coverage_none(self, external_test_resource):
        """Test deleting coverage with None response."""
        external_test_resource.client.delete.return_value = None
        result = external_test_resource.delete_coverage("cov-1")
        assert result is None

    def test_create_bug(self, external_test_resource):
        """Test creating bug."""
        request = CreateBugRequest(application_id="app-1", bug_id="BUG-1", name="Test Bug")
        external_test_resource.client.post.return_value = {"bugId": "BUG-1"}
        result = external_test_resource.create_bug(request)
        external_test_resource.client.post.assert_called_once()
        assert result is not None

    def test_create_bug_none(self, external_test_resource):
        """Test creating bug with None response."""
        request = CreateBugRequest(application_id="app-1", bug_id="BUG-1", name="Test Bug")
        external_test_resource.client.post.return_value = None
        result = external_test_resource.create_bug(request)
        assert result is None

    def test_get_last_bug(self, external_test_resource):
        """Test getting last bug."""
        external_test_resource.client.get.return_value = {"bugId": "BUG-1"}
        result = external_test_resource.get_last_bug("app-1")
        external_test_resource.client.get.assert_called_once()
        assert result is not None

    def test_get_last_bug_none(self, external_test_resource):
        """Test getting last bug with None response."""
        external_test_resource.client.get.return_value = None
        result = external_test_resource.get_last_bug("app-1")
        assert result is None

    def test_delete_bug(self, external_test_resource):
        """Test deleting bug."""
        external_test_resource.client.delete.return_value = True
        result = external_test_resource.delete_bug("BUG-1")
        external_test_resource.client.delete.assert_called_once()
        assert result is True

    def test_delete_bug_none(self, external_test_resource):
        """Test deleting bug with None response."""
        external_test_resource.client.delete.return_value = None
        result = external_test_resource.delete_bug("BUG-1")
        assert result is None


# --- Bulk Operations Resource Tests ---
class TestBulkOperationsResource:
    """Test BulkOperationsResource methods."""

    @pytest.fixture
    def bulk_operations_resource(self):
        """Create bulk operations resource with mocked client."""
        client = Mock(spec=OobeyaClient)
        return BulkOperationsResource(client)

    def test_prepare_bulk_analyses(self, bulk_operations_resource):
        """Test preparing bulk analyses."""
        request = BulkAnalysisPrepareRequest(datasource_id="ds-1")
        bulk_operations_resource.client.post.return_value = True
        result = bulk_operations_resource.prepare_bulk_analyses(request)
        bulk_operations_resource.client.post.assert_called_once()
        assert result is True

    def test_prepare_bulk_analyses_none(self, bulk_operations_resource):
        """Test preparing bulk analyses with None response."""
        request = BulkAnalysisPrepareRequest()
        bulk_operations_resource.client.post.return_value = None
        result = bulk_operations_resource.prepare_bulk_analyses(request)
        assert result is None

    def test_get_bulk_analyses_file(self, bulk_operations_resource):
        """Test getting bulk analyses file."""
        bulk_operations_resource.client.get.return_value = b"file content"
        result = bulk_operations_resource.get_bulk_analyses_file()
        bulk_operations_resource.client.get.assert_called_once()
        assert result == b"file content"

    def test_get_bulk_analyses_file_none(self, bulk_operations_resource):
        """Test getting bulk analyses file with None response."""
        bulk_operations_resource.client.get.return_value = None
        result = bulk_operations_resource.get_bulk_analyses_file()
        assert result is None

    def test_import_git_analysis(self, bulk_operations_resource, tmp_path):
        """Test importing git analysis from file."""
        test_file = tmp_path / "test.xlsx"
        test_file.write_text("test content")
        bulk_operations_resource.client.post.return_value = True
        result = bulk_operations_resource.import_git_analysis(str(test_file))
        bulk_operations_resource.client.post.assert_called_once()
        assert result is True

    def test_import_git_analysis_none(self, bulk_operations_resource, tmp_path):
        """Test importing git analysis with None response."""
        test_file = tmp_path / "test.xlsx"
        test_file.write_text("test content")
        bulk_operations_resource.client.post.return_value = None
        result = bulk_operations_resource.import_git_analysis(str(test_file))
        assert result is None

    def test_update_git_analysis(self, bulk_operations_resource, tmp_path):
        """Test updating git analysis from file."""
        test_file = tmp_path / "test.xlsx"
        test_file.write_text("test content")
        bulk_operations_resource.client.put.return_value = True
        result = bulk_operations_resource.update_git_analysis(str(test_file))
        bulk_operations_resource.client.put.assert_called_once()
        assert result is True

    def test_update_git_analysis_none(self, bulk_operations_resource, tmp_path):
        """Test updating git analysis with None response."""
        test_file = tmp_path / "test.xlsx"
        test_file.write_text("test content")
        bulk_operations_resource.client.put.return_value = None
        result = bulk_operations_resource.update_git_analysis(str(test_file))
        assert result is None

    def test_sync_git_analysis(self, bulk_operations_resource):
        """Test syncing git analysis."""
        request = SyncGitAnalysisDTO(team_id="team-1")
        bulk_operations_resource.client.put.return_value = True
        result = bulk_operations_resource.sync_git_analysis(request)
        bulk_operations_resource.client.put.assert_called_once()
        assert result is True

    def test_sync_git_analysis_none(self, bulk_operations_resource):
        """Test syncing git analysis with None response."""
        request = SyncGitAnalysisDTO()
        bulk_operations_resource.client.put.return_value = None
        result = bulk_operations_resource.sync_git_analysis(request)
        assert result is None


# --- Qwiser Resource Tests ---
class TestQwiserResource:
    """Test QwiserResource methods."""

    @pytest.fixture
    def qwiser_resource(self):
        """Create qwiser resource with mocked client."""
        client = Mock(spec=OobeyaClient)
        return QwiserResource(client)

    def test_start_analysis(self, qwiser_resource):
        """Test starting analysis."""
        request = QwiserAnalysisRequestDTO(project_key="proj-1")
        qwiser_resource.client.post.return_value = True
        result = qwiser_resource.start_analysis(request)
        qwiser_resource.client.post.assert_called_once()
        assert result is True

    def test_start_analysis_none(self, qwiser_resource):
        """Test starting analysis with None response."""
        request = QwiserAnalysisRequestDTO()
        qwiser_resource.client.post.return_value = None
        result = qwiser_resource.start_analysis(request)
        assert result is None


# --- Defect Detection Resource Tests ---
class TestDefectDetectionResource:
    """Test DefectDetectionResource methods."""

    @pytest.fixture
    def defect_detection_resource(self):
        """Create defect detection resource with mocked client."""
        client = Mock(spec=OobeyaClient)
        return DefectDetectionResource(client)

    def test_create(self, defect_detection_resource):
        """Test creating defect detection."""
        request = DefectDetectionRequest(repo_name="repo-1")
        defect_detection_resource.client.post.return_value = True
        result = defect_detection_resource.create(request)
        defect_detection_resource.client.post.assert_called_once()
        assert result is True

    def test_create_none(self, defect_detection_resource):
        """Test creating defect detection with None response."""
        request = DefectDetectionRequest()
        defect_detection_resource.client.post.return_value = None
        result = defect_detection_resource.create(request)
        assert result is None


# --- System Resource Tests ---
class TestSystemResource:
    """Test SystemResource methods."""

    @pytest.fixture
    def system_resource(self):
        """Create system resource with mocked client."""
        client = Mock(spec=OobeyaClient)
        return SystemResource(client)

    def test_get_logs(self, system_resource):
        """Test getting logs."""
        system_resource.client.get.return_value = "log content"
        result = system_resource.get_logs()
        system_resource.client.get.assert_called_once()
        assert result == "log content"

    def test_get_logs_none(self, system_resource):
        """Test getting logs with None response."""
        system_resource.client.get.return_value = None
        result = system_resource.get_logs()
        assert result is None

    def test_clear_git_analyses(self, system_resource):
        """Test clearing git analyses."""
        system_resource.client.delete.return_value = True
        result = system_resource.clear_git_analyses()
        system_resource.client.delete.assert_called_once()
        assert result is True

    def test_clear_git_analyses_none(self, system_resource):
        """Test clearing git analyses with None response."""
        system_resource.client.delete.return_value = None
        result = system_resource.clear_git_analyses()
        assert result is None


# --- Team Score Cards Resource Tests ---
class TestTeamScoreCardsResource:
    """Test TeamScoreCardsResource methods."""

    @pytest.fixture
    def team_score_cards_resource(self):
        """Create team score cards resource with mocked client."""
        client = Mock(spec=OobeyaClient)
        return TeamScoreCardsResource(client)

    def test_create_score_card(self, team_score_cards_resource):
        """Test creating score card."""
        score_card = TeamScoreCardDTO(team_id="team-1")
        team_score_cards_resource.client.post.return_value = {"teamId": "team-1"}
        result = team_score_cards_resource.create(score_card)
        team_score_cards_resource.client.post.assert_called_once()
        assert result is not None

    def test_create_score_card_none(self, team_score_cards_resource):
        """Test creating score card with None response."""
        score_card = TeamScoreCardDTO()
        team_score_cards_resource.client.post.return_value = None
        result = team_score_cards_resource.create(score_card)
        assert result is None

    def test_update_score_card(self, team_score_cards_resource):
        """Test updating score card."""
        score_card = TeamScoreCardDTO(id="card-1", team_id="team-1")
        team_score_cards_resource.client.put.return_value = {"id": "card-1"}
        result = team_score_cards_resource.update(score_card)
        team_score_cards_resource.client.put.assert_called_once()
        assert result is not None

    def test_update_score_card_none(self, team_score_cards_resource):
        """Test updating score card with None response."""
        score_card = TeamScoreCardDTO()
        team_score_cards_resource.client.put.return_value = None
        result = team_score_cards_resource.update(score_card)
        assert result is None


# --- Organization Level Resource Tests ---
class TestOrganizationLevelResource:
    """Test OrganizationLevelResource methods."""

    @pytest.fixture
    def organization_level_resource(self):
        """Create organization level resource with mocked client."""
        client = Mock(spec=OobeyaClient)
        return OrganizationLevelResource(client)

    def test_list_all_levels(self, organization_level_resource):
        """Test listing all organization levels."""
        organization_level_resource.client.get.return_value = [{"id": "level-1", "name": "Level 1"}]
        result = organization_level_resource.list_all()
        organization_level_resource.client.get.assert_called_once()
        assert result is not None
        assert len(result) == 1

    def test_list_all_levels_none(self, organization_level_resource):
        """Test listing all organization levels with None response."""
        organization_level_resource.client.get.return_value = None
        result = organization_level_resource.list_all()
        assert result is None

    def test_list_all_levels_not_list(self, organization_level_resource):
        """Test listing all organization levels with non-list response."""
        organization_level_resource.client.get.return_value = {"error": "not a list"}
        result = organization_level_resource.list_all()
        assert result is None

    def test_create_level(self, organization_level_resource):
        """Test creating organization level."""
        org_level = OrganizationLevelDTO(name="New Level")
        organization_level_resource.client.post.return_value = {"id": "level-1", "name": "New Level"}
        result = organization_level_resource.create(org_level)
        organization_level_resource.client.post.assert_called_once()
        assert result is not None

    def test_create_level_none(self, organization_level_resource):
        """Test creating organization level with None response."""
        org_level = OrganizationLevelDTO()
        organization_level_resource.client.post.return_value = None
        result = organization_level_resource.create(org_level)
        assert result is None

    def test_update_level(self, organization_level_resource):
        """Test updating organization level."""
        org_level = OrganizationLevelDTO(id="level-1", name="Updated Level")
        organization_level_resource.client.put.return_value = {"id": "level-1", "name": "Updated Level"}
        result = organization_level_resource.update("level-1", org_level)
        organization_level_resource.client.put.assert_called_once()
        assert result is not None

    def test_update_level_none(self, organization_level_resource):
        """Test updating organization level with None response."""
        org_level = OrganizationLevelDTO()
        organization_level_resource.client.put.return_value = None
        result = organization_level_resource.update("level-1", org_level)
        assert result is None
