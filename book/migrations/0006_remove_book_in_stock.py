# Generated by Django 4.2.1 on 2023-05-21 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_rename_in_sthock_quantity_book_in_stock_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='in_stock',
        ),
    ]
