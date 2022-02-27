from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from vendor.models import VendorRequest
from vendor.serializers import VendorRequestSerializer, VendorCreateSerializer


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