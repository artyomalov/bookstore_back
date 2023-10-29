from user.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user_staff.models import UserCart, UserPurchasesList, UserFavouriteBooks


class SignupSerializer(serializers.ModelSerializer):
    """
     Serializer that creates a new user
     """

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

            UserCart.objects.create(user_id=user)
            UserPurchasesList.objects.create(user_id=user)
            UserFavouriteBooks.objects.create(user_id=user)
        return user
