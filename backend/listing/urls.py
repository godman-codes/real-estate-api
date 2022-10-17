from django.urls import path
from .views import ListingCreateAPIView, ListingUpdateAPIView



urlpatterns = [
    path('', ListingCreateAPIView.as_view()),
    path('<str:slug>/update/', ListingUpdateAPIView.as_view())
]