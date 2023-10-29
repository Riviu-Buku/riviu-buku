# Generated by Django 4.2.6 on 2023-10-27 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_reviewcheck'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewcheck',
            old_name='checked',
            new_name='checkedDownvote',
        ),
        migrations.AddField(
            model_name='reviewcheck',
            name='checkedUpvote',
            field=models.BooleanField(default=False, unique=True),
        ),
    ]