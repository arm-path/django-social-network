# Generated by Django 4.2.3 on 2023-08-05 12:48

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('friends', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friend',
            unique_together={('user', 'subscription')},
        ),
    ]