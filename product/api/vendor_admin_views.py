from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from product.models import Product
from product.vendorSerializers import VendorProductListSerializer, VendorProductCreateSerializer
from product.pagination import ProductCustomPagination

class VendorAdminProductListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VendorProductListSerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'id'
    lookup_url_kwarg = "id"
    def get_queryset(self):
        id = self.kwargs['id']
        if id:
            queryset = Product.objects.filter(vendor_id=id, status='ACTIVE').order_by('-created_at')
        else:
            queryset = Product.objects.filter(status='ACTIVE').order_by('-created_at')
        return queryset

class VendorAdminProductCreateAPI(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VendorProductCreateSerializer

    def post(self, request, *args, **kwargs):
        return super(VendorAdminProductCreateAPI, self).post(request, *args, **kwargs)