from django.urls import path
from .views import GenresList, BookList, FoundBookList, GetComments, \
    CreateComment, GetSimularBooksByGenre

app_name = 'book_api'

urlpatterns = [
    path('list/', BookList.as_view()),
    path('simular/<slug:slug>', GetSimularBooksByGenre.as_view()),
    path('search/<slug:slug>', FoundBookList.as_view()),
    path('comments/create', CreateComment.as_view()),
    path('comments_list/<slug:slug>', GetComments.as_view()),
    # path('detail/<slug:slug>/', BookDetail.as_view()),
    path('genres/', GenresList.as_view(),
         )

]
