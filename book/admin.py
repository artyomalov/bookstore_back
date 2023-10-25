from django.contrib import admin
from .models import Book, Author, BookRaiting
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(BookRaiting)
