from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from core.models import User, UserSerializer


class UserViewSet(ModelViewSet):
    """
    ViewSet to manage tasks
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return []
        return [permission() for permission in self.permission_classes]

    def retrieve(self, request, *args, **kwargs):
        """
        Returns the details of a user
        """
        user = self.get_object()
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Creates a new user
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)