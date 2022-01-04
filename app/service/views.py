from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Event, Offer, Feedback, Notification, Message
from .forms import PostForm, EventForm, OfferForm, FeedbackForm, MessageForm, AdvancedSearchForm
from django.db import IntegrityError, transaction
from accounts.models import Profile
from itertools import chain

# to handle traffic create home
def home(request):
    context = {
        #following user'lari dB'den cekerek onlarin postlarini al - not all
        'posts': Post.objects.all() 
    }
    return render(request, 'service/home.html', context)

def about(request):
    return render(request, 'service/about.html', {'title': 'About'})

def search(request):
    if request.method == Post:
        return render(request, 'search.html', {})


# Request Service
#Home Page
class HomeListView(ListView):

    template_name = 'service/home.html'  # <app> / <model>_<viewtype>.html
    context_object_name = 'items'
    ordering = ['-date_posted']
    paginate_by = 6

    def get_queryset(self):
        posts = Post.objects.order_by('-date_posted').order_by('-date_posted')
        events = Event.objects.order_by('-date_posted').order_by('-date_posted')
        offers = Offer.objects.order_by('-date_posted').order_by('-date_posted')

        res = sorted(
            chain(posts, events, offers),
            key=lambda instance: instance.date_posted, reverse=True)

        return res

def following_user_posts(request):
    profile = Profile.objects.get(user=request.user)
    users = [user for user in profile.following.all()]
    following_posts = []
    qs = None
    for u in users:
        offer = Offer.objects.filter(author=u)
        post = Post.objects.filter(author=u)
        event = Event.objects.filter(author=u)
        following_posts.append(offer)
        following_posts.append(post)
        following_posts.append(event)   
    return render(request, 'service/recommendation.html', {'following_posts':following_posts})


class SearchListView(ListView):

    model = Post
    template_name = 'service/search_results.html'  # <app> / <model>_<viewtype>.html

    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.order_by('-date_posted').order_by('-date_posted')
        context['events'] = Event.objects.order_by('-date_posted').order_by('-date_posted')
        context['offers'] = Offer.objects.order_by('-date_posted').order_by('-date_posted')

        q = self.request.GET.get("q", None)

        if q and len(q) > 0:
            query = Q(title__icontains=q) | Q(content__icontains=q)
            context['posts'] = context['posts'].filter(query)
            context['events'] = context['events'].filter(query)
            context['offers'] = context['offers'].filter(query)
        
        loc = self.request.GET.get("loc", None)

        if loc and len(loc) > 0 and loc != "All":
            query = Q(location__icontains=loc)
            context['posts'] = context['posts'].filter(query)
            context['events'] = context['events'].filter(query)
            context['offers'] = context['offers'].filter(query)
        
        from_date = self.request.GET.get("from_date", None)
        to_date = self.request.GET.get("to_date", None)

        if to_date and from_date:
            query = Q(date__range=(from_date, to_date))
            context['posts'] = context['posts'].filter(query)
            context['events'] = context['events'].filter(query)
            context['offers'] = context['offers'].filter(query)

        return context

class PostListView(ListView):
    model = Post
    template_name = 'service/post_list.html'  # <app> / <model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4

    def get_queryset(self):
        username = self.kwargs.get('username')
        res = Post.objects.filter(author__username=username).order_by('-date_posted').order_by('-date_posted').all()

        return res

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    #fields = ['title', 'content','location','date']
    form_class = PostForm
    def form_valid(self, form):
        form.instance.author = self.request.user #author of the form
        return super().form_valid(form)  #validate the form

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content','location','date', 'time', 'duration']
    
    def form_valid(self, form):
        form.instance.author = self.request.user #author of the form
        return super().form_valid(form)  #validate the form
    
    def test_func(self):
        post = self.get_object()
        # if current user is the author of the post
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' #after being deleted, delete the post and redirect to home page

    def test_func(self):
        post = self.get_object()
        # if current user is the author of the post
        if self.request.user == post.author:
            return True
        return False

#user's requests 
class UserPostListView(ListView):
    model = Post
    template_name = 'service/user_posts.html'  # <app> / <model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5
    #modify queryset
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted').order_by('-date_posted')

