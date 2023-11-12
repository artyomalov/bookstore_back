# Generated by Django 4.2.1 on 2023-11-11 10:27

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_alter_comment_created_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_staff', '0002_rename_userfavouritebooks_userfavoritebooks'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserFavoriteBooks',
            new_name='UserLikedBooks',
        ),
        migrations.RenameField(
            model_name='purchaseitem',
            old_name='user_cart',
            new_name='user_purchases_list',
        ),
    ]