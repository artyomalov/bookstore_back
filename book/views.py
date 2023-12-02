from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Avg
from .models import Book, Genre, Comment, Rating
from .serializers import BookSerializer, CommentSerializer, GenreSerializer, \
    RatingSerializer
from django.core.paginator import Paginator


class BookList(APIView):
    """
    List Books depends on selected genres, selected price and
    selected sort type.
    Default values are all genres, price from 0 to 1000 and sort by id.
    """
    permission_classes = [AllowAny, ]

    def get(self, request, format=None):
        genres_ids_filter = [
            *request.query_params.getlist('genre_id')]
        if len(genres_ids_filter) == 0:
            genres_ids_filter = []
            genres_dicts_list = Genre.objects.values('id')
            for genre_dict in genres_dicts_list:
                genres_ids_filter.append(genre_dict.get('id'))
        sort_type = request.query_params.get(
            'sort_type') if request.query_params.get(
            'sort_type') is not None else 'id'
        min_price = request.query_params.get(
            'min_price') if request.query_params.get(
            'min_price') is not None else 0
        max_price = request.query_params.get(
            'max_price') if request.query_params.get(
            'max_price') is not None else 100
        page = request.query_params.get('page') if request.query_params.get(
            'page') is not None else 1
        books_queryset = Book.objects.filter(
            genres__id__in=[*genres_ids_filter],
            hardcover_price__range=(min_price, max_price))
        if sort_type == 'rating':
            books_queryset = books_queryset.annotate(
                rating_avg=Avg('rating__rate', default=0)).order_by(
                '-rating_avg').distinct()
        else:
            books_queryset = books_queryset.order_by(
                sort_type).distinct()
        paginator = Paginator(books_queryset, per_page=12)
        serializer = BookSerializer(paginator.page(page), many=True)
        return Response({
            'books': serializer.data,
            'pagesCount': paginator.num_pages,
            'hasNext': paginator.page(page).has_next(),
            'hasPrevious': paginator.page(page).has_previous()
        })


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
        return Response({
            'books': serializer.data,
            'pagesCount': 1,
            'hasNext': False,
            'hasPrevious': False,
        })


class FoundBooksList(APIView):
    """
    Look for requested book data using title for filter. Returns list of Book
    model instances.
    """

    permission_classes = [AllowAny]

    def get(self, request, slug, format=None):
        page = request.query_params.get('page') if request.query_params.get(
            'page') is not None else 1
        books_queryset = Book.objects.filter(slug__icontains=slug)
        paginator = Paginator(books_queryset, per_page=4)
        serializer = BookSerializer(paginator.page(page), many=True)
        return Response({
            'books': serializer.data,
            'pagesCount': paginator.num_pages,
            'hasNext': paginator.page(page).has_next(),
            'hasPrevious': paginator.page(page).has_previous()
        })


class CreateComment(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        validated_data = {'text': request.data.get('commentText')}
        context = {
            'user_id': request.data.get('userId'),
            'book_id': request.data.get('bookId')
        }
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
            rate_dict = {'rate__avg': 0}
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
