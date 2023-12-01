import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Book


@receiver(post_delete, sender=Book)
def post_delete_image(sender, **kwargs):
    """Delete models files after model deleting"""
    try:
        kwargs['instance'].cover_image.delete(save=False)
        kwargs['instance'].cover_image_preview.delete(save=False)
    except Exception as error:
        print(error)


@receiver(pre_save, sender=Book)
def pre_save_image(sender, **kwargs):
    """ Delete old cover image and old cover image preview from filesystem """
    try:
        instance = kwargs['instance']
        old_cover_image = instance.__class__.objects.get(
            id=instance.id).cover_image.path
        old_cover_image_preview = instance.__class__.objects.get(
            id=instance.id).cover_image_preview.path
        print('old', old_cover_image, 'old_previw', old_cover_image_preview)
        try:
            new_cover_image = instance.cover_image.path
            new_cover_image_preview = instance.cover_image_preview.path
        except:
            new_cover_image = None
            new_cover_image_preview = None
        if new_cover_image != old_cover_image:
            if os.path.exists(old_cover_image):
                os.remove(old_cover_image)
        if new_cover_image_preview != old_cover_image_preview:
            if os.path.exists(old_cover_image):
                os.remove(old_cover_image_preview)
    except Exception as error:
        print(error)
