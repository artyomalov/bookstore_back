# from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Book, Author, Comment, BookRaiting
from user.serializers import AuthUserSerializer, UserSerializer


class BookRatingSerializer(ModelSerializer):
    class Meta:
        model = BookRaiting
        fields = ['score', 'book_id']


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'biography']


class CommentSerializer(ModelSerializer):
    user = UserSerializer(many=False, reqired=True, allow_null=False)

    class Meta:
        model = Comment
        fields = ['created_at', 'comment_text', 'user']


class PublicBookSerializer(ModelSerializer):
    author = AuthorSerializer(many=True, required=True, allow_null=False)
    comments = CommentSerializer(many=True, required=False, allow_null=True)
    raitings = BookRatingSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Book
        fields = ['title', 'annotation', 'in_stock_quantity',
                  'genre', 'price', 'cover_image', 'author', 'comments']


class AuthBookSerializer(ModelSerializer):
    author = AuthorSerializer(many=True, required=True, allow_null=False)
    comments = CommentSerializer(many=True, required=False, allow_null=True)
    raitings = BookRatingSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Book
        fields = ['title', 'annotation', 'in_stock_quantity',
                  'genre', 'price', 'cover_image', 'author', 'comments', 'liked_by_user']
