# Generated by Django 4.0.6 on 2022-07-30 13:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0009_alter_review_rating'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserFollows',
            new_name='UserFollow',
        ),
    ]
