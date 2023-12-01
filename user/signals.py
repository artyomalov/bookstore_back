import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import User


@receiver(post_delete, sender=User)
def post_delete_image(sender, **kwargs):
    """Delete model's files after model deleting"""
    try:
        kwargs['instance'].avatar.delete(save=False)
    except:
        pass


@receiver(pre_save, sender=User)
def pre_save_image(sender, **kwargs):
    """ Delete old avatar from filesystem"""
    try:
        instance = kwargs['instance']
        old_avatar = instance.__class__.objects.get(
            id=instance.id).avatar.path
        try:
            new_avatar = instance.avatar.path
        except:
            new_avatar = None
        if new_avatar != old_avatar:
            if os.path.exists(old_avatar):
                os.remove(old_avatar)
    except Exception as error:
        print(error)
