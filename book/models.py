from django.db import models
from user.models import User


class Author(models.Model):
    first_name = models.CharField(255)
    last_name = models.CharField(255)
    biography = models.TextField(4000)


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


class Comment(models.Model):
    created_at = models.TimeField(auto_now_add=True)
    comment_text = models.CharField(max_length=4000)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)


class BookRaiting(models.Model):
    score = models.IntegerField()  # common count of users raitings
    rated_users_count = models.IntegerField()  # count of users that reted some book
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
