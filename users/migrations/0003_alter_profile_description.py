# Generated by Django 4.2.3 on 2023-09-05 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.TextField(default='Hello, i am a new one here.'),
        ),
    ]
