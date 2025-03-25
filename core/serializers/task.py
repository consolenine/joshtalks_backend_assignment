from rest_framework import serializers
from core.serializers.user import UserSerializer
from core.models import Task

class TaskSerializer(serializers.ModelSerializer):
    assigned_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'created_at', 'task_type', 'completed_at', 'status', 'assigned_users']

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['name', 'description', 'task_type', 'status']