# Generated by Django 3.0.5 on 2021-05-14 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_product_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='thumbnail',
        ),
    ]
