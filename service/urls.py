from django.urls import path
from .views import (PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView,
                    EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name = 'service-home'), #views.home changed to postlistview
    path('profile/<str:username>', UserPostListView.as_view(), name = 'user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),  
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name = 'post-delete'),
    path('about/', views.about, name = 'service-about'),

    path('event/<int:pk>/', EventDetailView.as_view(), name = 'event-detail'),
    path('event/new/', EventCreateView.as_view(), name = 'event-create'),  
    path('event/<int:pk>/update/', EventUpdateView.as_view(), name = 'event-update'),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name = 'event-delete'),

]



'''
    path('request/<int:pk>/', RequestDetailView.as_view(), name = 'request-detail'),
    path('request/new/', RequestCreateView.as_view(), name = 'request-create'),  
    path('request/<int:pk>/update/', RequestUpdateView.as_view(), name = 'request-update'),
    path('request/<int:pk>/delete/', RequestDeleteView.as_view(), name = 'request-delete'),
'''