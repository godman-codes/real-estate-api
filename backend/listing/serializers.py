from rest_framework import serializers
from .models import Listing
from .validators import validate_slug, validate_house_type, validate_sale_type

SALE_CHOICES = (
    ('FOR_RENT', 'For Rent'),
    ('FOR_SALE', 'For Sale'),
)

HOUSE_CHOICES = (
    ('HOUSE', 'House'),
    ('CONDO', 'Condo'),
    ('TOWNHOUSE', 'Townhouse'),
)
class ListingSerializers(serializers.ModelSerializer):
    realtor = serializers.EmailField(read_only=True)
    title = serializers.CharField(max_length=255, required=True)
    slug = serializers.SlugField(required=True, validators=[validate_slug])
    address = serializers.CharField(max_length=255, required=True)
    city = serializers.CharField(max_length=255, required=True)
    state = serializers.CharField(max_length=255, required=True)
    zipcode = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField( required=True)
    price = serializers.IntegerField( required=True)
    bedrooms = serializers.IntegerField( required=True)
    bathrooms = serializers.DecimalField(max_digits=3, decimal_places=1, required=True)
    sale_type = serializers.ChoiceField(choices=SALE_CHOICES, required=True, validators=[validate_sale_type])
    home_type = serializers.ChoiceField(choices=HOUSE_CHOICES, required=True, validators=[validate_house_type])
    main_photo = serializers.ImageField( required=True)
    photo_1 = serializers.ImageField(required=True)
    photo_2 = serializers.ImageField(required=True)
    photo_3 = serializers.ImageField(required=True)
    is_published = serializers.BooleanField()
    date_created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id',
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


class ListUpdateSerializer(ListingSerializers):
    slug = serializers.SlugField(required=True)