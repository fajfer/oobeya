# SPDX-FileCopyrightText: 2025 Damian Fajfer <damian@fajfer.org>
#
# SPDX-License-Identifier: EUPL-1.2

"""Data models for Oobeya API requests and responses."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


# Enums
class UserType(str, Enum):
    """User type enumeration."""

    LDAP = "LDAP"
    DB = "DB"
    AZURE = "AZURE"
    OKTA = "OKTA"


class CompanyRole(str, Enum):
    """Company role enumeration."""

    NONE = "NONE"
    DEVELOPER = "DEVELOPER"
    QA_ENGINEER = "QA_ENGINEER"
    DEVOPS_ENGINEER = "DEVOPS_ENGINEER"
    BUSINESS_ANALYST = "BUSINESS_ANALYST"
    PROJECT_MANAGER = "PROJECT_MANAGER"
    SCRUM_MASTER = "SCRUM_MASTER"
    PRODUCT_OWNER = "PRODUCT_OWNER"
    PRODUCT_MANAGER = "PRODUCT_MANAGER"
    TEAM_LEAD = "TEAM_LEAD"
    MANAGER = "MANAGER"
    DIRECTOR = "DIRECTOR"
    EXECUTIVE_BOARD_MEMBER = "EXECUTIVE_BOARD_MEMBER"
    TECH_LEAD = "TECH_LEAD"


class DeploymentType(str, Enum):
    """Deployment type enumeration."""

    RELEASE = "RELEASE"
    HOTFIX = "HOTFIX"


class AnalysisType(str, Enum):
    """Analysis type enumeration."""

    PULL_REQUEST = "PULL_REQUEST"
    TRUNK_BASED = "TRUNK_BASED"


class ReleaseStrategyType(str, Enum):
    """Release strategy type enumeration."""

    GITFLOW_RELEASE = "GITFLOW_RELEASE"
    MERGE_REQUEST_FLOW = "MERGE_REQUEST_FLOW"
    GIT_TAG = "GIT_TAG"


class GitProviderType(str, Enum):
    """Git provider type enumeration."""

    GITLAB = "GITLAB"


class ExecutionStatus(str, Enum):
    """Execution status enumeration."""

    TODO = "TODO"
    EXECUTING = "EXECUTING"
    FAIL = "FAIL"
    PASS = "PASS"
    ABORTED = "ABORTED"


# Base Models
@dataclass
class TeamMeta:
    """Team metadata."""

    id: Optional[str] = None
    name: Optional[str] = None


@dataclass
class MetaResourceRequestDTO:
    """Meta resource request DTO."""

    id: Optional[str] = None
    name: Optional[str] = None


@dataclass
class KeyLabel:
    """Key label pair with ordering."""

    key: Optional[str] = None
    label: Optional[str] = None
    order: Optional[int] = None
    selected: Optional[bool] = None
    active_user: Optional[bool] = None


@dataclass
class HeaderFilter:
    """Header filter."""

    key: Optional[str] = None
    label: Optional[str] = None
    selected: Optional[bool] = None


# User Models
@dataclass
class UserRequestDTO:
    """User request data transfer object."""

    id: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    user_type: Optional[str] = None
    company_role: Optional[str] = None
    hire_date: Optional[str] = None
    termination_date: Optional[str] = None


# @dataclass
# class DeveloperResource:
#     """Developer resource."""

#     id: Optional[str] = None
#     name: Optional[str] = None
#     surname: Optional[str] = None
#     user_name: Optional[str] = None
#     enabled: Optional[bool] = None
#     addon_accounts: List[str] = field(default_factory=list)
#     company_role: Optional[str] = None
#     teams: List[TeamMeta] = field(default_factory=list)
#     full_name: Optional[str] = None


@dataclass
class DeveloperResource:
    """Developer resource."""

    id: Optional[str] = None
    developer_id: Optional[str] = None  # The actual member/developer ID
    name: Optional[str] = None
    surname: Optional[str] = None
    username: Optional[str] = None  # API uses 'username', not 'userName'
    user_name: Optional[str] = None  # Keep for backwards compatibility
    email: Optional[str] = None
    enabled: Optional[bool] = None
    developer: Optional[bool] = None
    user_type: Optional[str] = None
    roles: List[str] = field(default_factory=list)
    addon_accounts: List[str] = field(default_factory=list)
    company_role: Optional[str] = None
    avatar: Optional[str] = None
    locked: Optional[bool] = None
    deletable: Optional[bool] = None
    hire_date: Optional[str] = None
    termination_date: Optional[str] = None
    ldapKey: Optional[str] = None
    teams: List[TeamMeta] = field(default_factory=list)
    full_name: Optional[str] = None


# Member Models
@dataclass
class DeveloperRequestDTO:
    """Developer request data transfer object."""

    id: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    user_name: Optional[str] = None
    addon_accounts: List[str] = field(default_factory=list)
    company_role: Optional[str] = None
    teams: List[MetaResourceRequestDTO] = field(default_factory=list)


# Team Models
@dataclass
class BulkTeamRequest:
    """Bulk team request."""

    id: Optional[str] = None
    organization_id: Optional[str] = None
    organization_name: Optional[str] = None
    unit_name: Optional[str] = None
    unit_members: List[str] = field(default_factory=list)
    unit_leads: List[str] = field(default_factory=list)
    upper_level_team: Optional[Any] = None


@dataclass
class TeamDTO:
    """Team data transfer object."""

    id: Optional[str] = None
    created_date: Optional[datetime] = None
    modify_date: Optional[datetime] = None
    created_user: Optional[str] = None
    modify_user: Optional[str] = None
    version: Optional[int] = None
    deleted_date: Optional[datetime] = None
    organization_id: Optional[str] = None
    organization_name: Optional[str] = None
    unit_name: Optional[str] = None
    unit_members: List[str] = field(default_factory=list)
    unit_leads: List[str] = field(default_factory=list)
    included_teams: List[BulkTeamRequest] = field(default_factory=list)
    upper_level_team: Optional[BulkTeamRequest] = None


@dataclass
class TeamPartialUpdateRequest:
    """Team partial update request (PATCH)."""

    organization_id: Optional[str] = None
    organization_name: Optional[str] = None
    unit_name: Optional[str] = None
    upper_level_team_id: Optional[str] = None
    upper_level_team_name: Optional[str] = None
    add_unit_members: List[str] = field(default_factory=list)
    remove_unit_members: List[str] = field(default_factory=list)
    add_unit_leads: List[str] = field(default_factory=list)
    remove_unit_leads: List[str] = field(default_factory=list)
    remove_upper_team_ids: List[str] = field(default_factory=list)


@dataclass
class TeamAnalysisRequestDTO:
    """Team analysis request DTO."""

    team_ids: List[str] = field(default_factory=list)
    trigger: Optional["TriggerAnalysisRequestDTO"] = None


@dataclass
class TriggerAnalysisRequestDTO:
    """Trigger analysis request DTO."""

    git: Optional[bool] = None
    pull_request: Optional[bool] = None
    deployment: Optional[bool] = None


@dataclass
class Branch:
    """Branch configuration."""

    priority: Optional[str] = None
    name: Optional[str] = None


@dataclass
class SyncAnalysisTeamDTO:
    """Sync analysis team DTO."""

    team_id: Optional[str] = None
    team_analysis_branches: List[Branch] = field(default_factory=list)
    team_dora_branches: List[Branch] = field(default_factory=list)
    team_sonar_branches: List[Branch] = field(default_factory=list)


# Team Score Card Models
@dataclass
class LiteGitAnalysisDTO:
    """Lite git analysis DTO."""

    analysis_id: Optional[str] = None
    has_dora_analysis: Optional[bool] = None


@dataclass
class LiteSonarAnalysisDTO:
    """Lite sonar analysis DTO."""

    datasource_url: Optional[str] = None
    project_key: Optional[str] = None
    project_name: Optional[str] = None
    branch: Optional[str] = None


@dataclass
class TeamScoreCardDTO:
    """Team score card data transfer object."""

    id: Optional[str] = None
    created_date: Optional[datetime] = None
    modify_date: Optional[datetime] = None
    created_user: Optional[str] = None
    modify_user: Optional[str] = None
    version: Optional[int] = None
    deleted_date: Optional[datetime] = None
    team_id: Optional[str] = None
    git_analyses: List[LiteGitAnalysisDTO] = field(default_factory=list)
    sonar_projects: List[LiteSonarAnalysisDTO] = field(default_factory=list)


# Organization Level Models
@dataclass
class OrganizationLevelDTO:
    """Organization level data transfer object."""

    id: Optional[str] = None
    created_date: Optional[datetime] = None
    modify_date: Optional[datetime] = None
    created_user: Optional[str] = None
    modify_user: Optional[str] = None
    version: Optional[int] = None
    deleted_date: Optional[datetime] = None
    name: Optional[str] = None
    level: Optional[int] = None
    lead_roles: List[KeyLabel] = field(default_factory=list)


# Git Analysis Models
@dataclass
class GitAnalysisRequestDTO:
    """Git analysis request DTO."""

    datasource_id: Optional[str] = None
    workspace_path: Optional[str] = None
    project_name: Optional[str] = None
    project_id: Optional[str] = None
    type: Optional[str] = None
    branch: Optional[str] = None
    release_strategy_type: Optional[str] = None
    analysis_type: Optional[str] = None
    exclusion_patterns: List[str] = field(default_factory=list)
    is_include_deployment: Optional[bool] = None
    date_range: Optional[str] = None
    job_name: Optional[str] = None
    fix_pattern: List[str] = field(default_factory=list)
    is_stage_type: Optional[bool] = None


@dataclass
class GitAnalysisDTO:
    """Git analysis data transfer object."""

    id: Optional[str] = None
    created_date: Optional[datetime] = None
    modify_date: Optional[datetime] = None
    created_user: Optional[str] = None
    modify_user: Optional[str] = None
    version: Optional[int] = None
    deleted_date: Optional[datetime] = None
    datasource_id: Optional[str] = None
    workspace_path: Optional[str] = None
    project_id: Optional[str] = None
    project_name: Optional[str] = None
    type: Optional[str] = None
    release_strategy_type: Optional[str] = None
    analysis_type: Optional[str] = None
    branch: Optional[str] = None
    exclusion_patterns: List[str] = field(default_factory=list)
    is_include_deployment: Optional[bool] = None
    date_range: Optional[str] = None
    job_name: Optional[str] = None
    fix_pattern: List[str] = field(default_factory=list)
    is_stage_type: Optional[bool] = None


@dataclass
class DoraAnalysisRequestDTO:
    """DORA analysis request DTO."""

    exclusion_patterns: List[str] = field(default_factory=list)
    job_name: Optional[str] = None
    fix_pattern: List[str] = field(default_factory=list)
    is_stage_type: Optional[bool] = None
    branch: Optional[str] = None


@dataclass
class JenkinsDoraAnalysisRequestDTO:
    """Jenkins DORA analysis request DTO."""

    datasource_id: Optional[str] = None
    ci_job_name: Optional[str] = None
    cd_job_name: Optional[str] = None
    parameter: Optional[str] = None
    commit_variable_key: Optional[str] = None
    release_strategy: Optional[str] = None
    release_pattern: Optional[str] = None
    analysis_type: Optional[str] = None
    hotfix_pattern: List[str] = field(default_factory=list)


# Deployment Models
@dataclass
class DeploymentRequestDTO:
    """Deployment request DTO."""

    analysis_id: Optional[str] = None
    clone_url: Optional[str] = None
    pipeline_start_at: Optional[datetime] = None
    last_commit_sha: Optional[str] = None
    deployment_type: Optional[str] = None
    analysis_type: Optional[str] = None
    deployed_at: Optional[datetime] = None
    name: Optional[str] = None
    title: Optional[str] = None
    target_branch: Optional[str] = None


@dataclass
class DeploymentDTO:
    """Deployment data transfer object."""

    id: Optional[str] = None
    created_date: Optional[datetime] = None
    modify_date: Optional[datetime] = None
    created_user: Optional[str] = None
    modify_user: Optional[str] = None
    version: Optional[int] = None
    deleted_date: Optional[datetime] = None
    analysis_id: Optional[str] = None
    clone_url: Optional[str] = None
    pipeline_start_at: Optional[datetime] = None
    last_commit_sha: Optional[str] = None
    deployment_type: Optional[str] = None
    deployed_at: Optional[datetime] = None
    author: Optional[str] = None
    name: Optional[str] = None
    title: Optional[str] = None
    analysis_type: Optional[str] = None
    release_strategy_type: Optional[str] = None
    is_stage_type: Optional[bool] = None
    target_branch: Optional[str] = None


# Qwiser Models
@dataclass
class TeamInfo:
    """Team information."""

    team_id: Optional[str] = None
    team_name: Optional[str] = None


@dataclass
class QwiserAnalysisRequestDTO:
    """Qwiser analysis request DTO."""

    datasource_id: Optional[str] = None
    project_key: Optional[str] = None
    branch: Optional[str] = None
    teams: List[TeamInfo] = field(default_factory=list)


# Defect Detection Models
@dataclass
class DefectDetectionRequest:
    """Defect detection request."""

    repo_name: Optional[str] = None
    branch: Optional[str] = None
    description: Optional[str] = None
    job_name: Optional[str] = None
    fixed_date: Optional[datetime] = None
    detected_date: Optional[datetime] = None


# External Test Models
@dataclass
class CreateExecutionRequest:
    """Create execution request."""

    execution_id: str
    status: str
    execution_time: int
    execution_start_date: str
    execution_end_date: str
    action_date: str
    application_id: Optional[str] = None
    scenario_id: Optional[str] = None
    scenario_name: Optional[str] = None
    scenario_description: Optional[str] = None
    module: Optional[str] = None
    environment: Optional[str] = None
    executed_by: Optional[str] = None
    team: Optional[str] = None


@dataclass
class ExternalExecutionResource:
    """External execution resource."""

    id: Optional[str] = None
    execution_id: Optional[str] = None
    status: Optional[str] = None
    execution_time: Optional[int] = None
    execution_start_date: Optional[datetime] = None
    execution_end_date: Optional[datetime] = None
    action_date: Optional[datetime] = None
    analysis_id: Optional[str] = None
    application_id: Optional[str] = None
    scenario_id: Optional[str] = None
    scenario_name: Optional[str] = None
    scenario_description: Optional[str] = None
    module: Optional[str] = None
    environment: Optional[str] = None
    executed_by: Optional[str] = None
    team: Optional[str] = None


@dataclass
class CreateDefectRequest:
    """Create defect request."""

    application_id: str
    problem_no: str
    detected_date: datetime
    fixed_date: datetime
    description: Optional[str] = None


@dataclass
class CreateCoverageRequest:
    """Create coverage request."""

    action_date: str
    application_id: str
    coverage_id: str
    coverage_rate: float
    total_line: int
    covered_line: int
    uncovered_line: int
    coverage_service: Optional[str] = None
    tool_type: Optional[str] = None
    team: Optional[str] = None
    created_by: Optional[str] = None


@dataclass
class ExternalCoverageResource:
    """External coverage resource."""

    id: Optional[str] = None
    action_date: Optional[datetime] = None
    application_id: Optional[str] = None
    coverage_id: Optional[str] = None
    analysis_id: Optional[str] = None
    coverage_service: Optional[str] = None
    tool_type: Optional[str] = None
    coverage_rate: Optional[float] = None
    total_line: Optional[int] = None
    covered_line: Optional[int] = None
    uncovered_line: Optional[int] = None
    team: Optional[str] = None
    created_by: Optional[str] = None


@dataclass
class CreateBugRequest:
    """Create bug request."""

    application_id: str
    bug_id: str
    name: str
    description: Optional[str] = None
    module: Optional[str] = None
    environment: Optional[str] = None
    created_by: Optional[str] = None
    team: Optional[str] = None
    created_date: Optional[str] = None
    updated_date: Optional[str] = None


@dataclass
class ExternalBugResource:
    """External bug resource."""

    id: Optional[str] = None
    action_date: Optional[datetime] = None
    application_id: Optional[str] = None
    analysis_id: Optional[str] = None
    bug_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    module: Optional[str] = None
    environment: Optional[str] = None
    created_by: Optional[str] = None
    team: Optional[str] = None
    bug_created_date: Optional[datetime] = None
    bug_updated_date: Optional[datetime] = None
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None


# Bulk Operation Models
@dataclass
class SyncGitAnalysisDTO:
    """Sync git analysis DTO."""

    team_id: Optional[str] = None
    delete_cancel_analysis: Optional[bool] = None
    team_analysis_branches: List[str] = field(default_factory=list)
    team_sonar_branches: List[str] = field(default_factory=list)


@dataclass
class BulkAnalysisPrepareRequest:
    """Bulk analysis prepare request."""

    datasource_id: Optional[str] = None
    branches: List[str] = field(default_factory=list)
    is_include_tags: Optional[bool] = None
    stages: List[str] = field(default_factory=list)
    tag_branch: Optional[str] = None


# API Key Models
@dataclass
class ApiKeyRequestDTO:
    """API key request DTO."""

    name: Optional[str] = None
    expire_date: Optional[datetime] = None


@dataclass
class ApiTokenDTO:
    """API token data transfer object."""

    id: Optional[str] = None
    created_date: Optional[datetime] = None
    modify_date: Optional[datetime] = None
    created_user: Optional[str] = None
    modify_user: Optional[str] = None
    version: Optional[int] = None
    deleted_date: Optional[datetime] = None
    name: Optional[str] = None
    expire_date: Optional[datetime] = None
    enabled: Optional[bool] = None
    token: Optional[str] = None
    expire: Optional[bool] = None


# Report Models
@dataclass
class MemberQualityStatistic:
    """Member quality statistic."""

    repository_count: Optional[int] = None
    total_issue: Optional[int] = None
    overall_score: Optional[int] = None
    overall_display_score: Optional[str] = None
    newly_added_score: Optional[int] = None
    newly_added_display_score: Optional[str] = None


@dataclass
class MemberQualityRepositoryStatistic:
    """Member quality repository statistic."""

    repository_name: Optional[str] = None
    technical_debt: Optional[MemberQualityStatistic] = None


@dataclass
class TeamMemberQualityStatistic:
    """Team member quality statistic."""

    member_name: Optional[str] = None
    member_id: Optional[str] = None
    role: Optional[str] = None
    technical_debt: Optional[MemberQualityStatistic] = None


@dataclass
class TeamQualityReportResponse:
    """Team quality report response."""

    technical_debt: Optional[MemberQualityStatistic] = None
    repository_activities: List[MemberQualityRepositoryStatistic] = field(default_factory=list)
    team_member_activities: List[TeamMemberQualityStatistic] = field(default_factory=list)


@dataclass
class MemberQualityReportResponse:
    """Member quality report response."""

    technical_debt: Optional[MemberQualityStatistic] = None
    repository_statistics: List[MemberQualityRepositoryStatistic] = field(default_factory=list)


@dataclass
class MemberPullRequestStatistic:
    """Member pull request statistic."""

    merged_pull_request_count: Optional[int] = None
    pull_request_size: Optional[int] = None
    needs_work_count: Optional[int] = None
    comment_count: Optional[int] = None


@dataclass
class MemberPullRequestRepositoryStatistic:
    """Member pull request repository statistic."""

    repository_name: Optional[str] = None
    statistic: Optional[MemberPullRequestStatistic] = None


@dataclass
class TeamMemberPullRequestStatistic:
    """Team member pull request statistic."""

    member_name: Optional[str] = None
    member_id: Optional[str] = None
    role: Optional[str] = None
    statistic: Optional[MemberPullRequestStatistic] = None


@dataclass
class TeamPullRequestReportResponse:
    """Team pull request report response."""

    statistic: Optional[MemberPullRequestStatistic] = None
    repository_statistics: List[MemberPullRequestRepositoryStatistic] = field(default_factory=list)
    team_member_statistics: List[TeamMemberPullRequestStatistic] = field(default_factory=list)


@dataclass
class MemberPullRequestReportResponse:
    """Member pull request report response."""

    statistic: Optional[MemberPullRequestStatistic] = None
    repository_statistics: List[MemberPullRequestRepositoryStatistic] = field(default_factory=list)


@dataclass
class WorkTypeStatisticsItem:
    """Work type statistics item."""

    value: Optional[int] = None
    percent: Optional[float] = None


@dataclass
class ImpactStatisticsItem:
    """Impact statistics item."""

    value: Optional[Any] = None
    ratio: Optional[float] = None


@dataclass
class MemberCommitStatistic:
    """Member commit statistic."""

    repository_count: Optional[int] = None
    total_commit: Optional[int] = None
    total_changes: Optional[int] = None
    add_line: Optional[int] = None
    delete_line: Optional[int] = None
    edit_line: Optional[int] = None
    churn: Optional[WorkTypeStatisticsItem] = None
    impact: Optional[ImpactStatisticsItem] = None
    efficiency: Optional[WorkTypeStatisticsItem] = None


@dataclass
class MemberRepositoryStatistic:
    """Member repository statistic."""

    repository_name: Optional[str] = None
    statistics: Optional[MemberCommitStatistic] = None


@dataclass
class TeamMemberCommitStatistic:
    """Team member commit statistic."""

    role: Optional[str] = None
    member_name: Optional[str] = None
    member_id: Optional[str] = None
    statistic: Optional[MemberCommitStatistic] = None


@dataclass
class MemberCommitReportResponse:
    """Member commit report response."""

    statistic: Optional[MemberCommitStatistic] = None
    repository_statistics: List[MemberRepositoryStatistic] = field(default_factory=list)


@dataclass
class TeamCommitReportResponse:
    """Team commit report response."""

    statistic: Optional[MemberCommitStatistic] = None
    repository_statistics: List[MemberRepositoryStatistic] = field(default_factory=list)
    team_member_activities: List[TeamMemberCommitStatistic] = field(default_factory=list)


# DORA Metrics Models
@dataclass
class DoraSummaryItemDTO:
    """DORA summary item DTO."""

    value: Optional[Any] = None
    formatted_value: Optional[str] = None


@dataclass
class DoraSummaryDeploymentDTO:
    """DORA summary deployment DTO."""

    title: Optional[str] = None
    pipeline_url: Optional[str] = None
    commit_count: Optional[int] = None
    pull_request_count: Optional[int] = None
    lead_time_for_changes: Optional[str] = None
    triggered_by: Optional[str] = None
    contributors: List[str] = field(default_factory=list)
    deployment_date: Optional[int] = None
    pipeline_name: Optional[str] = None
    status: Optional[str] = None
    development_time: Optional[int] = None
    waiting_for_deployment_time: Optional[int] = None
    deployment_time: Optional[int] = None


@dataclass
class DoraSummaryDTO:
    """DORA summary data transfer object."""

    lead_time_for_changes: Optional[DoraSummaryItemDTO] = None
    deployment_frequency: Optional[DoraSummaryItemDTO] = None
    change_failure_rate: Optional[DoraSummaryItemDTO] = None
    time_to_restore: Optional[DoraSummaryItemDTO] = None
    deployments: List[DoraSummaryDeploymentDTO] = field(default_factory=list)


# Response Models
@dataclass
class OobeyaResponse:
    """Generic Oobeya response."""

    version: Optional[str] = None
    reference_id: Optional[str] = None
    payload: Optional[Any] = None


@dataclass
class OobeyaResponseBoolean:
    """Oobeya response with boolean payload."""

    version: Optional[str] = None
    reference_id: Optional[str] = None
    payload: Optional[bool] = None


@dataclass
class PaginationResponse:
    """Pagination response."""

    contents: List[Any] = field(default_factory=list)
    size: Optional[int] = None
    page: Optional[int] = None
    total_elements: Optional[int] = None
    total_pages: Optional[int] = None
    is_last: Optional[bool] = None
    is_sorted: Optional[bool] = None
    header_filter: Dict[str, List[HeaderFilter]] = field(default_factory=dict)
