# Generated by Django 3.0.5 on 2021-02-04 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20210204_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Variant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.Variant'),
            preserve_default=False,
        ),
    ]
