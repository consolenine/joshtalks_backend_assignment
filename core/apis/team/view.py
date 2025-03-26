from django.db import models
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.generics import get_object_or_404

from core.models import Team, TeamSerializer, TeamRoles, TeamRolesSerializer, IsTeamOwnerOrManager


class TeamViewSet(ModelViewSet):
    """
    ViewSet to manage teams.
    """
    serializer_class = TeamSerializer
    permission_classes = (IsTeamOwnerOrManager,)

    def get_queryset(self):
        """
        Returns teams that the authenticated user is a part of or has created.
        """
        user_id = self.request.user.id
        return Team.objects.filter(models.Q(owner=user_id) | models.Q(members=user_id)).distinct()

    def get_object(self):
        """
        Retrieves a single team object, ensuring user has access.
        """
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        """
        Returns the details of a team.
        """
        team = self.get_object()
        serializer = self.serializer_class(team)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Creates a new team.
        """
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Updates an existing team.
        """
        team = self.get_object()
        serializer = self.serializer_class(team, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a team.
        """
        team = self.get_object()
        team.delete()
        return Response({"message": "Team deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        """
        Returns a list of all teams the user has access to.
        """
        teams = self.get_queryset()
        serializer = self.serializer_class(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamRolesViewSet(ModelViewSet):
    """
    ViewSet to manage team roles.
    """
    serializer_class = TeamRolesSerializer

    def get_queryset(self):
        """
        Returns all team roles for teams the authenticated user is a part of.
        """
        user_id = self.request.user.id
        return TeamRoles.objects.filter(user=user_id)

    def get_object(self):
        """
        Retrieves a single team role object, ensuring user has access.
        """
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        """
        Returns the details of a team role.
        """
        team_role = self.get_object()
        serializer = self.serializer_class(team_role)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Assigns a role to a user in a team.
        Only managers or owners can add members.
        """
        data = request.data
        team = get_object_or_404(Team, pk=data.get('team'))
        # Check if request user is manager or owner
        if not (team.owner == request.user or TeamRoles.objects.filter(team=team, user=request.user.id,
                                                                       role=TeamRoles.Roles.MANAGER).exists()):
            return Response({"detail": "Only team managers or owners can assign roles."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Updates an existing team role.
        Only team managers or owners can update roles.
        """
        team_role = self.get_object()

        # Ensure only owners or managers can change roles
        if not (team_role.team.owner == request.user or TeamRoles.objects.filter(team=team_role.team, user=request.user,
                                                                                 role=TeamRoles.Roles.MANAGER).exists()):
            return Response({"detail": "Only team managers or owners can update roles."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(team_role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Removes a user from a team.
        Only team managers or owners can remove members.
        """
        team_role = self.get_object()

        # Ensure only managers or owners can remove members
        if not (team_role.team.owner == request.user or TeamRoles.objects.filter(team=team_role.team, user=request.user,
                                                                                 role=TeamRoles.Roles.MANAGER).exists()):
            return Response({"detail": "Only team managers or owners can remove members."},
                            status=status.HTTP_403_FORBIDDEN)

        team_role.delete()
        return Response({"message": "User removed from team successfully"}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        """
        Returns a list of all team roles for teams the user is part of.
        """
        team_roles = self.get_queryset()
        serializer = self.serializer_class(team_roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
