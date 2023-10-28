__all__ = ['BookRatingSerializer', 'AuthorSerializer', 'BookSerializer']

from rest_framework.serializers import ModelSerializer
from .models import Book, Author, BookRaiting, Comment


class BookRatingSerializer(ModelSerializer):
    class Meta:
        model = BookRaiting
        fields = ['score']


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'biography']


class BookSerializer(ModelSerializer):
    author = AuthorSerializer(many=True, required=True, allow_null=False,
                              source='author_ids')
    raitings = BookRatingSerializer(many=True, required=False,
                                    allow_null=True)

    class Meta:
        model = Book
        fields = ['title', 'annotation', 'in_stock_quantity',
                  'genre', 'price', 'cover_image', 'author', 'raitings']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['created_at', 'comment_text', 'user', 'book']
