from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFavoriteBooks(models.Model):
    user_model_id = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'favorite'
