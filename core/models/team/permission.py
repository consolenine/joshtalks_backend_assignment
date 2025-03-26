from rest_framework.permissions import BasePermission
from .model import TeamRoles


class IsTeamOwnerOrManager(BasePermission):
    """
    Custom permission:
    - Owners can delete the team
    - Managers can add/remove members
    - All members can view
    """

    def has_object_permission(self, request, view, obj):
        """
        Check user permissions based on request method and role in the team.
        """
        user = request.user

        # Owners can do everything (GET, DELETE, PATCH, etc.)
        if obj.owner == user:
            return True

        # Get user's role in the team
        team_role = TeamRoles.objects.filter(team=obj, user=user).first()

        # Allow GET (view access) for all members
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return team_role is not None  # All members can view

        # Allow DELETE only for team owners
        if request.method == "DELETE":
            return obj.owner == user

        # Allow adding/removing members only for managers
        if request.method in ["POST", "PATCH"] and team_role:
            return team_role.role == TeamRoles.Roles.MANAGER

        return False
