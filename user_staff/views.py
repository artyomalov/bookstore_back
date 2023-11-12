from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserLikedBooks, UserCart, UserPurchasesList, CartItem
from .serializers import UserLikedBooksSerializer, UserCartSerializer, \
    CartItemSerializer
from rest_framework.permissions import AllowAny


class UserLikedBooksAPI(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, id, format=None):
        liked_books = UserLikedBooks.objects.filter(user_id__id=id)[0]
        serializer = UserLikedBooksSerializer(liked_books)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        liked_books = UserLikedBooks.objects.filter(user_id__id=id)[0]
        context = {
            'book_slug': request.data.get('bookSlug'),
            'operation_type': request.data.get('operationType')
        }
        print(context)
        serializer = UserLikedBooksSerializer(instance=liked_books,
                                              data={'id': id,
                                                    'user_liked_books': liked_books.user_liked_books},
                                              context=context)
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
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CartItemAPI(APIView):
    permission_classes = [AllowAny, ]

    def put(self, request, id, format=None):
        cart_item = CartItem.objects.get(pk=id)
        operation_type = request.data.get(
            'operation_type') if request.data.get(
            'operation_type') is not None else 'increase'
        data = {
            'id': cart_item.id,
            'relatedUserEmail': cart_item.user_cart.user_id.email,
            'book': cart_item.book,
            'coverType': cart_item.cover_type,
            'quantity': cart_item.quantity,
        }
        context = {'operation_type': operation_type, }
        serializer = CartItemSerializer(cart_item, context=context,
                                        data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
