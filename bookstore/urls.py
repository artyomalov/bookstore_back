from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/',
         include('authentication.urls', namespace='authentication')),
    path('api/v1/user/', include('user.urls', namespace='single_user_api')),
    path('api/v1/filters/', include('genres.urls', namespace='genres_api'),
         )
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
