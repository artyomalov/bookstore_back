from django.db import models
from django.contrib.auth import get_user_model
from book.models import Book

User = get_user_model()


class UserFavouriteBooks(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE,
                                   related_name='favourite',
                                   null=True)
    user_liked_books = models.ManyToManyField(
        Book, blank=True)

    class Meta:
        verbose_name = 'favourite'
        verbose_name_plural = 'favourite'
 # User.objects.get(pk=2).userfavouritebooks
