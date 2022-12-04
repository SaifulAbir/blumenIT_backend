from datetime import datetime
from django.db.models import Q
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from product.pagination import ProductCustomPagination
from product.serializers import DiscountTypeSerializer, ProductTagsSerializer, TagsSerializer, VariantTypeSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from product.models import Brand, Category, DiscountTypes, Product, ProductAttributes, ProductReview, ProductTags, SubCategory, SubSubCategory, Tags, Units, VariantType, ProductVideoProvider, VatType, FilterAttributes
from user.models import CustomerProfile, User
from vendor.models import VendorRequest, Vendor, Seller
from vendor.serializers import AddNewSubCategorySerializer, AddNewSubSubCategorySerializer,\
    VendorBrandSerializer, AdminCategoryListSerializer, VendorProductListSerializer,\
    ProductUpdateSerializer, VendorProductViewSerializer, \
    SellerDetailSerializer, AdminSubCategoryListSerializer, \
    AdminSubSubCategoryListSerializer, VendorUnitSerializer, SellerSerializer, ProductAttributesSerializer, \
    ProductVideoProviderSerializer, ProductVatProviderSerializer, UpdateCategorySerializer,\
    UpdateSubSubCategorySerializer, ProductCreateSerializer, AddNewCategorySerializer, \
    SellerCreateSerializer, FlashDealCreateSerializer, UpdateSubCategorySerializer, FilteringAttributesSerializer, AdminProfileSerializer
from user.models import User
from cart.models import Coupon
from rest_framework.exceptions import ValidationError


class AdminSellerCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SellerCreateSerializer

    def post(self, request, *args, **kwargs):
        return super(AdminSellerCreateAPIView, self).post(request, *args, **kwargs)


class AdminSellerDetailsAPIView(RetrieveAPIView):
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


class AdminSellerListAPIView(ListAPIView):
    queryset = Seller.objects.filter(is_active=True)
    permission_classes = [AllowAny]
    serializer_class = SellerSerializer


class AdminSellerUpdateAPIView(RetrieveUpdateAPIView):
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


