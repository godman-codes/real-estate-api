from rest_framework import serializers
from .models import Listing

class ListingSerializers(serializers.ModelSerializer):
    realtor = serializers.EmailField(read_only=True)
    title = serializers.CharField(max_length=255, required=True)
    slug = serializers.SlugField(required=True)
    address = serializers.CharField(max_length=255, required=True)
    city = serializers.CharField(max_length=255, required=True)
    state = serializers.CharField(max_length=255, required=True)
    zipcode = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField( required=True)
    price = serializers.IntegerField( required=True)
    bedrooms = serializers.IntegerField( required=True)
    bathrooms = serializers.DecimalField(max_digits=3, decimal_places=1, required=True)
    sale_type = serializers.CharField(max_length=10, required=True)
    home_type = serializers.CharField(max_length=10, required=True)
    main_photo = serializers.ImageField( required=True)
    photo_1 = serializers.ImageField(required=True)
    photo_2 = serializers.ImageField(required=True)
    photo_3 = serializers.ImageField(required=True)
    is_published = serializers.BooleanField()
    date_created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Listing
        fields = [
            'realtor',
            'title',
            'slug',
            'address',
            'city',
            'state',
            'zipcode',
            'description',
            'price',
            'bedrooms',
            'bathrooms',
            'sale_type',
            'home_type',
            'main_photo',
            'photo_1',
            'photo_2',
            'photo_3',
            'is_published',
            'date_created',
        ]