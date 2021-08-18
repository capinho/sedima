# Generated by Django 3.0.5 on 2021-02-04 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_productattribute'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.AddField(
            model_name='productattribute',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/%Y/%m/%d'),
        ),
    ]