# Generated by Django 3.2.9 on 2021-12-22 23:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('content', models.TextField(verbose_name='content')),
                ('location', models.CharField(max_length=100, verbose_name='location')),
                ('date', models.DateField(default='20/12/2021')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(default='defaultpost.jpg', upload_to='post_pics')),
                ('duration', models.TimeField(null=True)),
                ('max_participant', models.PositiveIntegerField(default=3, validators=[django.core.validators.MinValueValidator(1)])),
                ('num_participant', models.PositiveIntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('current_participant', models.ManyToManyField(related_name='current_events', to=settings.AUTH_USER_MODEL)),
                ('finished_participant', models.ManyToManyField(related_name='finished_events', to=settings.AUTH_USER_MODEL)),
                ('waiting_participant', models.ManyToManyField(related_name='waiting_events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('content', models.TextField(verbose_name='content')),
                ('location', models.CharField(max_length=100, verbose_name='location')),
                ('date', models.DateField(default='20/12/2021')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(default='defaultpost.jpg', upload_to='post_pics')),
                ('duration', models.TimeField(null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('content', models.TextField(verbose_name='content')),
                ('location', models.CharField(max_length=100, verbose_name='location')),
                ('date', models.DateField(default='20/12/2021')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('max_participants', models.PositiveIntegerField(default=3, validators=[django.core.validators.MinValueValidator(1)])),
                ('timecredit', models.PositiveIntegerField(default=1)),
                ('num_participants', models.PositiveIntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('current_participants', models.ManyToManyField(related_name='current_offers', to=settings.AUTH_USER_MODEL)),
                ('finished_participants', models.ManyToManyField(related_name='finished_offers', to=settings.AUTH_USER_MODEL)),
                ('waiting_participants', models.ManyToManyField(related_name='waiting_offers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=100, verbose_name='action')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='service.event')),
                ('offer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='service.offer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='content')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='content')),
                ('rating', models.PositiveSmallIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='feedbacks', to='service.offer')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_feedbacks', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_feedbacks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
