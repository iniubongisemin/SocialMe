from django.urls import path
from crmpipeline.views import (
    MerchantView, FetchAllMerchants, TrackTaskView, TrackActivityView, TrackDealView, \
    AddTeamMemberView, RemoveTeamMemberView, UpdateTeamMemberRoleView, TeamMemberRoleView, \
    TeamMemberPermissionView, TeamMemberRolePermissionView, RolePermissionsView, SalesOfficerTeamView, \
    SalesOfficerApiView, DealApiView, DealProgression, ManagePipelineStagesAPIView, ManagePipelineAPIView, \
    SalesOfficerPipelinesAPIView, SalesOfficersPipelines, CreateRolesAndPermissionsAPIView, ChangeDealStageView, \
    FetchCreatedDealsView, FetchCreatedActivitiesView, FetchCreatedTasksView,
)


SALES_OFFICER_ENDPOINT = [
    path("sales-officer/", SalesOfficerApiView.as_view()),
    path("sales-officer-team/", SalesOfficerTeamView.as_view()),
]

MERCHANT_ENDPOINT = [
    path("create-merchant/", MerchantView.as_view(), name="create_merchant"),
    path("get-merchant/", MerchantView.as_view()),
    path("fetch-all-merchants/", FetchAllMerchants.as_view()),
]

PIPELINE_ENDPOINT = [
    path("manage-pipeline/", ManagePipelineAPIView.as_view()),
    path("get-sales-officer-pipelines/", SalesOfficerPipelinesAPIView.as_view()),
    path("get-sales-officer-pipeline/", SalesOfficersPipelines.as_view()),
]

STAGE_ENDPOINT = [
    path("manage-pipeline-stage/", ManagePipelineStagesAPIView.as_view()), 
]

DEAL_ENDPOINT = [
    path("deal/", DealApiView.as_view()),
    path("deals/<str:unique_id>/", DealApiView.as_view()),
    path("track-deal/", TrackDealView.as_view(), name="track_deal_view"),
    path("fetch-created-deals/", FetchCreatedDealsView.as_view()),
    path("change-deal-stage/", ChangeDealStageView.as_view()),
    path("deal-progression/", DealProgression.as_view()), 
]

ACTIVITY_ENDPOINT = [
    path("track-activity/", TrackActivityView.as_view()),
    path("get-activity/", FetchCreatedActivitiesView.as_view()),
]

TASK_ENDPOINT = [
    path("track-task/", TrackTaskView.as_view()), 
    path("fetch-created-task/", FetchCreatedTasksView.as_view()),
]

PERMISSIONS_ENDPOINT = [
    path("team-member-role-permissions/", TeamMemberRolePermissionView.as_view()),
    path("team-member-permission/", TeamMemberPermissionView.as_view()),
    path("role-permissions/", RolePermissionsView.as_view()),
    path("create-roles-and-permissions/", CreateRolesAndPermissionsAPIView.as_view()),
]

TEAM_ENDPOINT = [
    path("add-team-member/", AddTeamMemberView.as_view()),
    path("remove-team-member/", RemoveTeamMemberView.as_view()),
    path("update-team-member-role/", UpdateTeamMemberRoleView.as_view()),
    path("team-member-role/", TeamMemberRoleView.as_view()),
]


urlpatterns = [
    *SALES_OFFICER_ENDPOINT,
    *MERCHANT_ENDPOINT,
    *PIPELINE_ENDPOINT,
    *STAGE_ENDPOINT,
    *DEAL_ENDPOINT,
    *ACTIVITY_ENDPOINT,
    *TASK_ENDPOINT,
    *PERMISSIONS_ENDPOINT,
    *TEAM_ENDPOINT,
]

