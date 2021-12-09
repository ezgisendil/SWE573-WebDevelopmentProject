from django import forms
from django.forms.widgets import HiddenInput
from .models import Post, Offer, Message, Event, Feedback
import datetime


#for request and event creation form - date-time widgets
class DateInput(forms.DateInput):
    input_type = 'date'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image','title', 'content','location','date']
        widgets = {
            'date': DateInput()
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['image','title', 'content','location','date']
        widgets = {
            'date': DateInput()
        }

class DateInput(forms.DateInput):
    input_type = 'date'

class OfferForm(forms.ModelForm):
    sehirler=["Online", "Adana", "Adıyaman", "Afyon", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "İçel (Mersin)", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]
    location = forms.ChoiceField(label='Location', choices=((i, i) for i in sehirler))

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

class AdvancedSearchForm(forms.Form):
    sehirler=["All", "Online", "Adana", "Adıyaman", "Afyon", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "İçel (Mersin)", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]

    q = forms.CharField(label='Query', max_length=100)
    loc = forms.ChoiceField(label='Location', choices=((i, i) for i in sehirler), required=False)
    from_date = forms.DateField(initial="2010-01-01", required=False, widget=DateInput())
    to_date = forms.DateField(initial=datetime.date.today, required=False, widget=DateInput())
    class Meta:
        fields = ['q', 'to_date', 'from_date', 'loc']       

# class AdvancedSearchForm(forms.Form):
#     sehirler=["Hepsi", "Online", "Adana", "Adıyaman", "Afyon", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "İçel (Mersin)", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]

#     q = forms.CharField(label='Query', max_length=100)
#     loc = forms.ChoiceField(label='Location', choices=((i, i) for i in sehirler), required=False)
#     from_date = forms.DateField(initial="2010-01-01", required=False)
#     to_date = forms.DateField(initial=datetime.date.today, required=False,  input_formats=["%Y-%m-%d"])
#     class Meta:
#         fields = ['q', 'to_date', 'from_date', 'loc']

#         widgets = {
#             'to_date': DateInput(),
#             'from_date': DateInput()
#         }