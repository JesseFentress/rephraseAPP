# Generated by Django 3.2.8 on 2021-12-06 01:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rephrase', '0003_alter_chat_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userchat',
            name='chat',
        ),
        migrations.RemoveField(
            model_name='userchat',
            name='user',
        ),
        migrations.AlterField(
            model_name='chat',
            name='server',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rephrase.server', verbose_name='server'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='chat_users', to=settings.AUTH_USER_MODEL, verbose_name='chat_users'),
        ),
        migrations.DeleteModel(
            name='FriendRequest',
        ),
        migrations.DeleteModel(
            name='UserChat',
        ),
    ]
