from rest_framework import serializers
from .models import Listing

def validate_slug(value):
    qs = Listing.objects.filter(slug__iexact=value)
    if qs.exists():
        raise serializers.ValidationError('Listing with slug already exists')
    return value