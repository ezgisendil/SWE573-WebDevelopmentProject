from django.db import models
from django.db.models.fields import TimeField
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


#Request Service
class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='title')
    content = models.TextField(verbose_name='content')
    location = models.CharField(max_length=100, verbose_name='location')
    date = models.DateField(default='20/12/2021')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='defaultpost.jpg', upload_to='post_pics')
    duration = TimeField(null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #redirect to its own detail page after being created
        return reverse('post-detail', kwargs={'pk':self.pk})


#Organize Event

class Event(models.Model):
    title = models.CharField(max_length=100, verbose_name='title')
    content = models.TextField(verbose_name='content')
    location = models.CharField(max_length=100, verbose_name='location')
    date = models.DateTimeField(default='20/12/2021')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='defaultpost.jpg', upload_to='post_pics')
    duration = TimeField(null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #redirect to its own detail page after being created
        return reverse('post-detail', kwargs={'pk':self.pk})