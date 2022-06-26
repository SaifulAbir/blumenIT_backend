from django.db.models import Q
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from vendor.models import VendorRequest, Vendor
from vendor.serializers import VendorRequestSerializer, VendorCreateSerializer, OrganizationNameSerializer, \
    VendorDetailSerializer


class VendorRequestAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = VendorRequestSerializer

    def post(self, request, *args, **kwargs):
        return super(VendorRequestAPIView, self).post(request, *args, **kwargs)


class VendorRequestListAPI(ListAPIView):
    queryset = VendorRequest.objects.all()
    serializer_class = VendorRequestSerializer


class VendorCreateAPIView(CreateAPIView):
    serializer_class = VendorCreateSerializer

class OrganizationNamesListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = VendorRequest.objects.all()
    serializer_class = OrganizationNameSerializer


class VendorDetailAPIView(RetrieveUpdateAPIView):
    serializer_class = VendorDetailSerializer

    def get_object(self):
        vendor = Vendor.objects.get(vendor_admin=self.request.user)
        return vendor