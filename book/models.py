from django.db import models
from django.contrib.auth import get_user_model
from userfavoritebooks.models import UserFavoriteBooks
User = get_user_model()


class Author(models.Model):
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    biography = models.TextField(max_length=4000, null=True, blank=True)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Book(models.Model):
    FICTION = 'fiction'
    NON_FICTION = 'non_fiction'
    LIGHT_FICTION = 'light_fiction'
    SCIENCE_FICTION = 'science_fiction'
    FANTSY = 'fantasy'
    BUSINESS_FINANCE = 'business_finance'
    POLITICS = 'politics'
    TREAVEL_BOOKS = 'travel_books'
    AUTOBIOGRAPHY = 'autobiography'
    HISTORY = 'history'
    THRILLER_MYSTERY = 'thriller_Mystery'
    ROMANCE = 'romance'
    SATIRE = 'satire'
    HORROR = 'horror'
    HEALTH_MEDICINE = 'health_medicine'
    CHILDEREN_BOOKS = 'childrens_books'
    ENCYCLOPEDIA = 'encyclopedia'

    GENRES = [
        (FICTION, 'fiction'),
        (NON_FICTION, 'non_fiction'),
        (LIGHT_FICTION, 'light_fiction'),
        (SCIENCE_FICTION, 'science_fiction'),
        (FANTSY, 'fantasy'),
        (BUSINESS_FINANCE, 'business_finance'),
        (POLITICS, 'politics'),
        (TREAVEL_BOOKS, 'travel_books'),
        (AUTOBIOGRAPHY, 'autobiography'),
        (HISTORY, 'history'),
        (THRILLER_MYSTERY, 'thriller_Mystery'),
        (ROMANCE, 'romance'),
        (SATIRE, 'satire'),
        (HORROR, 'horror'),
        (HEALTH_MEDICINE, 'health_medicine'),
        (CHILDEREN_BOOKS, 'childrens_books'),
        (ENCYCLOPEDIA, 'encyclopedia'),
    ]
    title = models.CharField(max_length=255, blank=False, null=False)
    annotation = models.CharField(max_length=4000, blank=False, null=False)
    genre = models.CharField(max_length=255, blank=False,
                             null=False, choices=GENRES)
    price = models.SmallIntegerField(null=False, blank=False)
    in_stock = models.BooleanField(default=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    average_value = models.IntegerField(default=0)
    author_ids = models.ManyToManyField(Author)
    liked_by_user = models.ForeignKey(
        UserFavoriteBooks, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'books'

    def __str__(self):
        return self.title


class Comment(models.Model):
    created_at = models.TimeField(auto_now_add=True)
    comment_text = models.CharField(max_length=4000)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'books'


class BookRaiting(models.Model):
    score = models.IntegerField(default=0)  # common count of users raitings
    # count of users that reted some book
    rated_users_count = models.IntegerField(default=0)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'raiting'
        verbose_name_plural = 'raitings'
