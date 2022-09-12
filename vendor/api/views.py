from datetime import datetime
from django.db.models import Q
from product.pagination import ProductCustomPagination
from product.serializers import DiscountTypeSerializer, ProductAttributesSerializer, ProductCreateSerializer, ProductDetailsSerializer, ProductTagsSerializer, ProductUpdateSerializer, VariantTypeSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from product.models import Brand, Category, DiscountTypes, Product, ProductAttributes, ProductReview, ProductTags, SubCategory, SubSubCategory, Units, VariantType
from user.models import CustomerProfile, User
from vendor.models import VendorRequest, Vendor
from vendor.serializers import VendorBrandSerializer, VendorCategorySerializer, VendorProductDetailsSerializer, VendorProductListSerializer, VendorRequestSerializer, VendorCreateSerializer, OrganizationNameSerializer, \
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
    lookup_field = 'sid'
    lookup_url_kwarg = "sid"

    def get_queryset(self):
        sid = self.kwargs['sid']
        if sid:
            queryset = SubSubCategory.objects.filter(
                sub_category=sid, is_active=True).order_by('-created_at')
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


class VendorDiscountListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = DiscountTypes.objects.filter(is_active=True)
    serializer_class = DiscountTypeSerializer


class VendorTagListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = ProductTags.objects.filter(is_active=True)
    serializer_class = ProductTagsSerializer


class VendorAttributeListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = ProductAttributes.objects.filter(is_active=True)
    serializer_class = ProductAttributesSerializer


class VendorVariantListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = VariantType.objects.filter(is_active=True)
    serializer_class = VariantTypeSerializer


class VendorProductListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorProductListSerializer
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


class VendorProductCreateAPIView(CreateAPIView):
    # permission_classes = (AllowAny,)
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return super(VendorProductCreateAPIView, self).post(request, *args, **kwargs)


class VendorProductUpdateAPIView(RetrieveUpdateAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = (AllowAny,)
    serializer_class = ProductUpdateSerializer
    # serializer_class = ProductCreateSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs['slug']
        print(slug)
        query = Product.objects.filter(slug=slug)
        return query

    # def put(self, request, *args, **kwargs):
    #     print('Put')
    #     return self.update(request, *args, **kwargs)


class VendorProductDetailsAPI(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorProductDetailsSerializer
    lookup_field = 'slugi'
    lookup_url_kwarg = "slugi"

    def get_object(self):
        slug = self.kwargs['slugi']
        if Vendor.objects.filter(vendor_admin=User.objects.get(id=self.request.user.id)).exists():
            vid = Vendor.objects.get(
                vendor_admin=User.objects.get(id=self.request.user.id))
            if vid:
                try:
                    query = Product.objects.get(slug=slug, vendor=vid)
                    if query:
                        return query
                    else:
                        raise ValidationError(
                            {"msg": 'You are not creator of this product!'})
                except:
                    raise ValidationError(
                        {"msg": "Product doesn't exist!"})
        else:
            raise ValidationError({"msg": 'You are not a vendor.'})
