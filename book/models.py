__all__ = ['Book', 'Author', 'Rating', 'Comment', 'Genre', ]

import os.path

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


# def upload_to(instance, filename):
#     """
#     return path for saving model's image
#     """
#     return f'user/books/{instance.title}/{filename}'.format(
#         filename=filename)


class Book(models.Model):
    """
    Book model. Main model of book app.
    """
    title = models.CharField(max_length=255, blank=False, )
    annotation = models.TextField(max_length=4000, blank=False, )
    quantity = models.IntegerField(
        default=0, blank=False, validators=[MinValueValidator(0)])

    price = models.IntegerField(
        blank=False, validators=[MinValueValidator(1)])
    cover_image = models.ImageField(
        upload_to='books/covers/', blank=False,
        null=False)
    authors = models.ManyToManyField('Author')
    genres = models.ManyToManyField('Genre')

    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'books'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        img_name, img_ext = os.path.splitext(self.cover_image.name)
        new_img_name = f'{self.title}{img_ext}'
        self.cover_image.name = new_img_name
        super().save(*args, **kwargs)


class Author(models.Model):
    """
    Author's model. Related with book. One book can be related with group of
    authors and one author can be related with many books.
    """
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

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
                                   MaxValueValidator(5)])
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, null=False, blank=False)

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
    comment_text = models.CharField(max_length=4000)
    created_at = models.TimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f'comment: {self.id}, {self.user.full_name}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'comment'
        verbose_name_plural = 'comments'


class Genre(models.Model):
    """
        Describes model of books' genres. It is also filters at client side.
    """
    genre_name = models.CharField(max_length=255, blank=False)
    slug = models.SlugField(max_length=255, db_index=True)

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.genre_name