class UserPostListViewFixed(ListView):

    model = Post
    template_name = 'service/user_posts.html'  # <app> / <model>_<viewtype>.html

    def get_context_data(self, **kwargs):
        context = super(UserPostListViewFixed, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        my_profile = Profile.objects.get(user=self.request.user)

        if user in my_profile.following.all():
            follow = True
        else:
            follow = False

        context['follow'] = follow
        context['posts'] = Post.objects.filter(author=user).order_by('-date_posted').order_by('-date_posted')
        context['events'] = Event.objects.filter(author=user).order_by('-date_posted').order_by('-date_posted')
        context['offers'] = Offer.objects.filter(author=user).order_by('-date_posted').order_by('-date_posted')
        context['author'] = user
        
        return context

def follow(request):
    if request.method=="POST":
        my_profile = Profile.objects.get(user=request.user)
        print(my_profile)
        pk = request.POST.get('profile_user')
        print(pk)
        obj = Profile.objects.get(pk=pk)
        print(obj)

        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
            obj.follower.remove(my_profile.user)
        else:
            my_profile.following.add(obj.user)
            obj.follower.add(my_profile.user)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('user-posts')


#Organize Event
class EventListView(ListView):
    model = Event
    template_name = 'service/event_list.html'  # <app> / <model>_<viewtype>.html
    context_object_name = 'events'
    ordering = ['-date_posted']
    paginate_by = 4

    def get_queryset(self):
        username = self.kwargs.get('username')
        filter = self.kwargs.get('filter')
        res = Event.objects

        if username:
            res = res.filter(author__username=username)
        elif filter == "waiting":
            res = res.filter(waiting_participant=self.request.user)
        elif filter == "current":
            res = res.filter(current_participant=self.request.user)

        res = res.order_by('-date_posted').order_by('-date_posted')
        return res

class EventDetailView(DetailView):
    model = Event
    context_object_name = 'event'

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    #fields = ['title', 'content','location','date']
    form_class = EventForm
    def form_valid(self, form):
        form.instance.author = self.request.user #author of the form
        return super().form_valid(form)  #validate the form

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['title', 'content', 'max_participant', 'location','date', 'time', 'duration']
    #form_class = EventForm
    
    def form_valid(self, form):
        form.instance.author = self.request.user #author of the form
        return super().form_valid(form)  #validate the form
    
    def test_func(self):
        event = self.get_object()
        # if current user is the author of the post
        if self.request.user == event.author:
            return True
        return False

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = '/' #after being deleted, delete the post and redirect to home page

    def test_func(self):
        event = self.get_object()
        # if current user is the author of the post
        if self.request.user == event.author:
            return True
        return False


#user's events 
class UserEventListView(ListView):
    model = Event
    template_name = 'service/user_posts.html'  # <app> / <model>_<viewtype>.html
    context_object_name = 'events'
    paginate_by = 5
    #modify queryset
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted').order_by('-date_posted')

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

class AdvancedSearchView(LoginRequiredMixin, FormView):
    model = Offer
    form_class = AdvancedSearchForm
    template_name = 'service/advanced_search.html'  # <app> / <model>_<viewtype>.html

    def form_valid(self, form):
        from django.db.models import Q

        is_valid = super().form_valid(form)
        
        return is_valid

class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    #fields = ['title', 'content','location','date']
    form_class = FeedbackForm
    def form_valid(self, form):
        form.instance.sender = self.request.user #author of the form

        receiver = User.objects.filter(username=self.kwargs.get("receiver")).first()
        form.instance.receiver = receiver

        offer = Offer.objects.filter(pk=self.kwargs.get('pk')).first()
        form.instance.offer = offer
        
        response = super().form_valid(form)  #validate the form

        with transaction.atomic():
            if offer.author == receiver:
                notification = Notification(user=offer.author, offer=offer, action="OFFER_NEW_FEEDBACK")
                notification.save()
            
            if offer.feedbacks.filter(Q(sender=receiver) & Q(receiver=self.request.user)).exists():
                participant = receiver if offer.author != receiver else self.request.user
                offer.current_participants.remove(participant)
                offer.finished_participants.add(participant)
                offer.author.profile.timecredit += offer.timecredit
                offer.author.profile.save()

                participant.profile.timecredit_hold -= offer.timecredit
                participant.profile.save()


        return response

    def get_context_data(self, **kwargs):
        context = super(FeedbackCreateView, self).get_context_data(**kwargs)
        context["receiver"] = self.kwargs.get("receiver")

        return context

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    #fields = ['title', 'content','location','date']
    form_class = MessageForm
    def form_valid(self, form):
        from django.db.models import Q

        form.instance.sender = self.request.user #author of the form
        form.instance.receiver = User.objects.filter(username=self.kwargs.get("username")).first() #author of the form
        return super().form_valid(form)  #validate the form
    
    def get_context_data(self, **kwargs):
        other_user =  User.objects.filter(username=self.kwargs.get("username")).first()
        print(self.request.user, other_user)
        kwargs['private_messages'] = Message.objects.filter(
            (Q(receiver=self.request.user) & Q(sender = other_user)) | 
            (Q(sender=self.request.user) & Q(receiver = other_user))
        ).order_by('date_posted').order_by('date_posted').all()
        
        kwargs['receiver'] = other_user
        
        return super(MessageCreateView, self).get_context_data(**kwargs)


class OfferUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Offer
    fields = ['title', 'content','max_participants','timecredit','location','date', 'time', 'duration']
    
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
    template_name = 'service/offer_list.html'  # <app> / <model>_<viewtype>.html
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
    template_name = 'service/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 5

    def get_queryset(self):
        res = Notification.objects.filter(user=self.request.user).order_by('-date_posted').order_by('-date_posted').all()

        return res

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'service/message_list.html'
    context_object_name = 'users_list'
    paginate_by = 5

    def get_queryset(self):
        res = Message.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user)).order_by('-date_posted').order_by('-date_posted')

        users_list = list(set(list(res.values_list("sender__username", flat=True)) + list(res.values_list("receiver__username", flat=True))))

        if self.request.user.username in users_list:
            users_list.remove(self.request.user.username)
        return users_list

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
            request.user.profile.timecredit_hold += offer.timecredit
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
            user.profile.timecredit_hold -= offer.timecredit

            user.profile.save()

            notification = Notification(user=user, offer=offer, action="OFFER_APPLICATION_REJECTED")
            notification.save()
    
    return HttpResponseRedirect(offer.get_absolute_url())

