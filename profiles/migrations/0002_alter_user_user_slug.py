# Generated by Django 4.2.3 on 2023-08-05 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_slug',
            field=models.SlugField(max_length=150, unique=True, verbose_name='user slug'),
        ),
    ]
