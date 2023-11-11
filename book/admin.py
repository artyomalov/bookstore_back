from django.contrib import admin
from .models import Book, Author, Rating, Comment, Genre


#
# admin.site.register(Book)
# admin.site.register(Author)
# admin.site.register(Rating)
# admin.site.register(Genre)
# admin.site.register(Comment)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'slug',
        'paperback_quantity',
        'paperback_price',
        'hardcover_quantity',
        'hardcover_price',
    )
    list_display_links = ('title', 'slug',)
    list_editable = ('paperback_price', 'hardcover_price',)
    list_per_page = 10


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('name',)
    ordering = ('id',)
    list_per_page = 20


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'rate',)
    list_display_links = ('id', 'rate')
    list_per_page = 20


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'created_at',)
    list_display_links = ('id', 'created_at',)
    list_per_page = 20
    ordering = ('id',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'genre_name')
    list_display_links = ('genre_name',)
    ordering = ('id',)
