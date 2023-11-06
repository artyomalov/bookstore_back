__all__ = ['BookSerializer']

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Avg, Sum, F

User = get_user_model()


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    slug = serializers.SlugField(max_length=255, allow_blank=False)
    title = serializers.CharField(max_length=255, allow_blank=False)
    annotation = serializers.CharField(max_length=4000, allow_blank=False)
    paperbackQuantity = serializers.IntegerField(source='paperback_quantity')
    hardcoverQuantity = serializers.IntegerField(source='hardcover_quantity')
    paperbackPrice = serializers.IntegerField(source='paperback_price')
    hardcoverPrice = serializers.IntegerField(source='hardcover_price')
    coverImage = serializers.ImageField(allow_empty_file=False,
                                        source='cover_image')
    createdAt = serializers.DateTimeField(source='created_at')
    rating = serializers.SerializerMethodField(method_name='get_rating')
    salesCount = serializers.SerializerMethodField(
        method_name='get_sales_count')
    authors = serializers.SerializerMethodField(method_name='get_authors')
    # genres = serializers.SerializerMethodField(method_name='get_genres')
    comments = serializers.SerializerMethodField(method_name='get_comments')

    def get_additional_data(self, instance):
        additional_data_query = instance

    def get_rating(self, instance):
        """
        Get common average rating of the book.
        """
        rate_dict = instance.rating_set.aggregate(Avg('rate'))
        if rate_dict.get('rate__avg') is None:
            return 0
        return rate_dict.get('rate__avg')

    def get_sales_count(self, instance):
        """
        Get common count of book's purchases.
        Is needed to add 'bestseller' icon at client side.
        """
        sales_count = 0
        sales_count_dict = instance.book_purchase.aggregate(Sum('quantity'))
        if sales_count_dict.get('quantity__sum') is not None:
            sales_count = sales_count_dict.get('quantity__sum')
        return sales_count

    def get_authors(self, instance):
        """
        Get list of book's authors.
        """
        authors_query = instance.authors.all()
        authors_list = [
            {
                'id': author.id,
                'name': author.name,
            } for author in authors_query
        ]
        return authors_list

    # def get_genres(self, instance):
    #     """
    #     Get list of book's genres.
    #     """
    #     genres_query = instance.genres.all()
    #     genres_list = [
    #         {'id': genre.id,
    #          'genreName': genre.genre_name,
    #          'slug': genre.slug,
    #          } for genre in genres_query
    #     ]
    #     return genres_list

    def get_comments(self, instance):
        """
        Get list of book's comments.
        """
        comments_list = instance.comment_set.all().values('id',
                                                          userName=F(
                                                              'user__full_name'),
                                                          cratedAt=F(
                                                              'created_at'),
                                                          text=F(
                                                              'comment_text'))

        return comments_list


class GenreSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    genreName = serializers.CharField(max_length=255, allow_null=False,
                                      allow_blank=False,
                                      source='genre_name')
    slug = serializers.SlugField(max_length=255)

# FICTION = 'fiction'
# NON_FICTION = 'non_fiction'
# LIGHT_FICTION = 'light_fiction'
# SCIENCE_FICTION = 'science_fiction'
# FANTASY = 'fantasy'
# BUSINESS_FINANCE = 'business_finance'
# POLITICS = 'politics'
# TREAVEL_BOOKS = 'travel_books'
# AUTOBIOGRAPHY = 'autobiography'
# HISTORY = 'history'
# THRILLER_MYSTERY = 'thriller_Mystery'
# ROMANCE = 'romance'
# SATIRE = 'satire'
# HORROR = 'horror'
# HEALTH_MEDICINE = 'health_medicine'
# CHILDEREN_BOOKS = 'childrens_books'
# ENCYCLOPEDIA = 'encyclopedia'
