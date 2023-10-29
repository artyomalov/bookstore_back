from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BookSerializer
from rest_framework.permissions import AllowAny
from .models import Genre
from .serializers import GenreSerializer


class GenresAPI(APIView):
    """
    List all genres with related books
    """

    permission_classes = [AllowAny, ]

    def get(self, request, format=None):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)
