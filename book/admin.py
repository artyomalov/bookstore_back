from django.contrib import admin
from .models import Book, Author, BookRaiting, Comment
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(BookRaiting)
admin.site.register(Comment)
