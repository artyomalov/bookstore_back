from django.db import models
from django.contrib.auth import get_user_model
from book.models import Book
from user.models import User


class UserCart(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'


class ListOfUsersPurchases(models.Model):
    user_id = models.OneToOneField(User,  on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'purchase'
        verbose_name_plural = 'purchases'


class CartItem(models.Model):
    user_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    book_id = models.ManyToManyField(Book)
    user_cart = models.ForeignKey(UserCart, on_delete=models.CASCADE)
    user_purchase_list = models.ForeignKey(
        ListOfUsersPurchases, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'cart item'
        verbose_name_plural = 'cart items'
