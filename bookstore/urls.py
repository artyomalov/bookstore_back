from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/',
         include('authentication.urls', namespace='authentication')),
    path('api/v1/user/', include('user.urls', namespace='single_user_api')),
    path('api/v1/book/', include('book.urls', namespace='book_api'),
         ),
    path('api/v1/staff/', include('user_staff.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Bookstore"
admin.site.index_title = "Admin panel"
