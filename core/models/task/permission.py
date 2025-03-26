from rest_framework.permissions import BasePermission
from ..team import Team, TeamRoles

class IsManagerOrOwnerOrSelf(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH']:
            task_user_id = request.data.get('user_id')
            if task_user_id == request.user.id:
                return True

            team_ids = Team.objects.filter(owner=request.user).values_list('id', flat=True)
            manager_team_ids = TeamRoles.objects.filter(user=request.user, role=TeamRoles.Roles.MANAGER).values_list('team_id', flat=True)
            allowed_team_ids = set(team_ids).union(set(manager_team_ids))

            user_team_ids = TeamRoles.objects.filter(user_id=task_user_id).values_list('team_id', flat=True)
            return any(team_id in allowed_team_ids for team_id in user_team_ids)
        return True