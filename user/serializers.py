from .models import User
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    fullName = serializers.CharField(allow_blank=True, allow_null=True,
                                     source='full_name')
    avatar = serializers.ImageField(required=False)


class AuthorizedUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    fullName = serializers.CharField(allow_blank=True, allow_null=True,
                                     source='full_name')
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()
    avatar = Base64ImageField(required=False, allow_null=True)
    userFavoriteBooks = serializers.SerializerMethodField(
        method_name='get_favourite')
    userCart = serializers.SerializerMethodField(
        method_name='get_cart')
    userPurchases = serializers.SerializerMethodField(
        method_name='get_purchases'
    )

    def get_favourite(self, instance):
        try:
            user_favourite_books = instance.favourite.user_liked_books.all()
            return [{
                'id': book.id,
                'title': book.title,
                'authors': [{
                    'name': author.name,
                } for author in book.authors.all()],
                'price': book.price,
                'coverImage': book.cover_image.url
            } for book in user_favourite_books]
        except Exception as error:
            print(error)
            return []

    def get_cart(self, instance):
        cart_items_query = instance.cart.cart_item.all()

        user_cart = [{
            'quantity': cart_item.quantity,
            'title': cart_item.book.title,
            'price': cart_item.book.price,
            'coverImage': cart_item.book.cover_image.url,
            'authors': [{
                'name': author.name,
            } for author in cart_item.book.authors.all()],
        } for cart_item in cart_items_query]

        return user_cart

    def get_purchases(self, instance):
        user_purchases_query = instance.purchases.purchase_item.all()

        purchase_items = [{
            'quantity': purchase_item.quantity,
            'bought_time': purchase_item.bought_time,
            'title': purchase_item.book.title,
            'coverImage': purchase_item.book.cover_image.url,
            'authors': [{
                'name': author.name,
            } for author in purchase_item.book.authors.all()],
        } for purchase_item in user_purchases_query]

        return purchase_items

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
