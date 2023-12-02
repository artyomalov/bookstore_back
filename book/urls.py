from django.urls import path
from .views import GenresList, BookList, FoundBooksList, GetComments, \
    CreateComment, GetSimularBooksByGenre, GetAverageRating, CreateRating

app_name = 'book_api'

urlpatterns = [
    path('list/', BookList.as_view()),
    path('simular/<slug:slug>', GetSimularBooksByGenre.as_view()),
    path('search/<slug:slug>', FoundBooksList.as_view()),
    path('comments/create', CreateComment.as_view()),
    path('comments_list/<slug:slug>', GetComments.as_view()),
    path('rating/get_average/<int:book_id>', GetAverageRating.as_view()),
    path('rating/rate', CreateRating.as_view()),
    path('genres/', GenresList.as_view(),
         )

]
