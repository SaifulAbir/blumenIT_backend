from datetime import datetime
from django.db.models import Q
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from product.pagination import ProductCustomPagination
from product.serializers import DiscountTypeSerializer, ProductTagsSerializer, TagsSerializer, VariantTypeSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from product.models import Brand, Category, DiscountTypes, Product, ProductAttributes, ProductMedia, ProductReview, ProductTags, SubCategory, SubSubCategory, Tags, Units, VariantType, ProductVideoProvider, VatType
from user.models import CustomerProfile, User
from vendor.models import VendorRequest, Vendor, Seller
from vendor.serializers import VendorAddNewCategorySerializer, VendorAddNewSubCategorySerializer, VendorAddNewSubSubCategorySerializer, VendorBrandSerializer, VendorCategorySerializer, VendorProductCreateSerializer, VendorProductDetailsSerializer, VendorProductListSerializer, VendorProductUpdateSerializer, VendorProductViewSerializer, VendorRequestSerializer, VendorCreateSerializer, OrganizationNameSerializer, \
    VendorDetailSerializer, StoreSettingsSerializer, SellerCreateSerializer, VendorSubCategorySerializer, VendorSubSubCategorySerializer, VendorUnitSerializer, SellerSerializer, ProductAttributesSerializer, ProductVideoProviderSerializer, ProductVatProviderSerializer, VendorUpdateCategorySerializer, VendorUpdateSubSubCategorySerializer
from user.models import User
from cart.models import Coupon
from rest_framework.exceptions import ValidationError


class SellerCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SellerCreateSerializer

    def post(self, request, *args, **kwargs):
        return super(SellerCreateAPIView, self).post(request, *args, **kwargs)


class SellerListAPIView(ListAPIView):
    queryset = Seller.objects.filter()
    permission_classes = [AllowAny]
    serializer_class = SellerSerializer


class SellerUpdateAPIView(RetrieveUpdateAPIView):
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


