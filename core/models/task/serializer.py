from rest_framework import serializers
from .model import Task, TaskAssignment
from ..user import UserSerializer


class TaskSerializer(serializers.ModelSerializer):
    assigned_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description',
            'created_at', 'task_type', 'task_type_other',
            'completed_at', 'status', 'assigned_users'
        ]

        extra_kwargs = {
            'completed_at': {'read_only': True}
        }

    def validate(self, data):
        if data['task_type'] == 'other' and not data.get('task_type_other'):
            raise serializers.ValidationError({"task_type_other": "This field is required."})
        return data

class TaskAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAssignment
        fields = ['id', 'user', 'task', 'status', 'assigned_at']