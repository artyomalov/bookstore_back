__all__ = ['Book', 'Author', 'Rating', 'Comment', 'Genre', ]

import os.path
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

User = get_user_model()


def upload_to(instance, filename):
    """
    return path for saving model's image
    """
    img_name, img_ext = os.path.splitext(filename)
    new_img_name = f'{instance.slug}{img_ext}'
    return f'books/covers/{new_img_name}'


def upload_to_preview(instance, filename):
    """
    return path for saving model's image
    """
    img_name, img_ext = os.path.splitext(filename)
    new_img_name = f'{instance.slug}_preview{img_ext}'
    return f'books/covers/{new_img_name}'


class Book(models.Model):
    """
    Book model. Main model of book app.
    """
    title = models.CharField(max_length=255, blank=False, null=True,
                             verbose_name='title')
    slug = models.SlugField(max_length=255, unique=True, db_index=True,
                            verbose_name='slug',
                            blank=True)
    annotation = models.TextField(max_length=4000, blank=False,
                                  verbose_name='annotation')
    paperback_quantity = models.IntegerField(default=0, blank=False,
                                             validators=[
                                                 MinValueValidator(0)],
                                             verbose_name='paperback quantity')
    hardcover_quantity = models.IntegerField(default=0, blank=False,
                                             validators=[
                                                 MinValueValidator(0)],
                                             verbose_name='hardcover quantity')
    paperback_price = models.FloatField(blank=False,
                                        validators=[MinValueValidator(1)],
                                        verbose_name='paperback price')
    hardcover_price = models.FloatField(blank=False,
                                        validators=[MinValueValidator(1)],
                                        verbose_name='hardcover price')
    cover_image_preview = models.ImageField(upload_to=upload_to_preview,
                                            verbose_name='cover preview')
    cover_image = models.ImageField(
        upload_to=upload_to, blank=False,
        null=False, verbose_name='cover full size')
    authors = models.ManyToManyField('Author', verbose_name='authors list')
    genres = models.ManyToManyField('Genre', verbose_name='genres list')
    created_at = models.DateTimeField(verbose_name='added to sell list time')

    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'books'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Author(models.Model):
    """
    Author's model. Related with book. One book can be related with group of
    authors and one author can be related with many books.
    """
    name = models.CharField(max_length=255, blank=False,
                            verbose_name='author\'s name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Rating(models.Model):
    """
    Single rate item. Contains rate from 1 to 5 link to rated book and
    user that marked book.
    """
    rate = models.IntegerField(default=5, blank=False,
                               validators=[
                                   MinValueValidator(1),
                                   MaxValueValidator(5)],
                               verbose_name='user\'s rate')
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='user rated')
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, null=False, blank=False,
        verbose_name='rated book')

    class Meta:
        verbose_name = 'raiting'
        verbose_name_plural = 'raitings'

    def __str__(self):
        return f'rated by {self.user.full_name}, rate:{self.rate}, '


class Comment(models.Model):
    """
    Singe comment item. Contains creation time, comment text,
    link to the created comment user and related book.
    """
    comment_text = models.TextField(max_length=4000, verbose_name='comment')
    created_at = models.DateTimeField(verbose_name='created at',
                                      auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='left comment user')
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             verbose_name='commented book')

    def __str__(self):
        return f'{self.user.email} about {self.book.title}: {self.comment_text}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'comment'
        verbose_name_plural = 'comments'


class Genre(models.Model):
    """
    Describes model of books' genres. It is also filters at client side.
    """
    genre_name = models.CharField(max_length=255, blank=False,
                                  verbose_name='genre')
    slug = models.SlugField(max_length=255, unique=True, db_index=True,
                            verbose_name='genre slug')

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.genre_name
