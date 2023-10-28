# Generated by Django 4.2.1 on 2023-10-27 20:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_favourite_books', '0003_alter_userfavouritebooks_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfavouritebooks',
            name='user_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favourite', to=settings.AUTH_USER_MODEL),
        ),
    ]