class SellerDeleteAPIView(DestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = SellerSerializer
    queryset = Seller.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    # def get_queryset(self):
    #     s_id = self.kwargs['id']
    #     seller_obj = Seller.objects.filter(id=s_id)

    def get_queryset(self):
        seller_id = self.kwargs['id']
        seller_obj = Seller.objects.filter(id=seller_id).exists()
        if seller_obj:
            seller_obj = Product.objects.filter(id=seller_id)
            seller_obj.update(status='REMOVE', is_active=False)

            queryset = Seller.objects.filter(status='ACTIVE').order_by('-created_at')
            return queryset
        else:
            raise ValidationError(
                {"msg": 'Product Does not exist!'})

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

class VendorProductListAPI(ListAPIView):
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

    # def get_queryset(self):
    #     if Vendor.objects.filter(vendor_admin=User.objects.get(id=self.request.user.id)).exists():
    #         vid = Vendor.objects.get(
    #             vendor_admin=User.objects.get(id=self.request.user.id))
    #         if vid:
    #             queryset = Product.objects.filter(
    #                 vendor=vid, status='ACTIVE').order_by('-created_at')
    #             return queryset
    #     else:
    #         raise ValidationError({"msg": 'You are not a vendor.'})


class VendorProductCreateAPIView(CreateAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = (AllowAny,)
    serializer_class = VendorProductCreateSerializer


    def post(self, request, *args, **kwargs):
        return super(VendorProductCreateAPIView, self).post(request, *args, **kwargs)

class VendorProductUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    serializer_class = VendorProductUpdateSerializer
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

    # def get_queryset(self):
    #     slug = self.kwargs['slug']
    #     # query = Product.objects.filter(slug=slug)
    #     # return query

    #     if Vendor.objects.filter(vendor_admin=User.objects.get(id=self.request.user.id)).exists():
    #         vid = Vendor.objects.get(
    #             vendor_admin=User.objects.get(id=self.request.user.id))
    #         if vid:
    #             try:
    #                 query = Product.objects.filter(slug=slug, vendor=vid)
    #                 if query:
    #                     return query
    #                 else:
    #                     raise ValidationError(
    #                         {"msg": 'You are not creator of this product!'})
    #             except:
    #                 raise ValidationError(
    #                     {"msg": "Product doesn't exist or You are not the creator of this product!"})
    #     else:
    #         raise ValidationError({"msg": 'You are not a vendor.'})

class VendorProductViewAPI(RetrieveAPIView):
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

class VendorProductDetailsAPI(RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = VendorProductDetailsSerializer
    lookup_field = 'slugi'
    lookup_url_kwarg = "slugi"

    def get_object(self):
        slug = self.kwargs['slugi']
        query = Product.objects.get(slug=slug)
        if query:
            return query
        else:
            raise ValidationError(
                {"msg": 'You are not creator of this product!'})

    # def get_object(self):
    #     slug = self.kwargs['slugi']
    #     if Vendor.objects.filter(vendor_admin=User.objects.get(id=self.request.user.id)).exists():
    #         vid = Vendor.objects.get(
    #             vendor_admin=User.objects.get(id=self.request.user.id))
    #         if vid:
    #             try:
    #                 query = Product.objects.get(slug=slug, vendor=vid)
    #                 if query:
    #                     return query
    #                 else:
    #                     raise ValidationError(
    #                         {"msg": 'You are not creator of this product!'})
    #             except:
    #                 raise ValidationError(
    #                     {"msg": "Product doesn't exist or You are not the creator of this product!"})
    #     else:
    #         raise ValidationError({"msg": 'You are not a vendor.'})

    # def get_object(self):
    #     slug = self.kwargs['slugi']
    #     if Vendor.objects.filter(vendor_admin=User.objects.get(id=self.request.user.id)).exists():
    #         vid = Vendor.objects.get(
    #             vendor_admin=User.objects.get(id=self.request.user.id))
    #         if vid:
    #             try:
    #                 query = Product.objects.get(slug=slug, vendor=vid)
    #                 if query:
    #                     return query
    #                 else:
    #                     raise ValidationError(
    #                         {"msg": 'You are not creator of this product!'})
    #             except:
    #                 raise ValidationError(
    #                     {"msg": "Product doesn't exist or You are not the creator of this product!"})
    #     else:
    #         raise ValidationError({"msg": 'You are not a vendor.'})


class VendorProductSingleMediaDeleteAPI(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorProductUpdateSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs['slug']
        mid = self.kwargs['mid']

        if Vendor.objects.filter(vendor_admin=User.objects.get(id=self.request.user.id)).exists():
            vid = Vendor.objects.get(
                vendor_admin=User.objects.get(id=self.request.user.id))
            if vid:
                # try:
                query_exist = Product.objects.filter(
                    slug=slug, vendor=vid).exists()
                if query_exist:
                    query = Product.objects.filter(slug=slug, vendor=vid)
                    media_obj = ProductMedia.objects.filter(
                        id=int(mid), product=query[0].id).exists()
                    if media_obj:
                        media_obj_obj = ProductMedia.objects.filter(
                            id=int(mid), product=query[0].id)
                        media_obj_obj.update(is_active=False)
                        return query
                    else:
                        raise ValidationError(
                            {"msg": "Media doesn't found"})
                else:
                    raise ValidationError(
                        {"msg": 'You are not creator of this product!'})
                # except:
                # raise ValidationError(
                # {"msg": "Product doesn't exist or You are not the creator of this product!"})
        else:
            raise ValidationError({"msg": 'You are not a vendor.'})


class VendorProductDeleteAPI(ListAPIView):
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
            product_obj.update(status='REMOVE', is_published=False)

            queryset = Product.objects.filter(status='ACTIVE').order_by('-created_at')
            return queryset
        else:
            raise ValidationError(
                {"msg": 'Product Does not exist!'})

    # def get_queryset(self):
    #     slug = self.kwargs['slug']
    #     if Vendor.objects.filter(vendor_admin=User.objects.get(id=self.request.user.id)).exists():
    #         vid = Vendor.objects.get(
    #             vendor_admin=User.objects.get(id=self.request.user.id))
    #         if vid:
    #             product_obj_exist = Product.objects.filter(
    #                 slug=slug, vendor=vid).exists()
    #             if product_obj_exist:
    #                 product_obj = Product.objects.filter(slug=slug, vendor=vid)
    #                 product_obj.update(status='REMOVE')

    #                 queryset = Product.objects.filter(
    #                     vendor=vid, status='ACTIVE').order_by('-created_at')
    #                 return queryset
    #             else:
    #                 raise ValidationError(
    #                     {"msg": 'You are not creator of this product!'})
    #     else:
    #         raise ValidationError({"msg": 'You are not a vendor.'})

class VendorVideoProviderListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = ProductVideoProvider.objects.filter(is_active=True)
    serializer_class = ProductVideoProviderSerializer

class VendorVatTypeListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = VatType.objects.filter(is_active=True)
    serializer_class = ProductVatProviderSerializer



class VendorCategoryListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.filter(is_active=True)
    serializer_class = VendorCategorySerializer

class VendorAddNewCategoryAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VendorAddNewCategorySerializer

    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return super(VendorAddNewCategoryAPIView, self).post(request, *args, **kwargs)

class VendorUpdateCategoryAPIView(RetrieveUpdateAPIView):
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

class VendorDeleteCategoryAPIView(ListAPIView):
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

class VendorAddNewSubCategoryAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VendorAddNewSubCategorySerializer

    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return super(VendorAddNewSubCategoryAPIView, self).post(request, *args, **kwargs)

class VendorUpdateSubCategoryAPIView(RetrieveUpdateAPIView):
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

class VendorDeleteSubCategoryAPIView(ListAPIView):
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

class VendorAddNewSubSubCategoryAPIView(CreateAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = (AllowAny,)
    serializer_class = VendorAddNewSubSubCategorySerializer


    def post(self, request, *args, **kwargs):
        return super(VendorAddNewSubSubCategoryAPIView, self).post(request, *args, **kwargs)

class VendorUpdateSubSubCategoryAPIView(RetrieveUpdateAPIView):
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

class VendorDeleteSubSubCategoryAPIView(ListAPIView):
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
