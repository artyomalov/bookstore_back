from django.urls import path
from .views import AuthUserDetail

app_name = 'user_detail'

urlpatterns = [
    path('user/<int:pk>', AuthUserDetail.as_view())
]
