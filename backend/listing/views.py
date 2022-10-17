from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Listing
from .serializers import ListUpdateSerializer, ListingSerializers
from .permissions import IsRealtorPermission

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
                status=status.HTTP_400_BAD_REQUEST
                )

class ListingUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsRealtorPermission]
    queryset = Listing.objects.all()
    serializer_class = ListUpdateSerializer
    lookup_field = 'slug'

    def perform_update(self, serializer):
        print(self.request.user)
        # print(serializer.data)
        serializer.save(user=self.request.user)