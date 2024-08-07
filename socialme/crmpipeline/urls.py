from django.urls import path
from crmpipeline.views import (
    MerchantView, TrackTaskView, TrackActivityView, TrackDealView, 
    AddTeamMemberView, RemoveTeamMemberView, UpdateTeamMemberRoleView, TeamMemberRoleView, 
    TeamMemberPermissionView, TeamMemberRolePermissionView, RolePermissionsView, SalesOfficerTeamView, 
    DealView, DealProgression, ManagePipelineStagesAPIView, ManagePipelineView, 
    SalesOfficersPipelines, CreateRolesAndPermissionsAPIView, ChangeDealStageView, 
    FetchCreatedDealsView, FetchCreatedActivitiesView, FetchCreatedTasksView, LeadView, SalesLeadView, HeadOfSalesView, SuperAdminView, ActivityView, TaskView,
    # FetchAllMerchants, SalesOfficerPipelinesAPIView, SalesOfficerView,
)


SALES_OFFICER_ENDPOINT = [
    # path("create-sales-officer/", SalesOfficerView.as_view()),
    # path("get-sales-officer/", SalesOfficerView.as_view()),
    # path("delete-sales-officer/", SalesOfficerView.as_view()),
    path("sales-officer-team/", SalesOfficerTeamView.as_view()),
]

SALES_LEAD_ENDPOINT = [
    path("create-sales-lead/", SalesLeadView.as_view()),
    path("get-sales-lead/", SalesLeadView.as_view()),
    path("delete-sales-lead/", SalesLeadView.as_view()),
]

HEAD_OF_SALES_ENDPOINT = [
    path("create-head-of-sales/", HeadOfSalesView.as_view()),
    path("get-head-of-sales/", HeadOfSalesView.as_view()),
    path("delete-head-of-sales/", HeadOfSalesView.as_view()),
]

SUPER_ADMIN_ENDPOINT = [
    path("create-super-admin/", SuperAdminView.as_view()),
    path("get-super-admin/", SuperAdminView.as_view()),
    path("delete-super-admin/", SuperAdminView.as_view()),
]

MERCHANT_ENDPOINT = [
    path("create-merchant/", MerchantView.as_view(), name="create_merchant"),
    path("get-merchant/", MerchantView.as_view()),
    # path("fetch-all-merchants/", FetchAllMerchants.as_view()),
    path("get-role-permissions", RolePermissionsView.as_view()),
]

PIPELINE_ENDPOINT = [
    path("manage-pipeline/<int:pipeline_id>/", ManagePipelineView.as_view()),
    path("edit-pipeline/<int:pipeline_id>/", ManagePipelineView.as_view()),
    path("partially-edit-pipeline/<int:pipeline_id>/", ManagePipelineView.as_view()),
    path("delete-pipeline/<int:pipeline_id>/", ManagePipelineView.as_view()),
    path("get-sales-officer-pipeline/", SalesOfficersPipelines.as_view()),
]

STAGE_ENDPOINT = [
    path("manage-pipeline-stage/", ManagePipelineStagesAPIView.as_view()), 
    path("update-pipeline-stage/<int:pipeline_id>/", ManagePipelineStagesAPIView.as_view()), 
    path("partially-update-pipeline-stage/<int:pipeline_id>/", ManagePipelineStagesAPIView.as_view()), 
    path("delete-pipeline-stage/<int:pipeline_id>/", ManagePipelineStagesAPIView.as_view()), 
]

LEAD_ENDPOINT = [
    path('create-lead/', LeadView.as_view()),
]

DEAL_ENDPOINT = [
    path("create-deal/", DealView.as_view()),
    path("get-deal/<str:unique_id>/", DealView.as_view()),
    path("delete-deal/<str:unique_id>/", DealView.as_view()),
    path("update-deal/<str:unique_id>/", DealView.as_view()),
    path("partially-update-deal/<str:unique_id>/", DealView.as_view()),
    path("track-deal/", TrackDealView.as_view(), name="track_deal_view"),
    path("fetch-created-deals/", FetchCreatedDealsView.as_view()),
    path("change-deal-stage/", ChangeDealStageView.as_view()),
    path("deal-progression/<int:deal_unique_id>/", DealProgression.as_view()), 
    path("delete-deal-progression/<int:deal_id>/", DealProgression.as_view()), 
]

ACTIVITY_ENDPOINT = [
    path("create-activity/", ActivityView.as_view()),
    path("track-activity/", TrackActivityView.as_view()),
    path("get-activity/", FetchCreatedActivitiesView.as_view()),
]

TASK_ENDPOINT = [
    path("create-task/", TaskView.as_view()),
    path("track-task/<int:task_id>/", TrackTaskView.as_view()), 
    path("get-task/<int:task_id>/", FetchCreatedTasksView.as_view()),
]

PERMISSIONS_ENDPOINT = [
    path("team-member-role-permissions/", TeamMemberRolePermissionView.as_view()),
    path("team-member-permission/", TeamMemberPermissionView.as_view()),
    path("role-permissions/", RolePermissionsView.as_view()),
    path("create-roles-and-permissions/", CreateRolesAndPermissionsAPIView.as_view()),
]

TEAM_ENDPOINT = [
    path("add-team-member/", AddTeamMemberView.as_view()),
    path("remove-team-member/<str:email>/", RemoveTeamMemberView.as_view()),
    path("update-team-member-role/<int:id>/", UpdateTeamMemberRoleView.as_view()),
    path("team-member-role/", TeamMemberRoleView.as_view()),
    path("team-member-permissions/<int:id>/", TeamMemberPermissionView.as_view()),
    path("team-role-member-permissions/<int:id>/", TeamMemberRolePermissionView.as_view()),
]


urlpatterns = [
    *SALES_OFFICER_ENDPOINT,
    *SALES_LEAD_ENDPOINT,
    *HEAD_OF_SALES_ENDPOINT,
    *SUPER_ADMIN_ENDPOINT,
    *MERCHANT_ENDPOINT,
    *PIPELINE_ENDPOINT,
    *STAGE_ENDPOINT,
    *DEAL_ENDPOINT,
    *ACTIVITY_ENDPOINT,
    *TASK_ENDPOINT,
    *PERMISSIONS_ENDPOINT,
    *TEAM_ENDPOINT,
    *LEAD_ENDPOINT,
]

