from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Book, Genre
from .serializers import BookSerializer, GenreSerializer
from django.http import Http404


class BookList(APIView):
    """
    List all Books.
    """
    permission_classes = [AllowAny, ]

    def get(self, request, format=None):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class FoundBookList(APIView):
    """
    Look for requested book data using title for filter. Returns list of Book
    model instances.
    """

    permission_classes = [AllowAny]

    def get(self, request, slug, format=None):
        books = Book.objects.filter(slug__icontains=slug)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BookDetail(APIView):
    permission_classes = [AllowAny, ]

    def get_book(self, slug):
        try:
            return Book.objects.get(slug=slug)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        book = Book.objects.get(slug=slug)
        serializer = BookSerializer(book)
        return Response(serializer.data)


class GenresList(APIView):
    """
    List all genres.
    """

    permission_classes = [AllowAny, ]

    def get(self, request, format=None):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)
