from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Listing
from .serializers import ListUpdateSerializer, ListingSerializers
from .permissions import IsRealtorPermission
from rest_framework.views import APIView
from django.contrib.postgres.search import SearchVector, SearchQuery

class ListingCreateAPIView(generics.CreateAPIView):
    '''
    create Listings
    '''
    permission_classes = [IsAuthenticated, IsRealtorPermission]
    queryset = Listing.objects.all()
    serializer_class = ListingSerializers

    def perform_create(self, serializer):
        # print(serializer.validated_data)
        user = self.request.user
        serializer.save(realtor=user)

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            slug = request.query_params.get('slug')
            if not slug:
                listings = Listing.objects.order_by('-date_created').filter(
                    realtor=user.email
                )
                listings = ListingSerializers(listings, many=True)
                return Response({
                    'listing': listings.data,
                }, status=status.HTTP_200_OK) 
            if not Listing.objects.filter(
                slug=slug,
                realtor=user.email
                ).exists():
                return Response(
                    {'error': 'listing does not exist'},
                                status=status.HTTP_404_NOT_FOUND
                                )
            listing = Listing.objects.get(realtor=user.email, slug=slug)
            listing = ListingSerializers(listing)
            return Response({
                'listing': listing.data,
            }, status=status.HTTP_200_OK)
        except:
            return Response(
                {'error': 'something went wrong while getting listings'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

class ListingUpdateAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsRealtorPermission]
    queryset = Listing.objects.all()
    serializer_class = ListUpdateSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Listing.objects.filter(realtor=self.request.user)
        return queryset

    def perform_update(self, serializer):
        # print(self.request.user.email)
        # print(serializer.data)
        # print(self.queryset)
        serializer.save(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class ListingDestroyAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsRealtorPermission]
    queryset = Listing.objects.all()
    serializer_class = ListUpdateSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Listing.objects.filter(realtor=self.request.user)
        return queryset

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


class SearchListingView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request, *args, **kwargs):
        try:
            city = request.query_params.get('city')
            state = request.query_params.get('state')
            max_price = request.query_params.get('max_price')
            try:
                max_price = int(max_price)
            except:
                return Response(
                    {'error': 'Max price must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            bedrooms = request.query_params.get('bedrooms')
            try:
                bedrooms = int(bedrooms)
            except:
                return Response(
                    {'error': 'Number of bedrooms must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            bathrooms = request.query_params.get('bathrooms')
            try:
                bathrooms = float(bathrooms)
                bathrooms = round(bathrooms, 1)
            except:
                return Response(
                    {'error': 'Bathrooms must be an integer or a float'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            sale_type = request.query_params.get('sale_type')
            if sale_type.lower() == 'for sale':
                sale_type = 'FOR_SALE'
            else: 
                sale_type = 'FOR_RENT'
            home_type = request.query_params.get('home_type')
            if home_type.lower() == 'townhouse':
                home_type = 'TOWNHOUSE'
            elif home_type.lower() == 'condo':
                home_type = 'CONDO'
            else:
                home_type = 'HOUSE'

            try:
                search = request.query_params.get('search')
            except:
                return Response({'error': 'Must pass search criteria'},
                                status=status.HTTP_400_BAD_REQUEST)
            
            vector = SearchVector('title', 'description')
            query = SearchQuery(search)
            if not Listing.objects.annotate(
                search=vector
                ).filter(
                    search=query,
                    city=city,
                    state=state,
                    price__lte=max_price,
                    bedrooms__gte=bedrooms,
                    bathrooms__gte=bathrooms,
                    sale_type=sale_type,
                    home_type=home_type,
                    is_published=True
                    ).exists():
                    return Response(
                        {'error': 'No listing found with this criteria'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                    
            listings = Listing.objects.annotate(
                search=vector
                ).filter(
                    search=query,
                    city=city,
                    state=state,
                    price__lte=max_price,
                    bedrooms__gte=bedrooms,
                    bathrooms__gte=bathrooms,
                    sale_type=sale_type,
                    home_type=home_type,
                    is_published=True
                    )
            listings = ListingSerializers(listings, many=True)
            
            return Response(
                {'listing': listings.data},
                status=status.HTTP_200_OK
                )
        except:
            return Response(
                {'error': 'something went wrong during search'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        