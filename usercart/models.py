from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from book.models import Book
from user.models import User


class UserCart(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'


class CartItem(models.Model):
    user_cart = models.ForeignKey(
        UserCart, on_delete=models.CASCADE)
    purchases_list = models.ForeignKey(
        UserCart, on_delete=models.CASCADE, related_name='purchases')
    book = models.ForeignKey(
        Book, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1, validators=[
                                   MinValueValidator(1), MaxValueValidator(99)])

    class Meta:
        verbose_name = 'cart item'
        verbose_name_plural = 'cart items'


class Comment(models.Model):
    created_at = models.TimeField(auto_now_add=True)
    comment_text = models.CharField(max_length=4000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
