from django.contrib.auth import get_user_model
from django.contrib import admin

UserProfile = get_user_model()


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name')
    list_display_links = ('id', 'email', 'full_name')
    ordering = ('id',)
    search_fields = ('email', 'full_name',)
    search_help_text = 'search by email and full name fields'
