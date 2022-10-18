from rest_framework import serializers
from .models import Listing

def validate_slug(value):
    qs = Listing.objects.filter(slug__iexact=value)
    if qs.exists():
        raise serializers.ValidationError('Listing with slug already exists')
    return value

def validate_sale_type(value):
    if value == 'FOR_SALE':
        return 'For Sale'
    elif value == 'FOR_RENT':
        return 'For Rent'
    else:
        raise serializers.ValidationError('Sale type must be either FOR_SALE or FOR_RENT')


def validate_house_type(value):
    if value == 'HOUSE':
        return 'House'
    elif value == 'CONDO':
        return 'Condo'
    elif value == 'TOWNHOUSE':
        return 'Townhouse'
    else:
        raise serializers.ValidationError('House type must be either HOUSE, CONDO or TOWNHOUSE')