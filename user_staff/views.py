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

    def get(self, request, pk, format=None):
        liked_books = UserLikedBooks.objects.get(pk=pk)
        serializer = UserLikedBooksSerializer(liked_books)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        liked_books = UserLikedBooks.objects.get(pk=pk)
        book_slug = request.data.get('bookSlug')
        in_list = request.data.get('inList')
        serializer = UserLikedBooksSerializer(instance=liked_books,
                                              data={'id': id,
                                                    'user_liked_books': liked_books.user_liked_books},
                                              context={
                                                  'book_slug': book_slug,
                                                  'in_list': in_list
                                              })
        if serializer.is_valid():
            serializer.save()
            addedBook = services.find_dict_in_list(find_by='slug',
                                                   find_value=book_slug,
                                                   array=serializer.data.get(
                                                       'user_liked_books'))
            if addedBook is not None:
                return Response(addedBook, status=status.HTTP_200_OK)
            dummy = {
                "id": 0,
                "title": "deleted",
                "slug": book_slug,
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
            return Response(dummy, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserCartAPI(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, pk, format=None):
        cart = UserCart.objects.get(pk=pk)
        serializer = UserCartSerializer(cart)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        cart = UserCart.objects.get(pk=pk)
        book_slug = request.data.get('book_slug')
        data = {
            'id': cart.id,
            'userCart': cart.cart_item.all()
        }

        if book_slug is not None:
            context = {
                'book_slug': request.data.get('bookSlug'),
                'cover_type': request.data.get('coverType'),
                'price': request.data.get('price')
            }
            serializer = UserCartSerializer(instance=cart, data=data,
                                            context=context)
            if serializer.is_valid():
                serializer.save()
                response = services.find_dict_in_list(find_by='bookSlug',
                                                      find_value=book_slug,
                                                      array=serializer.data)
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            cart_item_id = request.data.get('cartItemId')
            context = {
                'cart_item_id': cart_item_id,
            }
            serializer = UserCartSerializer(instance=cart, data=data,
                                            context=context)
            if serializer.is_valid():
                serializer.save()
                dummy = {
                    "id": cart_item_id,
                    "quantity": 0,
                    "title": "deleted",
                    "coverType": "deleted",
                    "coverImage": "deleted",
                    "price": 0,
                    "authors": [
                        {
                            "id": 0,
                            "name": "deleted"
                        }
                    ]
                }
                return Response(dummy, status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CartItemAPI(APIView):
    permission_classes = [AllowAny, ]

    def put(self, request, pk, format=None):
        cart_item = CartItem.objects.get(pk=pk)
        data = {
            'id': cart_item.id,
            'book': cart_item.book,
            'coverType': cart_item.cover_type,
            'quantity': cart_item.quantity,
            'price': cart_item.price,
        }
        context = {'increase': request.data.get('increase'), }
        serializer = CartItemSerializer(cart_item, context=context,
                                        data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserPurchasesAPI(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, pk, format=None):
        purchases_list = UserPurchasesList.objects.get(user_id__id=pk)
        serializer = UserPurchasesListSerializer(purchases_list)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        purchases_list = UserPurchasesList.objects.get(user_id__id=pk)
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

# from user.models import User
# u = User.objects.get(pk=2)
