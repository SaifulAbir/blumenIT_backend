from datetime import datetime
from django.db.models import Q
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from product.pagination import ProductCustomPagination
from product.serializers import DiscountTypeSerializer, ProductTagsSerializer, TagsSerializer, VariantTypeSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView,DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from product.models import Brand, Category, DiscountTypes, Product, ProductAttributes, ProductMedia, ProductReview, ProductTags, ProductVideoProvider, SubCategory, SubSubCategory, Tags, Units, VariantType, VatType
from user.models import CustomerProfile, User
from vendor.models import VendorRequest, Vendor,Seller
from vendor.serializers import ProductVatProviderSerializer, ProductVideoProviderSerializer, VendorBrandSerializer, VendorCategorySerializer, VendorProductCreateSerializer, VendorProductDetailsSerializer, VendorProductListSerializer, VendorProductUpdateSerializer, VendorRequestSerializer, VendorCreateSerializer, OrganizationNameSerializer, \
    VendorDetailSerializer, StoreSettingsSerializer,SellerDetailSerializer , VendorSubCategorySerializer, VendorSubSubCategorySerializer, VendorUnitSerializer, SellerSerializer, ProductAttributesSerializer, CouponSerializer
from user.models import User
from cart.models import Coupon
from rest_framework.exceptions import ValidationError


class SellerCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SellerSerializer


    def post(self, request):
        seller = SellerSerializer(data=request.data)

        # validating for already existing data
        if Seller.objects.filter(**request.data).exists():
            raise serializers.ValidationError('This data already exists')

        if seller.is_valid():
            seller.save()
            return (Response(seller.data))
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class SellerListAPIView(ListAPIView):

        queryset = Seller.objects.filter()
        permission_classes = [AllowAny]
        serializer_class = SellerDetailSerializer


class SellerUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SellerSerializer
    queryset = Seller.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def put(self, request, *args, **kwargs):
        return super(SellerUpdateAPIView, self).put(request, *args, **kwargs)

class SellerDeleteAPIView(DestroyAPIView):
    serializer_class = SellerSerializer
    queryset = Seller.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def delete(self, request, *args, **kwargs):
        return super(SellerDeleteAPIView, self).delete(request, *args, **kwargs)

class CouponCreateAPIView(CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = CouponSerializer

    def post(self, request):
        coupon = CouponSerializer(data=request.data)

        # validating for already existing data
        if Coupon.objects.filter(**request.data).exists():
            raise serializers.ValidationError('This data already exists')

        if coupon.is_valid():
            coupon.save()
            return (Response(coupon.data))
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



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
    permission_classes = (AllowAny,)
    serializer_class = VendorProductCreateSerializer
    # permission_classes = [IsAuthenticated]

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