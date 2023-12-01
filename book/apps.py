from django.apps import AppConfig
from django.db.models.signals import post_delete
class BookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'book'

    def ready(self):
        from . import signals

