# Generated by Django 5.0 on 2024-08-10 06:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_chatmessage_message_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='members',
            field=models.ManyToManyField(related_name='communities', to=settings.AUTH_USER_MODEL),
        ),
    ]
