from django.urls import path
from .views import GenresList, BookList, BookDetail, FoundBookList

app_name = 'book_api'

urlpatterns = [
    path('book_list/', BookList.as_view()),
    path('search/<slug:slug>', FoundBookList.as_view()),
    path('detail/<slug:slug>/', BookDetail.as_view()),
    path('genres/', GenresList.as_view(),
         )
]
