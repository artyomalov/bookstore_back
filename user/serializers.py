from .models import User
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.db.models import F


class AuthorizedUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    fullName = serializers.CharField(allow_blank=True, allow_null=True,
                                     source='full_name')
    email = serializers.EmailField(max_length=255)
    avatar = serializers.SerializerMethodField(required=False,
                                               allow_null=True, method_name='get_avatar')
    userLikedId = serializers.SerializerMethodField(read_only=True,
                                                    method_name='get_liked_id')
    userCartId = serializers.SerializerMethodField(read_only=True,
                                                   method_name='get_cart_id')
    userPurchasesId = serializers.SerializerMethodField(read_only=True,
                                                        method_name='get_purchases_id')

    def update(self, instance: User, validated_data):
        instance.full_name = validated_data.get('full_name',
                                                instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.avatar = validated_data.get('avatar', instance.avatar)

    def get_liked_id(self, instance: User):
        return instance.liked.id

    def get_cart_id(self, instance: User):
        return instance.cart.id

    def get_purchases_id(self, instance: User):
        return instance.purchases.id

    def get_avatar(self, instance: User):
        return instance.get_avatar_url
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
