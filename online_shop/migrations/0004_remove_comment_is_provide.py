# Generated by Django 5.0.7 on 2024-08-06 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online_shop', '0003_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='is_provide',
        ),
    ]
