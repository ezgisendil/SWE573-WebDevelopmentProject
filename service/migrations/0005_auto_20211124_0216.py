# Generated by Django 3.2.9 on 2021-11-23 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_auto_20211124_0145'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='duration',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='duration',
            field=models.TimeField(null=True),
        ),
    ]