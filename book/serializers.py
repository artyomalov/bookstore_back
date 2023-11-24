__all__ = ['BookSerializer']

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Avg, Sum, F

from book.models import Comment

User = get_user_model()


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    slug = serializers.SlugField(max_length=255, allow_blank=False)
    title = serializers.CharField(max_length=255, allow_blank=False)
    annotation = serializers.CharField(max_length=4000, allow_blank=False)
    paperbackQuantity = serializers.IntegerField(source='paperback_quantity')
    hardcoverQuantity = serializers.IntegerField(source='hardcover_quantity')
    paperbackPrice = serializers.FloatField(source='paperback_price')
    hardcoverPrice = serializers.FloatField(source='hardcover_price')
    coverImage = serializers.ImageField(allow_empty_file=False,
                                        source='cover_image')
    coverImagePreview = serializers.ImageField(allow_empty_file=False,
                                               source='cover_image_preview')
    createdAt = serializers.DateTimeField(source='created_at')
    rating = serializers.SerializerMethodField(method_name='get_rating')
    salesCount = serializers.SerializerMethodField(
        method_name='get_sales_count')
    authors = serializers.SerializerMethodField(method_name='get_authors')

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

    # def get_comments(self, instance):
    #     """
    #     Get list of book's comments.
    #     """
    #     comments_list = instance.comment_set.all().values(
    #         'id',
    #         userName=F('user__full_name'),
    #         userAvatar=F('user__avatar'),
    #         createdAt=F('created_at'),
    #         text=F('comment_text')
    #     )
    #
    #     return comments_list


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=4000, source='comment_text')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    userData = serializers.SerializerMethodField(method_name='get_user_data',
                                                 read_only=True)

    def get_user_data(self, instance: Comment):
        user_name = instance.user.full_name
        user_avatar = instance.user.get_avatar_url
        if user_name is None:
            user_name = 'Unknown'
        user_data = {
            'userName': user_name,
            'userAvatar': user_avatar,
        }
        return user_data

    def create(self, validated_data):
        comment = Comment(comment_text=validated_data.get('comment_text'))
        comment.user_id = self.context.get('user_id')
        comment.book_id = self.context.get('book_id')
        comment.save()
        return comment


class GenreSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    genreName = serializers.CharField(max_length=255, allow_null=False,
                                      allow_blank=False,
                                      source='genre_name')
    slug = serializers.SlugField(max_length=255)

# Fiction
# fiction

# Non-fiction
# non_fiction

# Light fiction
# light_fiction

# Science-fiction
# science_fiction

# Fantasy
# fantasy

# Business & finance
# business_finance

# Politics
# politics

# Travel books
# travel_books

# Autobiography
# autobiography

# History
# history

# Thriller/Mystery
# thriller_mystery

# Romance
# romance

# Satire
# satire

# Horror
# horror

# Health\medicine
# health_medicine

# Children's books
# children_books

# Encyclopedia
# encyclopedia
