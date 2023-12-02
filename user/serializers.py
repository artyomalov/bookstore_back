from drf_extra_fields.fields import Base64ImageField

from .models import User
from rest_framework import serializers


class AuthorizedUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    fullName = serializers.CharField(source='full_name')
    email = serializers.EmailField(max_length=255)
    avatar = serializers.ImageField(required=False)
    userLikedId = serializers.SerializerMethodField(read_only=True,
                                                    method_name='get_liked_id')
    userCartId = serializers.SerializerMethodField(read_only=True,
                                                   method_name='get_cart_id')
    userPurchasesId = serializers.SerializerMethodField(read_only=True,
                                                        method_name='get_purchases_id')

    def update(self, instance: User, validated_data):
        if instance.full_name != self.context.get(
                'fullName') and self.context.get('fullName') is not None:
            instance.full_name = self.context.get('fullName')
        if instance.email != validated_data.get(
                'email') and validated_data.get('email') is not None:
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
