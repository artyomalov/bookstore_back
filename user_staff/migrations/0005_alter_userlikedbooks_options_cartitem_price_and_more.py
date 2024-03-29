# Generated by Django 4.2.1 on 2023-11-16 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_staff', '0004_cartitem_cover_type_purchaseitem_cover_type_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userlikedbooks',
            options={'verbose_name': 'liked', 'verbose_name_plural': 'liked'},
        ),
        migrations.AddField(
            model_name='cartitem',
            name='price',
            field=models.IntegerField(default=19.99),
        ),
        migrations.AddField(
            model_name='purchaseitem',
            name='price',
            field=models.IntegerField(default=19.99),
        ),
    ]
