from django.db import models
from django.contrib.auth import get_user_model
from book.models import Book


User = get_user_model()


class UserCart(models.Model):
    user_model_id = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'


class CartItem(models.Model):
    user_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    book_id = models.OneToOneField(Book, on_delete=models.CASCADE)
    user_cart = models.ForeignKey(UserCart, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'cart item'
        verbose_name_plural = 'cart items'
