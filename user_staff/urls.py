from django.urls import path
from .views import UserLikedBooksAPI, UserCartAPI, CartItemAPI, \
    UserPurchasesAPI

app_name = 'user_staff'

urlpatterns = [
    path('liked/<int:pk>', UserLikedBooksAPI.as_view()),
    path('cart/<int:pk>', UserCartAPI.as_view()),
    path('cart_item/<int:pk>', CartItemAPI.as_view()),
    path('purchases_list/<int:pk>', UserPurchasesAPI.as_view())
]
