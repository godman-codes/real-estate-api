from multiprocessing import managers
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Listing
from .serializers import ListUpdateSerializer, ListingSerializers
from .permissions import IsRealtorPermission
from rest_framework.views import APIView
from django.contrib.postgres.search import SearchVector

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
            search = request.query_params.get('search') or None
            # listing = Listing.objects.filter(
            #     title__search=search,
            #     description=search,
            #     is_published=True
            #     )
            if not Listing.objects.annotate(
                search=SearchVector('title', 'description')
                ).filter(
                    search=search,
                    is_published=True
                    ):
                    return Response(
                        {'error': 'No listing for you'},
                        status=status.HTTP_404_NOT_FOUND
                    )
            
            listing = Listing.objects.annotate(
            search=SearchVector('title', 'description')
            ).filter(
                search=search,
                is_published=True
                )
            listing = ListingSerializers(listing, many=True)
            
            return Response(
                {'listing': listing.data},
                status=status.HTTP_200_OK
                )
        except:
            return Response(
                {'error': 'something went wrong during search'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        