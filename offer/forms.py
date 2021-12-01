from django import forms
from django.forms.widgets import HiddenInput, TimeInput
from .models import Feedback, Offer

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