def apply_event(request, pk):
    event = Event.objects.filter(pk=pk).first()

    print(request.user)

    if event is None:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    if not request.user in event.waiting_participant.all():
        with transaction.atomic():
            event.waiting_participant.add(request.user)

            event.num_participant += 1
            event.save()

            request.user.profile.save()

            notification = Notification(user=event.author, event=event, action="EVENT_NEW_APPLICATION")
            notification.save()

    return HttpResponseRedirect(event.get_absolute_url())

def event_action(request, pk, action, user_id):
    print(pk, action, user_id)

    event = Event.objects.filter(pk=pk).first()
    user = event.waiting_participant.filter(pk=user_id).first()

    if (event is None) or (user is None) or not (action in ["accept", "reject"]):
        return HttpResponseNotFound('<h1>Page not found</h1>')

    with transaction.atomic():
        if action == "accept":
            event.waiting_participant.remove(user)
            event.current_participant.add(user)

            notification = Notification(user=user, event=event, action="EVENT_APPLICATION_ACCEPTED")
            notification.save()
        elif action == "reject":
            event.waiting_participant.remove(user)
            
            event.num_participant -= 1
            event.save()
            
            user.profile.timecredit += event.timecredit
            user.profile.timecredit_hold -= event.timecredit

            user.profile.save()

            notification = Notification(user=user, event=event, action="EVENT_APPLICATION_REJECTED")
            notification.save()
    
    return HttpResponseRedirect(event.get_absolute_url())

class FollowingListView(ListView):
    model = Profile
    template_name = 'service/following.html'
    context_object_name = 'followings'

    # exclude current user
    def get_query(self):
        return Profile.objects.all().exclude(user=self.request.user)

class FollowerListView(ListView):
    model = Profile
    template_name = 'service/follower.html'
    context_object_name = 'followers'

    # exclude current user
    def get_query(self):
        return Profile.objects.all().exclude(user=self.request.user)