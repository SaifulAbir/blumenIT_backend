from django.db.models import Q
from product.pagination import ProductCustomPagination
from product.serializers import ProductCreateSerializer, ProductListSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from product.models import Brand, Category, Product, SubCategory, SubSubCategory, Units
from user.models import User
from vendor.models import VendorRequest, Vendor
from vendor.serializers import VendorBrandSerializer, VendorCategorySerializer, VendorRequestSerializer, VendorCreateSerializer, OrganizationNameSerializer, \
    VendorDetailSerializer, StoreSettingsSerializer, VendorSubCategorySerializer, VendorSubSubCategorySerializer, VendorUnitSerializer
from rest_framework.response import Response
from user.models import User
from rest_framework.exceptions import ValidationError


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


class StoreSettingsUpdateAPIView(CreateAPIView):
    serializer_class = StoreSettingsSerializer


class OrganizationNamesListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = VendorRequest.objects.all()
    serializer_class = OrganizationNameSerializer


class VendorDetailAPIView(RetrieveUpdateAPIView):
    serializer_class = VendorDetailSerializer

    def get_object(self):
        vendor = Vendor.objects.get(vendor_admin=self.request.user)
        return vendor


class VendorCategoryListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.filter(is_active=True)
    serializer_class = VendorCategorySerializer


class VendorSubCategoryListAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VendorSubCategorySerializer
    lookup_field = 'cid'
    lookup_url_kwarg = "cid"

    def get_queryset(self):
        cid = self.kwargs['cid']
        if cid:
            queryset = SubCategory.objects.filter(
                category=cid, is_active=True).order_by('-created_at')
        else:
            queryset = SubCategory.objects.filter(
                is_active=True).order_by('-created_at')
        return queryset


class VendorSubSubCategoryListAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VendorSubSubCategorySerializer
    lookup_field = 'cid'
    lookup_url_kwarg = "cid"

    def get_queryset(self):
        cid = self.kwargs['cid']
        if cid:
            queryset = SubSubCategory.objects.filter(
                category=cid, is_active=True).order_by('-created_at')
        else:
            queryset = SubSubCategory.objects.filter(
                is_active=True).order_by('-created_at')
        return queryset


class VendorBrandListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = VendorBrandSerializer


class VendorUnitListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Units.objects.filter(is_active=True)
    serializer_class = VendorUnitSerializer


class VendorProductListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductListSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if Vendor.objects.filter(vendor_admin=User.objects.get(id=self.request.user.id)).exists():
            vid = Vendor.objects.get(
                vendor_admin=User.objects.get(id=self.request.user.id))
            if vid:
                queryset = Product.objects.filter(
                    vendor=vid, status='ACTIVE').order_by('-created_at')
                return queryset
        else:
            raise ValidationError({"msg": 'You are not a vendor.'})

    # def get_queryset(self):
    #     cid = self.kwargs['cid']
    #     if cid:
    #         queryset = Product.objects.filter(category=cid, status='ACTIVE').order_by('-created_at')
    #     else:
    #         queryset = Product.objects.filter(status='ACTIVE').order_by('-created_at')
    #     return queryset

    # def get(self, request):
    #     if Vendor.objects.filter(vendor_admin = User.objects.get(id = self.request.user.id)).exists():
    #         vid = Vendor.objects.get(vendor_admin = User.objects.get(id = self.request.user.id))
    #         if vid:
    #             products = Product.objects.filter(vendor=vid, status='ACTIVE').order_by('-created_at')

    #             result = list(products)
    #         else:
    #             result = []
    #         serializer = ProductListSerializer(result, many=True)
    #         return Response({"result": serializer.data})
    #     else:
    #         return Response({"result": "You are not a vendor"})


class VendorProductCreateAPIView(CreateAPIView):
    # permission_classes = (AllowAny,)
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return super(VendorProductCreateAPIView, self).post(request, *args, **kwargs)
