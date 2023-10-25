from django.urls import path
from .views import AuthUserDetail

app_name = 'user_detail'

urlpatterns = [
    path('profile/', AuthUserDetail.as_view())
]
