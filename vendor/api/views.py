from datetime import datetime
from django.db.models import Q
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from product.pagination import ProductCustomPagination
from product.serializers import DiscountTypeSerializer, ProductTagsSerializer, TagsSerializer, VariantTypeSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from product.models import Brand, Category, DiscountTypes, Product, ProductAttributes, ProductReview, ProductTags, SubCategory, SubSubCategory, Tags, Units, VariantType, ProductVideoProvider, VatType
from user.models import CustomerProfile, User
from vendor.models import VendorRequest, Vendor, Seller
from vendor.serializers import VendorAddNewSubCategorySerializer, VendorAddNewSubSubCategorySerializer,\
    VendorBrandSerializer, VendorCategorySerializer, VendorProductListSerializer,\
    SellerProductUpdateSerializer, VendorProductViewSerializer, \
    SellerDetailSerializer, VendorSubCategorySerializer, \
    VendorSubSubCategorySerializer, VendorUnitSerializer, SellerSerializer, ProductAttributesSerializer, \
    ProductVideoProviderSerializer, ProductVatProviderSerializer, VendorUpdateCategorySerializer,\
    VendorUpdateSubSubCategorySerializer, SellerProductCreateSerializer, SellerAddNewCategorySerializer, \
    SellerCreateSerializer, FlashDealCreateSerializer
from user.models import User
from cart.models import Coupon
from rest_framework.exceptions import ValidationError


class AdminCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SellerCreateSerializer

    def post(self, request, *args, **kwargs):
        return super(AdminCreateAPIView, self).post(request, *args, **kwargs)


class AdminDetailsAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = SellerSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_object(self):
        seller_id = self.kwargs['id']
        try:
            query = Seller.objects.get(id=seller_id)
            return query
        except:
            raise ValidationError({"details": "Seller doesn't exist!"})


class AdminListAPIView(ListAPIView):
    queryset = Seller.objects.filter(is_active=True)
    permission_classes = [AllowAny]
    serializer_class = SellerSerializer


class AdminUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SellerSerializer
    # queryset = Seller.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        seller_id = self.kwargs['id']
        query = Seller.objects.filter(id=seller_id)
        if query:
            return query
        else:
            raise ValidationError(
                {"msg": 'Seller not found'}
            )


class AdminDeleteAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SellerSerializer
    queryset = Seller.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        seller_id = self.kwargs['id']
        seller_obj = Seller.objects.filter(id=seller_id).exists()
        if seller_obj:
            seller_obj = Seller.objects.filter(id=seller_id)
            seller_obj.update(is_active=False)

            queryset = Seller.objects.filter(is_active=True).order_by('-created_at')
            return queryset
        else:
            raise ValidationError(
                {"msg": 'Seller Does not exist!'})


