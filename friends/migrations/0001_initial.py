# Generated by Django 4.2.3 on 2023-08-12 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friends', models.BooleanField(default=False, help_text='Friend request confirmation')),
                ('black_list', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'firend',
                'verbose_name_plural': 'friends',
            },
        ),
    ]
