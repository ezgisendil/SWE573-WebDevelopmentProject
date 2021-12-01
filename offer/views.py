from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db import IntegrityError, transaction

from .models import Feedback, Notification, Offer
from .forms import FeedbackForm, OfferForm
from django.db.models import Count, F, Value

# Offer Service
#Home Page
class OfferDetailView(DetailView):
    model = Offer
    context_object_name = 'offer'

class OfferCreateView(LoginRequiredMixin, CreateView):
    model = Offer
    #fields = ['title', 'content','location','date']
    form_class = OfferForm
    def form_valid(self, form):
        form.instance.author = self.request.user #author of the form
        return super().form_valid(form)  #validate the form

class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    #fields = ['title', 'content','location','date']
    form_class = FeedbackForm
    def form_valid(self, form):
        form.instance.author = self.request.user #author of the form
        offer = Offer.objects.filter(pk=self.kwargs.get('pk')).first()
        form.instance.offer = offer
        
        response = super().form_valid(form)  #validate the form

        with transaction.atomic():
            offer.current_participants.remove(self.request.user)
            offer.finished_participants.add(self.request.user)
            offer.author.profile.timecredit += offer.timecredit
            offer.author.profile.save()

            notification = Notification(user=offer.author, offer=offer, action="OFFER_NEW_FEEDBACK")
            notification.save()

        return response

class OfferUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Offer
    fields = ['title', 'content','max_participants','timecredit','location','date']
    
    def form_valid(self, form):
        form.instance.author = self.request.user #author of the form
        return super().form_valid(form)  #validate the form
    
    def test_func(self):
        offer = self.get_object()
        # if current user is the author of the offer
        if self.request.user == offer.author:
            return True
        return False

class OfferDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Offer
    success_url = '/' #after being deleted, delete the offer and redirect to home page

    def test_func(self):
        offer = self.get_object()
        # if current user is the author of the offer
        if self.request.user == offer.author:
            return True
        return False

#user's offers 
class OfferListView(ListView):
    model = Offer
    template_name = 'offer/offer_list.html'  # <app> / <model>_<viewtype>.html
    context_object_name = 'offers'
    paginate_by = 5

    def get_queryset(self):
        username = self.kwargs.get('username')
        filter = self.kwargs.get('filter')

        res = Offer.objects
        if username:
            res = res.filter(author__username=username)
        elif filter == "waiting":
            res = res.filter(waiting_participants=self.request.user)
        elif filter == "current":
            res = res.filter(current_participants=self.request.user)
        elif filter == "finished":
            res = res.filter(finished_participants=self.request.user)

        res = res.order_by('-date_posted').order_by('-date_posted')

        return res

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'offer/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 5

    def get_queryset(self):
        res = Notification.objects.filter(user=self.request.user).order_by('-date_posted').order_by('-date_posted').all()

        return res

def apply_offer(request, pk):
    offer = Offer.objects.filter(pk=pk).first()

    print(request.user)

    if offer is None:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    if not request.user in offer.waiting_participants.all():
        with transaction.atomic():
            offer.waiting_participants.add(request.user)

            offer.num_participants += 1
            offer.save()

            request.user.profile.timecredit -= offer.timecredit
            request.user.profile.save()

            notification = Notification(user=offer.author, offer=offer, action="OFFER_NEW_APPLICATION")
            notification.save()

    return HttpResponseRedirect(offer.get_absolute_url())

def offer_action(request, pk, action, user_id):
    print(pk, action, user_id)

    offer = Offer.objects.filter(pk=pk).first()
    user = offer.waiting_participants.filter(pk=user_id).first()

    if (offer is None) or (user is None) or not (action in ["accept", "reject"]):
        return HttpResponseNotFound('<h1>Page not found</h1>')

    with transaction.atomic():
        if action == "accept":
            offer.waiting_participants.remove(user)
            offer.current_participants.add(user)

            notification = Notification(user=user, offer=offer, action="OFFER_APPLICATION_ACCEPTED")
            notification.save()
        elif action == "reject":
            offer.waiting_participants.remove(user)
            
            offer.num_participants -= 1
            offer.save()
            
            user.profile.timecredit += offer.timecredit
            user.profile.save()

            notification = Notification(user=user, offer=offer, action="OFFER_APPLICATION_REJECTED")
            notification.save()
    
    return HttpResponseRedirect(offer.get_absolute_url())
