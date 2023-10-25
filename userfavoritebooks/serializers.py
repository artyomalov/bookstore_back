from rest_framework.serializers import ModelSerializer
from .models import UserFavoriteBooks


class UserFavoriteBooksSerializer(ModelSerializer):
    class Meta:
        model = UserFavoriteBooks
        fields = ['user_liked_books']
