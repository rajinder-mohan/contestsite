# Generated by Django 2.0.2 on 2018-03-05 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20180305_0320'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='adress',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='occupation',
            field=models.CharField(default='1', max_length=200, null=True),
        ),
    ]