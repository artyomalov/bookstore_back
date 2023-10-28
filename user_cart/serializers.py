from rest_framework.serializers import ModelSerializer
from .models import CartItem, UserCart
from book.serializers import BookSerializer


class CartItemSerializer(ModelSerializer):

    book = BookSerializer(required=True, allow_null=False)

    class Meta:
        model = CartItem
        fields = ['book', 'quantity']


class UserCartSerializer(ModelSerializer):
    cartitem = CartItemSerializer(
        many=True, required=True, allow_null=False, source='cartitem_set')

    class Meta:
        model = UserCart
        fields = ['cartitem']



