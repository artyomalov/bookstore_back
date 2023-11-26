from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Avg
from .models import Book, Genre, Comment, Rating
from .serializers import BookSerializer, CommentSerializer, GenreSerializer, \
    RatingSerializer


class BookList(APIView):
    """
    List all Books.
    """
    permission_classes = [AllowAny, ]

    def get(self, request, format=None):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class GetSimularBooksByGenre(APIView):
    """
    Get simular books by genre
    """
    permission_classes = [AllowAny]

    def get(self, request, slug, format=None):
        genres_query = Book.objects.values('genres').filter(
            slug=slug)
        genres_ids = []

        for genre_dict in genres_query:
            genres_ids.append(genre_dict['genres'])

        books = Book.objects.filter(genres__id__in=[*genres_ids]).exclude(
            slug=slug)
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


class CreateComment(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        validated_data = {'text': request.data.get('commentText')}
        context = {
            'user_id': request.data.get('userId'),
            'book_id': request.data.get('bookId')
        }
        print(request.data)
        serializer = CommentSerializer(data=validated_data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetComments(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug, format=None):
        comments_list = Comment.objects.filter(book__slug=slug)
        serializer = CommentSerializer(comments_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenresList(APIView):
    """
    List all genres.
    """

    permission_classes = [AllowAny, ]

    def get(self, request, format=None):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)


class GetAverageRating(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, book_id, format=None):
        rate_dict = Book.objects.get(pk=book_id).rating_set.all().aggregate(
            Avg('rate'))
        if rate_dict.get('rate__avg') is None:
            return 0
        return Response({'averageRating': rate_dict.get('rate__avg')},
                        status=status.HTTP_200_OK)


class CreateRating(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, format=None):
        validated_data = {'rate': request.data.get('rate')}
        user_id = request.data.get('userId')
        book_id = request.data.get('bookId')

        rating_model = Rating.objects.filter(
            user_id=request.data.get('userId'),
            book_id=request.data.get('bookId')).first()
        if rating_model:
            serializer = RatingSerializer(instance=rating_model,
                                          data=validated_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = RatingSerializer(data=validated_data, context={
            'user_id': user_id,
            'book_id': book_id
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
