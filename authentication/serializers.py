from user.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password


class SingupSerializer(serializers.ModelSerializer):
    '''
    Serializer that create a new user
    '''

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'password', 'date_of_birth']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if validate_password(validated_data['password']) == None:
            password = make_password(validated_data.get('password', None))

            user = User.objects.create(
                email=validated_data.get('email', None),
                password=password,
                full_name=validated_data.get('full_name', None),
                date_of_birth=validated_data.get('date_of_birth', None),
                avatar=validated_data.get('avatar', None)
            )

        return user
