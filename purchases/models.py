from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from book.models import Book

User = get_user_model()


class UserPurchasesList(models.Model):
    """
    List of user purchases
    """

    user_id = models.OneToOneField(User, on_delete=models.CASCADE,
                                   related_name='purchases')

    class Meta:
        verbose_name = 'user_purchases_list'
        verbose_name_plural = 'users_purchases_lists'


class PurchaseItem(models.Model):
    """
    Single purchase.
    Every item is related with one book and belongs to one purchases list
    """

    user_cart = models.ForeignKey(
        UserPurchasesList, on_delete=models.CASCADE,
        related_name='purchase_item'
    )
    book = models.OneToOneField(Book, on_delete=models.CASCADE, null=False,
                                related_name='book_purchase')
    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)])
    bought_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'purchase item'
        verbose_name_plural = 'purchase items'