class AdminSellerDeleteAPIView(ListAPIView):
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
    permission_classes = [IsAuthenticated]
    serializer_class = ProductCreateSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True:
            return super(AdminProductCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create product, because you are not a Admin!'})

class AdminProductUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductUpdateSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs['slug']
        if self.request.user.is_superuser == True:
            query = Product.objects.filter(slug=slug)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Product does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not update this product, because you are not a Admin!'})

class AdminFilterAttributesAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FilteringAttributesSerializer
    def get_queryset(self):
        id = self.kwargs['id']
        type = self.kwargs['type']
        if id and type:
            if type == 'category':
                queryset = FilterAttributes.objects.filter(Q(category__id=id) & Q(is_active=True)).order_by('-created_at')
            if type == 'sub_category':
                queryset = FilterAttributes.objects.filter(Q(sub_category__id=id) & Q(is_active=True)).order_by('-created_at')
            if type == 'sub_sub_category':
                queryset = FilterAttributes.objects.filter(Q(sub_sub_category__id=id) & Q(is_active=True)).order_by('-created_at')

        if queryset:
            return queryset
        else:
            raise ValidationError({"msg": 'Filter Attributes not found!'})

class AdminCategoryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.filter(is_active=True)
    serializer_class = AdminCategoryListSerializer

class AdminAddNewCategoryAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddNewCategorySerializer

    def post(self, request, *args, **kwargs):
        return super(AdminAddNewCategoryAPIView, self).post(request, *args, **kwargs)

class AdminUpdateCategoryAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateCategorySerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        query = Category.objects.filter(id=id)
        if query:
            return query
        else:
            raise ValidationError(
                {"msg": 'Category does not found!'})

class AdminDeleteCategoryAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCategoryListSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        category_obj_exist = Category.objects.filter(id=id).exists()
        if category_obj_exist:
            category_obj = Category.objects.filter(id=id)
            category_obj.update(is_active=False)
            queryset = Category.objects.filter(is_active=True).order_by('-created_at')
            return queryset
        else:
            raise ValidationError(
                {"msg": 'Category Does not exist!'})

class AdminSubCategoryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSubCategoryListSerializer
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
    permission_classes = [IsAuthenticated]
    serializer_class = AddNewSubCategorySerializer

    def post(self, request, *args, **kwargs):
        return super(AdminAddNewSubCategoryAPIView, self).post(request, *args, **kwargs)

class AdminUpdateSubCategoryAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateSubCategorySerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        query = SubCategory.objects.filter(id=id)
        if query:
            return query
        else:
            raise ValidationError(
                {"msg": 'Sub Category does not found!'})

class AdminDeleteSubCategoryAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSubCategoryListSerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        sub_category_obj_exist = SubCategory.objects.filter(
            id=id).exists()
        if sub_category_obj_exist:
            sub_category_obj = SubCategory.objects.filter(id=id)
            sub_category_obj.update(is_active=False)

            queryset = SubCategory.objects.filter(is_active=True).order_by('-created_at')
            return queryset
        else:
            raise ValidationError(
                {"msg": 'Sub Category Does not exist!'})

class AdminSubSubCategoryListAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AdminSubSubCategoryListSerializer
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
    permission_classes = [IsAuthenticated]
    serializer_class = AddNewSubSubCategorySerializer

    def post(self, request, *args, **kwargs):
        return super(AdminAddNewSubSubCategoryAPIView, self).post(request, *args, **kwargs)

class AdminUpdateSubSubCategoryAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateSubSubCategorySerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        query = SubSubCategory.objects.filter(id=id)
        if query:
            return query
        else:
            raise ValidationError(
                {"msg": 'Sub Sub Category does not found!'})

class AdminDeleteSubSubCategoryAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSubSubCategoryListSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        sub_sub_category_obj_exist = SubSubCategory.objects.filter(id=id).exists()
        if sub_sub_category_obj_exist:
            sub_sub_category_obj = SubSubCategory.objects.filter(id=id)
            sub_sub_category_obj.update(is_active=False)

            queryset = SubSubCategory.objects.filter(is_active=True).order_by('-created_at')
            return queryset
        else:
            raise ValidationError(
                {"msg": 'Sub Sub Category Does not exist!'})

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
    permission_classes = [IsAuthenticated]
    serializer_class = VendorProductListSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            queryset = Product.objects.filter(status='PUBLISH').order_by('-created_at')
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "Product doesn't exist! " })
        else:
            raise ValidationError(
                {"msg": 'You can not show product list, because you are not a Admin!'})

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
    permission_classes = [IsAuthenticated]
    serializer_class = VendorProductListSerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs['slug']
        if self.request.user.is_superuser == True:
            product_obj_exist = Product.objects.filter(
                slug=slug).exists()
            if product_obj_exist:
                product_obj = Product.objects.filter(slug=slug)
                product_obj.update(status='UNPUBLISH')

                queryset = Product.objects.filter(status='PUBLISH').order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Product Does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not delete this product, because you are not a Admin!'})

class AdminVideoProviderListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = ProductVideoProvider.objects.filter(is_active=True)
    serializer_class = ProductVideoProviderSerializer

class AdminVatTypeListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = VatType.objects.filter(is_active=True)
    serializer_class = ProductVatProviderSerializer

class AdminFlashDealCreateAPIView(CreateAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = (AllowAny,)
    serializer_class = FlashDealCreateSerializer


    def post(self, request, *args, **kwargs):
        return super(AdminFlashDealCreateAPIView, self).post(request, *args, **kwargs)

class AdminProfileAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminProfileSerializer

    def get_object(self):
        if self.request.user.is_superuser == True:
            query = User.objects.get(id=self.request.user.id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'User does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not view your profile, because you are not a Admin!'})
