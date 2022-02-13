from rest_framework.generics import CreateAPIView
from vendor.serializers import VendorRequestSerializer


class VendorRequestAPIView(CreateAPIView):
    serializer_class = VendorRequestSerializer

    def post(self, request, *args, **kwargs):
        return super(VendorRequestAPIView, self).post(request, *args, **kwargs)