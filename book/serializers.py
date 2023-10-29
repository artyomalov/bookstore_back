__all__ = ['BookSerializer']

from rest_framework import serializers


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255, allow_blank=False)
    annotation = serializers.CharField(max_length=4000, allow_blank=False)
    quantity = serializers.IntegerField(default=0)
    price = serializers.IntegerField()
    coverImage = serializers.ImageField(allow_empty_file=False,
                                        source='cover_image')
    rating = serializers.SerializerMethodField(method_name='get_rating')
    authors = serializers.SerializerMethodField(method_name='get_authors')
    genres = serializers.SerializerMethodField(method_name='get_genres')
    comments = serializers.SerializerMethodField(method_name='get_comments')

    def get_authors(self, instance):
        authors_query = instance.authors.all()
        authors_list = [
            {'firstName': author.first_name,
             'lastName': author.last_name,
             } for author in authors_query
        ]
        return authors_list

    def get_genres(self, instance):
        genres_query = instance.genres.all()
        genres_list = [
            {'genreName': genre.genre_name,
             'slug': genre.slug,
             } for genre in genres_query
        ]
        return genres_list

    def get_comments(self, instance):
        comments_query = instance.comments.all()
        comments_list = [{
            'userName': comment.user.full_name,
            'createdAt': comment.created_at,
            'text': comment.comment_text
        } for comment in comments_query]

        return comments_list

    def get_rating(self, instance):
        rating_query = instance.rating_set.all()
        rating_summ = 0
        rating_list = []
        for rate in rating_query:
            rating_summ += rate.rate
            rating_list.append(rate.rate)
        book_rating = rating_summ / len(rating_list)
        return book_rating


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
# FANTSY = 'fantasy'
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
