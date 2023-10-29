from django.contrib import admin
from .models import Book, Author, Rating, Comment, Genre

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Rating)
admin.site.register(Genre)
