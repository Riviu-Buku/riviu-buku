# Generated by Django 4.2.6 on 2023-10-29 05:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('homepage', '0002_load_fixtures'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='liked_by_users',
            field=models.ManyToManyField(blank=True, related_name='liked_books', to=settings.AUTH_USER_MODEL),
        ),
    ]
