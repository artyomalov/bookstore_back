from django.urls import path
from .views import UserLikedBooksAPI,UserCartAPI

app_name = 'user_staff'

urlpatterns = [
    path('liked/<int:id>', UserLikedBooksAPI.as_view(),
         name='get_user_liked'),
    path('cart/<int:id>', UserCartAPI.as_view())
]
