from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from book.models import Book

User = get_user_model()


class UserFavouriteBooks(models.Model):
    """
    List of user's favourite books.
    """

    user_id = models.OneToOneField(User, on_delete=models.CASCADE,
                                   related_name='favourite',
                                   null=True)
    user_liked_books = models.ManyToManyField(
        Book, blank=True)

    class Meta:
        verbose_name = 'favourite'
        verbose_name_plural = 'favourite'


class UserCart(models.Model):
    """
    User cart container. Contains list of cart items.
    """

    user_id = models.OneToOneField(User, on_delete=models.CASCADE,
                                   related_name='cart')

    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'


class CartItem(models.Model):
    """
    Model of cart item. Contains quantity of books, that user is going to buy
    and related book's model.
    """

    user_cart = models.ForeignKey(
        UserCart, on_delete=models.CASCADE, related_name='cart_item')
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, null=False, related_name='book_cart')
    quantity = models.IntegerField(default=1, validators=[
        MinValueValidator(1), MaxValueValidator(99)])

    class Meta:
        verbose_name = 'cart item'
        verbose_name_plural = 'cart items'


class UserPurchasesList(models.Model):
    """
   User purchases container. Contains list of purchases.
    """

    user_id = models.OneToOneField(User, on_delete=models.CASCADE,
                                   related_name='purchases')

    class Meta:
        verbose_name = 'user_purchases_list'
        verbose_name_plural = 'users_purchases_lists'


class PurchaseItem(models.Model):
    """
    Single purchase.
    Contains quantity of books, that user has bought already, bought time
    and related book's model
    """

    user_cart = models.ForeignKey(
        UserPurchasesList, on_delete=models.CASCADE,
        related_name='purchase_item'
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False,
                             related_name='book_purchase')
    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)])
    bought_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'purchase item'
        verbose_name_plural = 'purchase items'
