# Generated by Django 4.2.6 on 2023-10-27 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='cover_image',
            field=models.URLField(blank=True, null=True),
        ),
    ]