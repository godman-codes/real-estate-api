from django.urls import path
from .views import ListingCreateAPIView, ListingUpdateAPIView, ListingDestroyAPIView, SearchListingView



urlpatterns = [
    path('', ListingCreateAPIView.as_view()),
    path('<str:slug>/update/', ListingUpdateAPIView.as_view()),
    path('<str:slug>/delete/', ListingDestroyAPIView.as_view()),
    path('search/', SearchListingView.as_view()),
]