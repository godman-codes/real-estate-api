from django.urls import path
from .views import ListingCreateAPIView
urlpatterns = [
    path('create/', ListingCreateAPIView.as_view())
]