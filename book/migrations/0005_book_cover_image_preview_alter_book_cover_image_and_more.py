# Generated by Django 4.2.1 on 2023-11-24 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_alter_book_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover_image_preview',
            field=models.ImageField(null=True, upload_to='books/covers/', verbose_name='cover preview'),
        ),
        migrations.AlterField(
            model_name='book',
            name='cover_image',
            field=models.ImageField(upload_to='books/covers/', verbose_name='cover full size'),
        ),
        migrations.AlterField(
            model_name='book',
            name='created_at',
            field=models.DateTimeField(verbose_name='added to sell list time'),
        ),
    ]
