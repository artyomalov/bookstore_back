from rest_framework.serializers import ModelSerializer
from .models import User
from usercart.serializers import UserCartSerializer
from userfavoritebooks.serializers import UserFavoriteBooksSerializer
from usercart.models import Comment
from rest_framework import serializers


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'avatar']


class AuthUserSerializer(ModelSerializer):

    usercart = UserCartSerializer(
        many=False, required=True, allow_null=False)
    # user_favorite_books = UserFavoriteBooksSerializer(
    #     many=True, required=True, allow_null=True)
    # list_of_users_purchases = ListOfUserPurchasesSerializer(
    #     many=False, required=True, allow_null=True)

    class Meta:

        model = User
        fields = ['email', 'avatar', 'full_name', 'usercart',
                  ]


# 'user_favorite_books', 'list_of_users_purchases'