class AdminProductCreateAPIView(CreateAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = (AllowAny,)
    serializer_class = SellerProductCreateSerializer

    def post(self, request, *args, **kwargs):
        return super(AdminProductCreateAPIView, self).post(request, *args, **kwargs)


class AdminProductUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    serializer_class = SellerProductUpdateSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs['slug']
        query = Product.objects.filter(slug=slug)
        if query:
            return query
        else:
            raise ValidationError(
                {"msg": 'You Can not edit this product!'})


class AdminAddNewCategoryAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SellerAddNewCategorySerializer

    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return super(AdminAddNewCategoryAPIView, self).post(request, *args, **kwargs)

class AdminBrandListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = VendorBrandSerializer

class AdminUnitListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Units.objects.filter(is_active=True)
    serializer_class = VendorUnitSerializer

class AdminDiscountListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = DiscountTypes.objects.filter(is_active=True)
    serializer_class = DiscountTypeSerializer

class AdminTagListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    # queryset = ProductTags.objects.filter(is_active=True)
    queryset = Tags.objects.filter(is_active=True)
    # serializer_class = ProductTagsSerializer
    serializer_class = TagsSerializer

class VendorAttributeListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = ProductAttributes.objects.filter(is_active=True)
    serializer_class = ProductAttributesSerializer

class VendorVariantListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = VariantType.objects.filter(is_active=True)
    serializer_class = VariantTypeSerializer

class AdminProductListAPI(ListAPIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    serializer_class = VendorProductListSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        queryset = Product.objects.filter(status='ACTIVE').order_by('-created_at')
        if queryset:
            return queryset
        else:
            raise ValidationError({"msg": 'No active product available or You are not a vendor.'})

class AdminProductViewAPI(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = VendorProductViewSerializer
    lookup_field = 'slugi'
    lookup_url_kwarg = "slugi"

    def get_object(self):
        slug = self.kwargs['slugi']
        query = Product.objects.get(slug=slug)
        if query:
            return query
        else:
            raise ValidationError(
                {"msg": 'You can not view this product!'})

class AdminProductDeleteAPI(ListAPIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    serializer_class = VendorProductListSerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs['slug']
        product_obj_exist = Product.objects.filter(
            slug=slug).exists()
        if product_obj_exist:
            product_obj = Product.objects.filter(slug=slug)
            product_obj.update(status='UNPUBLISH')

            queryset = Product.objects.filter(status='ACTIVE').order_by('-created_at')
            return queryset
        else:
            raise ValidationError(
                {"msg": 'Product Does not exist!'})

class AdminVideoProviderListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = ProductVideoProvider.objects.filter(is_active=True)
    serializer_class = ProductVideoProviderSerializer

class AdminVatTypeListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = VatType.objects.filter(is_active=True)
    serializer_class = ProductVatProviderSerializer

class AdminCategoryListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.filter(is_active=True)
    serializer_class = VendorCategorySerializer

class AdminUpdateCategoryAPIView(RetrieveUpdateAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = VendorUpdateCategorySerializer
    lookup_field = 'ordering_number'
    lookup_url_kwarg = "ordering_number"

    def get_queryset(self):
        ordering_number = self.kwargs['ordering_number']
        query = Category.objects.filter(ordering_number=int(ordering_number))
        if query:
            return query
        else:
            raise ValidationError(
                {"msg": 'Category does not found!'})

class AdminDeleteCategoryAPIView(ListAPIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    serializer_class = VendorCategorySerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'ordering_number'
    lookup_url_kwarg = "ordering_number"

    def get_queryset(self):
        ordering_number = self.kwargs['ordering_number']
        category_obj_exist = Category.objects.filter(
            ordering_number=ordering_number).exists()
        if category_obj_exist:
            category_obj = Category.objects.filter(ordering_number=ordering_number)
            category_obj.update(is_active=False)

            queryset = Category.objects.filter(is_active=True).order_by('-created_at')
            return queryset
        else:
            raise ValidationError(
                {"msg": 'Category Does not exist!'})

class AdminSubCategoryListAPIView(ListAPIView):
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

class AdminAddNewSubCategoryAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VendorAddNewSubCategorySerializer

    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return super(AdminAddNewSubCategoryAPIView, self).post(request, *args, **kwargs)

class AdminUpdateSubCategoryAPIView(RetrieveUpdateAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = VendorUpdateCategorySerializer
    lookup_field = 'ordering_number'
    lookup_url_kwarg = "ordering_number"

    def get_queryset(self):
        ordering_number = self.kwargs['ordering_number']
        query = SubCategory.objects.filter(ordering_number=int(ordering_number))
        if query:
            return query
        else:
            raise ValidationError(
                {"msg": 'Sub Category does not found!'})

class AdminDeleteSubCategoryAPIView(ListAPIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    serializer_class = VendorSubCategorySerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'ordering_number'
    lookup_url_kwarg = "ordering_number"

    def get_queryset(self):
        ordering_number = self.kwargs['ordering_number']
        category_obj_exist = SubCategory.objects.filter(
            ordering_number=ordering_number).exists()
        if category_obj_exist:
            category_obj = SubCategory.objects.filter(ordering_number=ordering_number)
            category_obj.update(is_active=False)

            queryset = SubCategory.objects.filter(is_active=True).order_by('-created_at')
            return queryset
        else:
            raise ValidationError(
                {"msg": 'Sub Category Does not exist!'})

class AdminSubSubCategoryListAPIView(ListAPIView):
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

class AdminAddNewSubSubCategoryAPIView(CreateAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = (AllowAny,)
    serializer_class = VendorAddNewSubSubCategorySerializer


    def post(self, request, *args, **kwargs):
        return super(AdminAddNewSubSubCategoryAPIView, self).post(request, *args, **kwargs)

class AdminUpdateSubSubCategoryAPIView(RetrieveUpdateAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = VendorUpdateSubSubCategorySerializer
    lookup_field = 'ordering_number'
    lookup_url_kwarg = "ordering_number"

    def get_queryset(self):
        ordering_number = self.kwargs['ordering_number']
        query = SubSubCategory.objects.filter(ordering_number=int(ordering_number))
        if query:
            return query
        else:
            raise ValidationError(
                {"msg": 'Sub Sub Category does not found!'})

class AdminDeleteSubSubCategoryAPIView(ListAPIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    serializer_class = VendorSubCategorySerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'ordering_number'
    lookup_url_kwarg = "ordering_number"

    def get_queryset(self):
        ordering_number = self.kwargs['ordering_number']
        category_obj_exist = SubSubCategory.objects.filter(
            ordering_number=ordering_number).exists()
        if category_obj_exist:
            category_obj = SubSubCategory.objects.filter(ordering_number=ordering_number)
            category_obj.update(is_active=False)

            queryset = SubSubCategory.objects.filter(is_active=True).order_by('-created_at')
            return queryset
        else:
            raise ValidationError(
                {"msg": 'Sub Sub Category Does not exist!'})

class AdminFlashDealCreateAPIView(CreateAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = (AllowAny,)
    serializer_class = FlashDealCreateSerializer


    def post(self, request, *args, **kwargs):
        return super(AdminFlashDealCreateAPIView, self).post(request, *args, **kwargs)
