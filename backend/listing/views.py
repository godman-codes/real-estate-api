from rest_framework import generics
from .models import Listing
from .serializers import ListingSerializers
from .permissions import IsRealtorPermission

class ListingCreateAPIView(IsRealtorPermission, generics.CreateAPIView):
    '''
    create Listings
    '''
    permission_classes = [IsRealtorPermission]
    queryset = Listing.objects.all()
    serializer_class = ListingSerializers

    def perform_create(self, serializer):
        # print(serializer.validated_data)
        print(self.request)
        user = self.request.user
        serializer.save(realtor=user)

