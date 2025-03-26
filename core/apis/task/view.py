from django.db import models
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from core.models import (
    Task, TaskSerializer,
    TaskAssignment, TaskAssignmentSerializer,
    IsManagerOrOwnerOrSelf
)


class TaskViewSet(ModelViewSet):
    """
    ViewSet to manage tasks
    """
    serializer_class = TaskSerializer
    permission_classes = [IsManagerOrOwnerOrSelf]

    def get_queryset(self):
        user_id = self.request.user.id
        return (Task.objects.filter(models.Q(created_by=user_id) | models.Q(assignments__user=user_id))
                .distinct())

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        """
        Returns the details of a task.
        """
        task = self.get_object()  # No need to pass `pk`
        serializer = self.serializer_class(task)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Creates a new task.
        """
        # add created_by automatically
        data = request.data.copy()
        data['created_by'] = request.user
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Updates an existing task.
        """
        task = self.get_object()
        serializer = self.serializer_class(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a task.
        """
        task = self.get_object()
        task.delete()
        return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        """
        Returns a list of all tasks.
        """
        tasks = self.get_queryset()
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TaskAssignmentViewSet(ModelViewSet):
    """
    ViewSet to manage task assignments
    """
    serializer_class = TaskAssignmentSerializer
    permission_classes = [IsManagerOrOwnerOrSelf]

    def get_queryset(self):
        user_id = self.request.user.id
        return TaskAssignment.objects.filter(user_id=user_id)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        """
        Returns the details of a task assignment.
        """
        task_assignment = self.get_object()  # No need to pass `pk`
        serializer = self.serializer_class(task_assignment)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Creates a new task assignment.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Updates an existing task assignment.
        """
        task_assignment = self.get_object()
        serializer = self.serializer_class(task_assignment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a task assignment.
        """
        task_assignment = self.get_object()
        task_assignment.delete()
        return Response({"message": "Task assignment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        """
        Returns a list of all task assignments.
        """
        task_assignments = self.get_queryset()
        serializer = self.serializer_class(task_assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)