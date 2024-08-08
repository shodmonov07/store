# Generated by Django 5.0.7 on 2024-08-08 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_shop', '0007_product_is_available_alter_comment_is_provide'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_available',
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterModelTable(
            name='category',
            table='category',
        ),
        migrations.AlterModelTable(
            name='comment',
            table='comment',
        ),
        migrations.AlterModelTable(
            name='order',
            table='order',
        ),
        migrations.AlterModelTable(
            name='product',
            table='product',
        ),
    ]
