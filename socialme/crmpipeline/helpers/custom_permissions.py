from rest_framework.permissions import BasePermission
from crmpipeline.helpers.enums import UserRole
from crmpipeline.models import TeamMember
from crmpipeline.helpers.custom_exceptions import EditException

class CanEditTeam(BasePermission):
    """
    Custom permission class to check if the user is the owner of any active company.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view based on their company membership and role.
        Args:
            request (HttpRequest): The request object containing user information.
            view (View): The view being accessed.
        Returns:
            bool: True if the user is a member of the company and has the authorization, False otherwise.
        Raises:
            EditException: Raised when the user does not have the necessary permissions.
        """
        user = request.user
        data = request.data
        team_id = data.get("team_id")

        member_object = TeamMember.objects.filter(member=user, team_id=team_id).first()
        roles = [
            UserRole.ADMIN,
            UserRole.DISBURSER,
            UserRole.OWNER,
            UserRole.SUB_ADMIN,
        ]
        if member_object and (member_object.role in roles):
            return True
        raise EditException
