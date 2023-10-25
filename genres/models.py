from django.db import models


class Genre(models.Model):
    """
        Describes model of books' genres
    """
    genre_name = models.CharField(max_length=255, blank=False)

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.genre_name