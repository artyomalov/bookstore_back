from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from book.models import Book

User = get_user_model()


class UserLikedBooks(models.Model):
    """
    List of user's favourite books.
    """

    user_id = models.OneToOneField(User, on_delete=models.CASCADE,
                                   related_name='favorite',
                                   null=True, verbose_name='related user')
    user_liked_books = models.ManyToManyField(
        Book, blank=True, verbose_name='liked books list')

    class Meta:
        verbose_name = 'liked'
        verbose_name_plural = 'liked'


class UserCart(models.Model):
    """
    User cart container. Contains list of cart items.
    """

    user_id = models.OneToOneField(User, on_delete=models.CASCADE,
                                   related_name='cart',
                                   verbose_name='related user')

    def __str__(self):
        return f'Cart of {self.user_id.email}'

    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'


class CartItem(models.Model):
    """
    Model of cart item. Contains quantity of books, that user is going to buy
    and related book's model.
    """
    PAPERBACK = 'paperback'
    HARDCOVER = 'hardcover'
    COVER_CHOICES = (
        ('PAPERBACK', 'paperback'),
        ('HARDCOVER', 'hardcover')
    )
    user_cart = models.ForeignKey(
        UserCart, on_delete=models.CASCADE, related_name='cart_item',
        verbose_name='user\'s cart')
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, null=False, related_name='book_cart',
        verbose_name='stored book')
    cover_type = models.CharField(max_length=9, choices=COVER_CHOICES,
                                  default=HARDCOVER)

    quantity = models.IntegerField(default=1, validators=[
        MinValueValidator(1), MaxValueValidator(99)],
                                   verbose_name='stored quantity')
    price = models.IntegerField(default=19.99)

    def is_upperclass(self):
        return self.cover_type in {self.PAPERBACK, self.HARDCOVER}

    def __str__(self):
        return f'Cart item for {self.user_cart.user_id.email}'

    class Meta:
        verbose_name = 'cart item'
        verbose_name_plural = 'cart items'


class UserPurchasesList(models.Model):
    """
   User purchases container. Contains list of purchases.
    """

    user_id = models.OneToOneField(User, on_delete=models.CASCADE,
                                   related_name='purchases',
                                   verbose_name='related user')

    def __str__(self):
        return f'Purchases of {self.user_id.email}'

    class Meta:
        verbose_name = 'user purchases list'
        verbose_name_plural = 'users purchases lists'


class PurchaseItem(models.Model):
    """
    Single purchase.
    Contains quantity of books, that user has bought already, bought time
    and related book's model
    """
    PAPERBACK = 'paperback'
    HARDCOVER = 'hardcover'
    COVER_CHOICES = (
        ('PAPERBACK', 'paperback'),
        ('HARDCOVER', 'hardcover')
    )
    user_purchases_list = models.ForeignKey(
        UserPurchasesList, on_delete=models.CASCADE,
        related_name='purchase_items',
        verbose_name='related list of user\'s purchases'
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False,
                             related_name='book_purchase',
                             verbose_name='bought book')
    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        verbose_name='bought quantity')
    cover_type = models.CharField(max_length=9, choices=COVER_CHOICES,
                                  default=HARDCOVER)
    price = models.IntegerField(default=19.99)
    bought_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name='bought time')

    def is_upperclass(self):
        return self.cover_type in {self.PAPERBACK, self.HARDCOVER}

    def __str__(self):
        return f'Purchase item for {self.user_cart.user_id.email}'

    class Meta:
        verbose_name = 'purchase item'
        verbose_name_plural = 'purchase items'
