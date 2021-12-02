from django import forms
from django import forms
from django.forms.widgets import TimeInput, HiddenInput
from .models import Post, Offer, Message, Event, Feedback


#for request and event creation form - date-time widgets
class DateInput(forms.DateInput):
    input_type = 'date'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image','title', 'content','location','date', 'duration']
        widgets = {
            'date': DateInput()
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['image','title', 'content','location','date', 'duration']
        widgets = {
            'date': DateInput()
        }

class DateInput(forms.DateInput):
    input_type = 'date'

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['title', 'content','max_participants','timecredit','location','date']
        widgets = {
            'date': DateInput()
        }

        num_participants = forms.IntegerField(widget=HiddenInput(), initial=0)

class FeedbackForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=((i, i) for i in range(5, 0, -1)))
    class Meta:
        model = Feedback
        fields = ['content', 'rating']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
