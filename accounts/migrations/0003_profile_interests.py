# Generated by Django 3.2.9 on 2021-11-23 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_shortbio'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='interests',
            field=models.TextField(max_length=250, null=True),
        ),
    ]