from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserLikedBooks, UserCart, UserPurchasesList
from .serializers import UserLikedBooksSerializer, UserCartSerializer
from rest_framework.permissions import AllowAny


class UserLikedBooksAPI(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, id, format=None):
        liked_books = UserLikedBooks.objects.filter(user_id__id=id)[0]
        serializer = UserLikedBooksSerializer(liked_books)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        liked_books = UserLikedBooks.objects.filter(user_id__id=id)[0]
        data = {
            'book_slug': request.data.get('bookSlug'),
            'operation_type': request.data.get('operationType')
        }
        serializer = UserLikedBooksSerializer(liked_books, data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserCartAPI(APIView):
    permission_classes = [AllowAny, ]
    def get(self, request, id, format=None):
        cart = UserCart.objects.filter(user_id__id=id)[0]
        serializer = UserCartSerializer(cart)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        cart = UserCart.objects.filter(user_id__id=id)[0]
        if request.data.get('operationType') == 'add':
            data = {
                'operation_type': request.data.get('operationType'),
                'book_slug': request.data.get('bookSlug'),
            }
        else:
            data = {
                'operation_type': request.data.get('operationType'),
                'cart_item_id': request.data.get('cartItemId'),
            }
        serializer = UserCartSerializer(cart, data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
