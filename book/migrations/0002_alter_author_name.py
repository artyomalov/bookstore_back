# Generated by Django 4.2.1 on 2023-11-04 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.TextField(max_length=255),
        ),
    ]