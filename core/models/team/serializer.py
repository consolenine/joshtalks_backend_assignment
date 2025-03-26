from rest_framework import serializers
from .model import Team, TeamRoles


class TeamRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamRoles
        fields = ['role', 'user', 'team']

class TeamSerializer(serializers.ModelSerializer):
    members = TeamRolesSerializer(many=True, read_only=True)
    class Meta:
        model = Team
        fields = ['name', 'created_at', 'owner', 'members']