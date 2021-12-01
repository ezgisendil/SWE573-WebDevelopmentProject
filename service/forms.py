from django import forms
from django import forms
from django.forms.widgets import TimeInput
from .models import Post, Event


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


