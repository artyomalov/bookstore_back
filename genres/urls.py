from django.urls import path
from .views import GenresAPI

app_name = 'genres'

urlpatterns = [
    path('genres/', GenresAPI.as_view(), )
]
