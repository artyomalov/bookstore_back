__all__ = ['Author', 'Book', 'BookRaiting']

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from genres.models import Genre

User = get_user_model()


class Author(models.Model):
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    biography = models.TextField(max_length=4000, blank=True)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Book(models.Model):
    title = models.CharField(max_length=255, blank=False, )
    annotation = models.CharField(max_length=4000, blank=False, )
    quantity = models.IntegerField(
        default=0, blank=False, validators=[MinValueValidator(0)])

    price = models.SmallIntegerField(
        blank=False, validators=[MinValueValidator(1)])
    cover_image = models.ImageField(upload_to=f'covers/{title}', blank=False,
                                    null=False)
    authors = models.ManyToManyField(Author)
    genres = models.ManyToManyField(Genre)

    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'books'

    def __str__(self):
        return self.title


class BookRaiting(models.Model):
    score = models.IntegerField(default=5, blank=False,
                                validators=[
                                    MinValueValidator(1),
                                    MaxValueValidator(5)])
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    book_id = models.ForeignKey(
        Book, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = 'raiting'
        verbose_name_plural = 'raitings'
