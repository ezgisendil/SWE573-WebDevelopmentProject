from django.urls import path
from .views import (FeedbackCreateView, NotificationListView, OfferListView, OfferDetailView, OfferCreateView, OfferUpdateView, OfferDeleteView)
from . import views

urlpatterns =[
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