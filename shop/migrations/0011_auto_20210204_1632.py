# Generated by Django 3.0.5 on 2021-02-04 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20201217_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variant',
            name='available',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='created',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='price',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='product',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='updated',
        ),
    ]
