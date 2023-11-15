from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserLikedBooks, UserCart, UserPurchasesList, CartItem
from .serializers import UserLikedBooksSerializer, UserCartSerializer, \
    CartItemSerializer, UserPurchasesListSerializer
from rest_framework.permissions import AllowAny
import services


class UserLikedBooksAPI(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, id, format=None):
        liked_books = UserLikedBooks.objects.get(user_id__id=id)
        serializer = UserLikedBooksSerializer(liked_books)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        liked_books = UserLikedBooks.objects.get(user_id__id=id)
        book_slug = request.data.get('bookSlug')
        serializer = UserLikedBooksSerializer(instance=liked_books,
                                              data={'id': id,
                                                    'user_liked_books': liked_books.user_liked_books},
                                              context={
                                                  'book_slug': book_slug,
                                              })
        if serializer.is_valid():
            serializer.save()
            addedBook = services.find_dict_in_list(find_by='slug',
                                                   find_value=book_slug,
                                                   array=serializer.data.get(
                                                       'user_liked_books'))
            if addedBook is not None:
                return Response(addedBook, status=status.HTTP_200_OK)
            response_deleted = {
                "id": 0,
                "title": "deleted",
                "slug": "deleted",
                "authors": [
                    {
                        "id": 0,
                        "name": "deleted"
                    },
                ],
                "hardcoverPrice": 0,
                "paperbackPrice": 0,
                "coverImage": "deleted"
            }
            return Response(response_deleted, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserCartAPI(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, id, format=None):
        cart = UserCart.objects.get(user_id__id=id)
        serializer = UserCartSerializer(cart)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        cart = UserCart.objects.get(user_id__id=id)
        data = {
            'id': cart.id,
            'userCart': cart.cart_item.all()
        }
        if request.data.get('operationType') == 'add':
            context = {
                'operation_type': request.data.get('operationType'),
                'book_slug': request.data.get('bookSlug'),
                'cover_type': request.data.get('coverType'),
                'price': request.data.get('price')
            }
        else:
            context = {
                'operation_type': request.data.get('operationType'),
                'cart_item_id': request.data.get('cartItemId'),
            }
        serializer = UserCartSerializer(instance=cart, data=data,
                                        context=context)
        response = {'completed': 'adding'} if request.data.get(
            'operationType') == 'add' else {'completed': 'removal'}
        if serializer.is_valid():
            serializer.save()
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CartItemAPI(APIView):
    permission_classes = [AllowAny, ]

    def put(self, request, id, format=None):
        cart_item = CartItem.objects.get(pk=id)
        operation_type = request.data.get(
            'operationType') if request.data.get(
            'operationType') is not None else 'increase'
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
            return Response({'updated': True}, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserPurchasesAPI(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, id, format=None):
        purchases_list = UserPurchasesList.objects.get(user_id__id=id)
        serializer = UserPurchasesListSerializer(purchases_list)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        purchases_list = UserPurchasesList.objects.get(user_id__id=id)
        data = {
            'id': purchases_list.id,
            'purchases': purchases_list.purchase_items.all()
        }
        context = {'cart_items_ids': request.data.get('cartItemIds')}
        serializer = UserPurchasesListSerializer(instance=purchases_list,
                                                 data=data,
                                                 context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
