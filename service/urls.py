from django.urls import path
from .views import (FeedbackCreateView, HomeListView, NotificationListView, OfferCreateView, OfferDeleteView, OfferDetailView, OfferListView, OfferUpdateView, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView,
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

    path('offer/<int:pk>/', OfferDetailView.as_view(), name = 'offer-detail'),
    path('offer/list/', OfferListView.as_view(), name = 'offer-list'),
    path('offer/list/my/<str:filter>/', OfferListView.as_view(), name = 'applied-offer-list'),
    path('offer/list/<str:username>/', OfferListView.as_view(), name = 'offer-list-user'),
    path('offer/new/', OfferCreateView.as_view(), name = 'offer-create'),  
    path('offer/<int:pk>/feedback/', FeedbackCreateView.as_view(), name = 'feedback-create'),  
    path('offer/<int:pk>/update/', OfferUpdateView.as_view(), name = 'offer-update'),
    path('offer/<int:pk>/delete/', OfferDeleteView.as_view(), name = 'offer-delete'),
    path('offer/<int:pk>/apply/', views.apply_offer, name = 'offer-apply'),
    path('offer/<int:pk>/<str:action>/<int:user_id>/', views.offer_action, name = 'offer-action'),
    path('notifications/', NotificationListView.as_view(), name= 'notifications-list'),

]



'''
    path('request/<int:pk>/', RequestDetailView.as_view(), name = 'request-detail'),
    path('request/new/', RequestCreateView.as_view(), name = 'request-create'),  
    path('request/<int:pk>/update/', RequestUpdateView.as_view(), name = 'request-update'),
    path('request/<int:pk>/delete/', RequestDeleteView.as_view(), name = 'request-delete'),
'''