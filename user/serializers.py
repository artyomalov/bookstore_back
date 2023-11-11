from .models import User
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.db.models import F


class AuthorizedUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    fullName = serializers.CharField(allow_blank=True, allow_null=True,
                                     source='full_name')
    email = serializers.EmailField(max_length=255)
    avatar = Base64ImageField(required=False, allow_null=True)
    # userFavoriteBooks = serializers.SerializerMethodField(
    #     method_name='get_favorite')
    # userCart = serializers.SerializerMethodField(
    #     method_name='get_cart')
    # userPurchases = serializers.SerializerMethodField(
    #     method_name='get_purchases'
    # )

    # def get_favorite(self, instance):
    #     user_favorite_books = instance.favorite.user_liked_books.all()
    #     return [{
    #         'id': book.id,
    #         'title': book.title,
    #         'authors': [{
    #             'name': author.name,
    #         } for author in book.authors.all()],
    #         'hardcoverPrice': book.hardcover_price,
    #         'paperbackPrice': book.paperback_price,
    #         'coverImage': book.cover_image.url
    #     } for book in user_favorite_books]

    # def get_cart(self, instance):
    #     cart_items_query = instance.cart.cart_item.all()
    #
    #     user_cart = [{
    #         'quantity': cart_item.quantity,
    #         'title': cart_item.book.title,
    #         'hardcoverPrice': cart_item.hardcover_price,
    #         'paperbackPrice': cart_item.paperback_price,
    #         'coverImage': cart_item.book.cover_image.url,
    #         'authors': [{
    #             'name': author.name,
    #         } for author in cart_item.book.authors.all()],
    #     } for cart_item in cart_items_query]
    #
    #     return user_cart
    #
    # def get_purchases(self, instance):
    #     user_purchases_query = instance.purchases.purchase_item.all()
    #
    #     purchase_items = [{
    #         'quantity': purchase_item.quantity,
    #         'bought_time': purchase_item.bought_time,
    #         'title': purchase_item.book.title,
    #         'coverImage': purchase_item.book.cover_image.url,
    #         'authors': [{
    #             'name': author.name,
    #         } for author in purchase_item.book.authors.all()],
    #     } for purchase_item in user_purchases_query]
    #
    #     return purchase_items

    def update(self, instance: User, validated_data):
        instance.full_name = validated_data.get('full_name',
                                                instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.avatar = validated_data.get('avatar', instance.avatar)

# def update_image_field(image_byte_string, path_to_save):
#     from PIL import Image
#     import base64
#     from io import BytesIO
#     image_name = 'image_name'
#     image_data = image_byte_string[image_byte_string.index(',') + 1]
#     data_decoded = base64.b64decode(image_data)
#     image = Image.open(BytesIO(data_decoded))
#     output_image = image.convert('RGB')
#     output_image.save(f'{path_to_save}{image_name}')
#     return f'media/{path_to_save}{image_name}'
