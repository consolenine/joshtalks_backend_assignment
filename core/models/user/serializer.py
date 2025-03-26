from rest_framework import serializers
from .model import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'mobile']
        extra_kwargs = {
            'password': {'write_only': True}
        }