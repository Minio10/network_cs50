# Generated by Django 2.2.7 on 2021-04-14 15:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user_likes',
            field=models.ManyToManyField(blank=True, related_name='user_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
