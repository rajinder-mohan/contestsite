# Generated by Django 2.0.2 on 2018-03-08 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_chatgroup_groupusers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='user',
        ),
    ]
