from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('authentication.urls', namespace='authentication')),
    path('api/v1/', include('user.urls', namespace='single user api'))
]
