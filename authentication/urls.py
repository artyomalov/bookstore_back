from django.urls import path
from .views import SignupAPIView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import CustomTokenObtainPairView

app_name = 'authentication'

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='singup'),
    path('signin/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
