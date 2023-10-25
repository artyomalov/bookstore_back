from user.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from usercart.serializers import UserCartSerializer


class SingupSerializer(serializers.ModelSerializer):
    '''
    Serializer that creates a new user
    '''

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        if validate_password(validated_data['password']) == None:
            password = make_password(validated_data.get('password', None))

            user = User.objects.create(
                email=validated_data.get('email', None),
                password=password,
            )

        return user


# class CustromTokenObtainPairSerializer(TokenObtainPairSerializer):

#     def validate(self, attrs):
#         data = super().validate(attrs)
#         refresh = self.get_token(self.user)
#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)
#         data['email'] = self.user.email
#         data['full_name'] = self.user.full_name
#         if self.user.avatar and hasattr(self.user.avater, 'url'):
#             data['avatar'] = self.user.avatar.url
#         return data
