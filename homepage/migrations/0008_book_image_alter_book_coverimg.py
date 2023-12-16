# Generated by Django 5.0 on 2023-12-11 17:07

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0007_alter_book_coverimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='book',
            name='coverImg',
            field=models.URLField(blank=True, null=True),
        ),
    ]
