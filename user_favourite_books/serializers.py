from rest_framework.serializers import ModelSerializer
from .models import UserFavouriteBooks


class UserFavoriteBooksSerializer(ModelSerializer):
    class Meta:
        model = UserFavouriteBooks
        fields = ['user_liked_books']
