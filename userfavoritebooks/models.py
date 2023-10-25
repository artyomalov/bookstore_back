from django.db import models
from django.contrib.auth import get_user_model
from book.models import Book

User = get_user_model()


class UserFavoriteBooks(models.Model):
    user_model_id = models.OneToOneField(User, on_delete=models.CASCADE)
    user_liked_books = models.ManyToManyField(
        Book, blank=True)

    class Meta:
        verbose_name = 'favorite'
        verbose_name_plural = 'favorite'
