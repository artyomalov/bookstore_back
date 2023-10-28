from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from book.models import Book
from user.models import User


class UserCart(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE,
                                   related_name='cart')

    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'


class CartItem(models.Model):
    user_cart = models.ForeignKey(
        UserCart, on_delete=models.CASCADE, related_name='cart_item')
    book = models.OneToOneField(
        Book, on_delete=models.CASCADE, null=False, related_name='book_cart')
    quantity = models.IntegerField(default=1, validators=[
        MinValueValidator(1), MaxValueValidator(99)])

    class Meta:
        verbose_name = 'cart item'
        verbose_name_plural = 'cart items'
