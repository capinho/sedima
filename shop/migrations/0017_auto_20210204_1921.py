# Generated by Django 3.0.5 on 2021-02-04 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_auto_20210204_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattribute',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/%Y/%m/%d'),
        ),
    ]