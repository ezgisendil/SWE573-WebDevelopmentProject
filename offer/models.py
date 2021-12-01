from django.db import models
from django.db.models.fields import PositiveIntegerField
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


# Offer Service
class Offer(models.Model):
    title = models.CharField(max_length=100, verbose_name='title')
    content = models.TextField(verbose_name='content')
    location = models.CharField(max_length=100, verbose_name='location')
    date = models.DateField(default='20/12/2021')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

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

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.DO_NOTHING)
    action = models.CharField(max_length=100, verbose_name='action')
    date_posted = models.DateTimeField(default=timezone.now)

    # Actions:
    # OFFER_APPLICATION_ACCEPTED
    # OFFER_APPLICATION_REJECTED
    # OFFER_NEW_APPLICATION
    # OFFER_NEW_FEEDBACK

class Feedback(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.DO_NOTHING, related_name="feedbacks")
    content = models.TextField(verbose_name='content')
    rating = models.PositiveSmallIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    date_posted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        #redirect to its own detail page after being created
        return reverse('offer-detail', kwargs={'pk':self.offer.pk})
