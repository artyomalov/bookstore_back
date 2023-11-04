__all__ = ['BookSerializer']

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    slug = serializers.SlugField(max_length=255, allow_blank=False)
    title = serializers.CharField(max_length=255, allow_blank=False)
    annotation = serializers.CharField(max_length=4000, allow_blank=False)
    paperbackQuantity = serializers.IntegerField(default=0)
    hardcoverQuantity = serializers.IntegerField(default=0)
    paperbackPrice = serializers.IntegerField(default=0)
    hardcoverPrice = serializers.IntegerField(default=0)
    coverImage = serializers.ImageField(allow_empty_file=False,
                                        source='cover_image')
    rating = serializers.SerializerMethodField(method_name='get_rating')
    salesCount = serializers.SerializerMethodField(
        method_name='get_sales_count')
    authors = serializers.SerializerMethodField(method_name='get_authors')
    # genres = serializers.SerializerMethodField(method_name='get_genres')
    comments = serializers.SerializerMethodField(method_name='get_comments')

    def get_rating(self, instance):
        """
        Get common average rating of the book.
        """
        rating_query = instance.rating_set.all()
        rating_summ = 0
        rating_list = []
        for rate in rating_query:
            rating_summ += rate.rate
            rating_list.append(rate.rate)
        if len(rating_list) != 0:
            book_rating = rating_summ / len(rating_list)
            return book_rating
        return 0

    def get_sales_count(self, instance):
        """
        Get common count of book's purchases.
        Need to add 'bestseller' icon at client side.
        """
        sales_count_query = instance.book_purchase.all()
        sales_count = 0
        for sale in sales_count_query:
            sales_count += sale.quantity
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
        comments_query = instance.comment_set.all()
        comments_list = []
        for comment in comments_query:
            user = User.objects.get(id=comment.user.id)
            comment_data = {
                'id': comment.id,
                'userName': user.full_name,
                'createdAt': comment.created_at,
                'text': comment.comment_text
            }
            if comment.user.full_name is None:
                comment_data['userName'] = user.email
            comments_list.append(comment_data)

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
