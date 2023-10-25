from rest_framework import serializers


class GenreSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    genreName = serializers.CharField(max_length=255, allow_null=False,
                                       allow_blank=False, source='genre_name')
    # books = serializers.SerializerMethodField(method_name='get_sorted_books')

    # def get_sorted_books(self, object):
    #     books_query = object.related_books.all()
    #     books_list = []
    #     for book in books_query:
    #         authors = []
    #         for author in book.authors.all():
    #             authors.append({
    #                 'first_name': author.first_name,
    #                 'last_name': author.last_name,
    #                 'biography': author.biography
    #             })
    #         book_data = {
    #             'title': book.title,
    #             'annotation': book.annotation,
    #             'quantity': book.quantity,
    #             'price': book.price,
    #             'cover_image': book.cover_image.url,
    #             'authors': authors
    #         }
    #         books_list.append(book_data)
    #     return books_list
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
