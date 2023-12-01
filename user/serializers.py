from drf_extra_fields.fields import Base64ImageField

from .models import User
from rest_framework import serializers


class AuthorizedUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    fullName = serializers.CharField(allow_blank=True, allow_null=True,
                                     source='full_name')
    email = serializers.EmailField(max_length=255)
    avatar = serializers.ImageField(required=False)
    userLikedId = serializers.SerializerMethodField(read_only=True,
                                                    method_name='get_liked_id')
    userCartId = serializers.SerializerMethodField(read_only=True,
                                                   method_name='get_cart_id')
    userPurchasesId = serializers.SerializerMethodField(read_only=True,
                                                        method_name='get_purchases_id')

    def update(self, instance: User, validated_data):
        print(validated_data)
        instance.full_name = validated_data.get('fullName',
                                                instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance

    def get_liked_id(self, instance: User):
        return instance.liked.id

    def get_cart_id(self, instance: User):
        return instance.cart.id

    def get_purchases_id(self, instance: User):
        return instance.purchases.id

    def get_avatar(self, instance: User):
        return instance.get_avatar_url
