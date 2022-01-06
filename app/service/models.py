from django.db import models
from django.db.models.fields import TimeField
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.fields import PositiveIntegerField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from PIL import Image
# from location_field.models.plain import PlainLocationField

# Create your models here.

# Offer Service
class Offer(models.Model):
    title = models.CharField(max_length=100, verbose_name='title')
    content = models.TextField(verbose_name='content')
    location = models.CharField(max_length=100, verbose_name='location')
    date = models.DateField(default='20/12/2021')
    time = TimeField(null=True)
    duration = PositiveIntegerField(null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='defaultservice.jpg', upload_to='post_pics')

    max_participants = models.PositiveIntegerField(default=3, validators=[MinValueValidator(1)])
    timecredit = models.PositiveIntegerField(default=1)
    num_participants = models.PositiveIntegerField(default=0)

    finished_participants = models.ManyToManyField(User, related_name="finished_offers")
    current_participants = models.ManyToManyField(User, related_name="current_offers")
    waiting_participants = models.ManyToManyField(User, related_name="waiting_offers")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #redirect to its own detail page after being created
        return reverse('offer-detail', kwargs={'pk':self.pk})

    def clean(self):
        if self.num_participants > self.max_participants:
            raise ValidationError(_('Maximum number of participants cannot be less than number of current participants!'))

    @property
    def feedback_senders(self):

        return list(self.feedbacks.values_list("sender__username", flat=True))

    @property
    def feedback_receivers(self):

        return list(self.feedbacks.values_list("receiver__username", flat=True))
    
    def get_type(self):
        return "offer"

class Feedback(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_feedbacks")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_feedbacks")
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="feedbacks")
    content = models.TextField(verbose_name='content')
    rating = models.PositiveSmallIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    date_posted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        #redirect to its own detail page after being created
        return reverse('offer-detail', kwargs={'pk':self.offer.pk})


#Request Service
class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='title')
    content = models.TextField(verbose_name='content')
    # city = models.CharField(max_length=255)
    # location = PlainLocationField(based_fields=['city'], zoom=7)
    location = models.CharField(max_length=100, verbose_name='location')
    date = models.DateField(default='20/12/2021')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='defaultservice.jpg', upload_to='post_pics')
    time = TimeField(null=True)
    duration = PositiveIntegerField(null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #redirect to its own detail page after being created
        return reverse('post-detail', kwargs={'pk':self.pk})

    def get_type(self):
        return "post"

#Organize Event
class Event(models.Model):
    title = models.CharField(max_length=100, verbose_name='title')
    content = models.TextField(verbose_name='content')
    location = models.CharField(max_length=100, verbose_name='location')
    date = models.DateField(default='20/12/2021')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='defaultservice.jpg', upload_to='post_pics')
    time = TimeField(null=True)
    duration = PositiveIntegerField(null=True)

    max_participant = models.PositiveIntegerField(default=3, validators=[MinValueValidator(1)])
    num_participant = models.PositiveIntegerField(default=0)

    finished_participant = models.ManyToManyField(User, related_name="finished_events")
    current_participant = models.ManyToManyField(User, related_name="current_events")
    waiting_participant = models.ManyToManyField(User, related_name="waiting_events")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #redirect to its own detail page after being created
        return reverse('event-detail', kwargs={'pk':self.pk})

    def clean(self):
        if self.num_participant > self.max_participant:
            raise ValidationError(_('Maximum number of participants cannot be less than number of current participants!'))
    
    def get_type(self):
        return "event"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField(verbose_name='content')
    date_posted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        #redirect to its own detail page after being created
        return reverse('message-detail', kwargs={'username': self.receiver.username})

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE)
    action = models.CharField(max_length=100, verbose_name='action')
    date_posted = models.DateTimeField(default=timezone.now)

    # Actions:
    # OFFER_APPLICATION_ACCEPTED
    # OFFER_APPLICATION_REJECTED
    # OFFER_NEW_APPLICATION
    # OFFER_NEW_FEEDBACK
    # EVENT_APPLICATION_ACCEPTED
    # EVENT_APPLICATION_REJECTED
    # EVENT_NEW_APPLICATION
    # EVENT_NEW_FEEDBACK