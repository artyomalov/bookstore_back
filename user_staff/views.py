import json
import requests
import services
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import UserLikedBooks, UserCart, UserPurchasesList, CartItem
from .serializers import UserLikedBooksSerializer, UserCartSerializer, \
    CartItemSerializer, UserPurchasesListSerializer
from rest_framework.permissions import AllowAny


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
                                              data={'id': id},
                                              context={
                                                  'book_slug': book_slug,
                                                  'in_list': in_list
                                              })
        if serializer.is_valid():
            serializer.save()

            def compare_slug(element):
                if element['slug'] == book_slug:
                    return True
                return False

            added_book = services.find_dict_in_list(array=serializer.data.get(
                'likedList'), compare_function=compare_slug)
            if added_book is not None:
                return Response(added_book, status=status.HTTP_200_OK)
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
        book_slug = request.data.get('bookSlug')
        data = {
            'id': cart.id,
            'userCart': cart.cart_item.all()
        }

        if book_slug is not None:
            cover_type = request.data.get('coverType')
            context = {
                'book_slug': request.data.get('bookSlug'),
                'cover_type': request.data.get('coverType'),
                'price': request.data.get('price')
            }
            serializer = UserCartSerializer(instance=cart, data=data,
                                            context=context)
            if serializer.is_valid():
                serializer.save()

                def compare_slug_and_cover_type(element):
                    if (element['slug'] == book_slug and
                            element['coverType'] == cover_type):
                        return True
                    return False

                cart_item = services.find_dict_in_list(
                    array=serializer.data.get('cartItemsList'),
                    compare_function=compare_slug_and_cover_type)

                response = {
                    'cartItem': cart_item,
                    'total': serializer.data.get('total')
                }

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
                data = serializer.data
                total = data.get('total')
                response = {
                    'cartItem': dummy,
                    'total': total
                }
                return Response(response, status=status.HTTP_200_OK)
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
            data = serializer.data
            total = data.get('total')
            response = {
                'cartItem': data,
                'total': total
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserPurchasesAPI(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, pk, format=None):
        purchases_list = UserPurchasesList.objects.get(pk=pk)
        serializer = UserPurchasesListSerializer(purchases_list)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        purchases_list = UserPurchasesList.objects.get(pk=pk)
        cart_items_ids = request.data.get('cartItemsIds')
        cart_items_query = CartItem.objects.filter(
            pk__in=[*cart_items_ids])
        cart_data_for_purchases = []
        for cart_item in cart_items_query:
            book = cart_item.book
            quantity = cart_item.quantity
            cover_type = cart_item.cover_type
            purchase_data = f'&text=New book.\nBook title: {book.title}.\nQuantity: {quantity}.\nCover type: {cover_type}.\nUser email: {cart_item.user_cart.user_id.email}'
            try:
                response = requests.get(
                    settings.TELEGRAM_API + purchase_data).content
                response_data = json.loads(response)
                if response_data.get('ok') is not True:
                    raise Exception("Can't send data to TG")
                cart_data_for_purchases.append(
                    {
                        'book': book,
                        'quantity': quantity,
                        'cover_type': cover_type
                    }
                )
            except Exception as error:
                return Response({error: error},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = UserPurchasesListSerializer(
            instance=purchases_list,
            data={},
            context={'cart_data_for_purchases': cart_data_for_purchases}
        )
        if serializer.is_valid():
            serializer.save()
            cart_items_query.delete()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# from user.models import User
# u = User.objects.get(pk=2)
