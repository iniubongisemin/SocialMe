# from django.http import Http404
# from django.shortcuts import get_object_or_404
# from rest_framework import permissions
# from django.db import transaction
# from crmpipeline.models import (
#     SalesOfficer,
#     TeamMemberPermission,
#     TeamMemberRolePermission,
#     TeamMemberRole,
# )
# from users.models import TeamMember
# from rest_framework.exceptions import PermissionDenied


# class CustomPermission(permissions.BasePermission):
#     def __init__(self, required_roles_map):
#         super().__init__()
#         self.required_roles_map = required_roles_map

#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
        
#         try:
#             # Get recruiter
#             recruiter = get_object_or_404(SalesOfficer, user=request.user)

#             # Get user's role
#             team_member = TeamMember.objects.get(member=recruiter)
#             user_role = team_member.role.role.name

#             # Check if the user is an admin
#             if user_role == "ADMIN":
#                 return True
            
#             # Get permissions associated with the user's role
#             role_permissions = team_member.role.permission.all()

#             # Get the required roles for the current HTTP method
#             required_roles = self.required_roles_map.get(request.method, [])

#             # Check if the user has any of the required roles
#             has_permission = any(permission.name in required_roles for permission in role_permissions)
#             if not has_permission:
#                 raise PermissionDenied("User does not have the required permissions.")

#             return True

#         except SalesOfficer.DoesNotExist:
#             raise PermissionDenied("Sales Officer. Ensure the user is associated with a recruiter account.")
         
#         except TeamMember.DoesNotExist:
#             raise PermissionDenied("Team role not found for the user. Ensure the Sales Officer is assigned to a team with an appropriate role")
        

# # Define the required roles for each HTTP method
# merchants_progress_roles_map = {
#     "POST": ["Can Progress Merchants", "Can Move Merchants To Group"],
#     "DELETE": ["Can Remove Merchants From Stage"],
# }

# deal_roles_map = {
#     "POST": ["Can Create Deal"],
#     "DELETE": ["Can Delete Deal"],
#     "PUT": ["Can Edit Deal"],
#     "PATCH": ["Can Edit Deal"],
# }

# stage_roles_map = {
#     "POST": ["Can Create Stage"],
#     "PUT": ["Can Edit Stage"],
#     "PATCH": ["Can Edit Stage"],
#     "DELETE": ["Can Delete Stage"],
# }

# filter_merchants_roles_map = {
#     "POST": ["Can Move New Merchant To Group"],
# }

# pipeline_roles_map = {
#     "POST": ["Can Create Pipeline"],
#     "PUT": ["Can Edit Pipeline"],
#     "DELETE": ["Can Delete Pipeline"],
# }

# class CanManageMerchantsProgress(CustomPermission):
#     def __init__(self):
#         super().__init__(merchants_progress_roles_map)


# class CanManageDeal(CustomPermission):
#     def __init__(self):
#         super().__init__(deal_roles_map)


# class CanManageStage(CustomPermission):
#     def __init__(self):
#         super().__init__(stage_roles_map)


# class CanManagePipeline(CustomPermission):
#     def __init__(self):
#         super().__init__(pipeline_roles_map)


# @transaction.atomic
# def create_roles_and_permissions(merchant=None, **kwargs):
#     roles_permissions_mapping = {
#         'SALES LEAD': [
#             'Can Create Deal',
#             'Can Edit Deal',
#             'Can Delete Deal',
#             'Can Create Pipeline',
#             'Can Edit Pipeline',
#             'Can Delete Pipeline',
#             'Can Create Stage',
#             'Can Edit Stage',
#             'Can Delete Stage',
#             'Can Move Merchant To Group',
#         ],
#         'ADMIN': [],
#         'MEMBER': [],
#         'SALES OFFICER': [
#             'Can Create Deal',
#             'Can Edit Deal',
#             'Can Delete Deal',
#             'Can Create Pipeline',
#             'Can Edit Pipeline',
#             'Can Delete Pipeline',
#             'Can Create Stage',
#             'Can Edit Stage',
#             'Can Delete Stage',
#             'Can Move Merchant To Group'
#         ],
#     }

#     for role_name, permissions_list in roles_permissions_mapping.items():
#         role, created = TeamMemberRole.objects.get_or_create(name=role_name)
#         role_permission, created = TeamMemberRolePermission.objects.get_or_create(role=role)
#         for permission_name in permissions_list:
#             permission, created = TeamMemberPermission.objects.get_or_create(name=permission_name)
#             role_permission.permission.add(permission)
#             if merchant is not None:
#                 role_permission.merchant = merchant