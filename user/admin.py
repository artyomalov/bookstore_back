from django.contrib.auth import get_user_model
from django.contrib import admin


UserProfile = get_user_model()
admin.site.register(UserProfile)
