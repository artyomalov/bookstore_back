from rest_framework.serializers import ModelSerializer
from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'avatar']


class AuthUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'avatar', 'password', 'date_of_birth']
