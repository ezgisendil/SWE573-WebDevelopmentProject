from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Event
from .forms import PostForm, EventForm

# Create your views here.
# dummy data to create posts
# posts = [
#     {
#         'author': 'author2',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'August 27, 2021',
#     },
#     {
#         'author': 'author',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'October 27, 2021',
#     },
# ]

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
class PostListView(ListView):
    model = Post
    template_name = 'service/home.html'  # <app> / <model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    #fields = ['title', 'content','location','date']
    form_class = PostForm
    def form_valid(self, form):
        form.instance.author = self.request.user #author of the form
        return super().form_valid(form)  #validate the form

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['image','title', 'content','location','date']
    
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


#Organize Event
class EventListView(ListView):
    model = Event
    template_name = 'service/home.html'  # <app> / <model>_<viewtype>.html
    context_object_name = 'events'
    ordering = ['-date_posted']
    paginate_by = 4

class EventDetailView(DetailView):
    model = Event

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    #fields = ['title', 'content','location','date']
    form_class = EventForm
    def form_valid(self, form):
        form.instance.author = self.request.user #author of the form
        return super().form_valid(form)  #validate the form

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    #fields = ['title', 'content','location','date']
    form_class = EventForm
    
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