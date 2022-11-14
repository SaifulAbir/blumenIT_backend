from datetime import datetime
from django.db.models.functions import Concat, text, Coalesce
from django.db.models import Q, Count, Value, F, CharField, Prefetch, Subquery, Max, Min, ExpressionWrapper, \
    IntegerField, Sum, DecimalField
from ecommerce.settings import MEDIA_URL
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.views import APIView
from home.models import ProductView
from product import serializers
from product.serializers import StoreProductDetailsSerializer, \
    ProductDetailsSerializer, ProductListSerializer, ProductReviewCreateSerializer, BrandSerializer,\
    StoreCategoryAPIViewListSerializer
from product.models import Category, Product, Brand
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from product.pagination import ProductCustomPagination
from itertools import chain
from user.models import CustomerProfile, User
from vendor.models import Vendor


class BrandCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = BrandSerializer

    def post(self, request):
        brand = BrandSerializer(data=request.data)

        if Brand.objects.filter(**request.data).exists():
            raise serializers.ValidationError('This data already exists')

        if brand.is_valid():
            brand.save()
            return Response(brand.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class StoreCategoryListAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = StoreCategoryAPIViewListSerializer

    def get_queryset(self):
        queryset = Category.objects.filter(is_active=True)
        return queryset


class ProductDetailsAPI(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductDetailsSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"

    def get_object(self):
        slug = self.kwargs['slug']
        try:
            query = Product.objects.get(slug=slug)
            if self.request.user.is_authenticated:
                try:
                    product_view = ProductView.objects.get(
                        user=self.request.user, product=query)
                    product_view.view_date = datetime.now()
                    product_view.view_count += 1
                    product_view.save()
                except ProductView.DoesNotExist:
                    customer = CustomerProfile.objects.get(
                        user=self.request.user)
                    ProductView.objects.create(
                        user=self.request.user, product=query, customer=customer, view_date=datetime.now())
            return query
        except:
            raise ValidationError({"details": "Product doesn't exist!"})


class ProductListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.filter(status='ACTIVE').order_by('-created_at')
    serializer_class = ProductListSerializer
    pagination_class = ProductCustomPagination


class ProductListByCategoryAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListSerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'cid'
    lookup_url_kwarg = "cid"

    def get_queryset(self):
        cid = self.kwargs['cid']
        if cid:
            queryset = Product.objects.filter(
                category=cid, status='ACTIVE').order_by('-created_at')
        else:
            queryset = Product.objects.filter(
                status='ACTIVE').order_by('-created_at')
        return queryset


class ProductListBySubCategoryAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListSerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'subcid'
    lookup_url_kwarg = "subcid"

    def get_queryset(self):
        subcid = self.kwargs['subcid']
        if subcid:
            queryset = Product.objects.filter(
                sub_category=subcid, status='ACTIVE').order_by('-created_at')
        else:
            queryset = Product.objects.filter(
                status='ACTIVE').order_by('-created_at')
        return queryset


class ProductListBySubSubCategoryAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListSerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'subsubcid'
    lookup_url_kwarg = "subsubcid"

    def get_queryset(self):
        subsubcid = self.kwargs['subsubcid']
        if subsubcid:
            queryset = Product.objects.filter(
                sub_sub_category=subsubcid, status='ACTIVE').order_by('-created_at')
        else:
            queryset = Product.objects.filter(
                status='ACTIVE').order_by('-created_at')
        return queryset


class ProductSearchAPI(ListAPIView):
    permission_classes = ()
    pagination_class = ProductCustomPagination
    serializer_class = ProductListSerializer

    def get_queryset(self):
        request = self.request
        query = request.GET.get('query')
        category = request.GET.get('category_id')

        queryset = Product.objects.filter(
            status='ACTIVE').order_by('-created_at')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(full_description__icontains=query) |
                Q(short_description__icontains=query) |
                Q(sku__icontains=query)
            )

        if category:
            queryset = queryset.filter(category__id=category)

        return queryset


class ProductReviewCreateAPIView(CreateAPIView):
    # permission_classes = (AllowAny,)
    permission_classes = [IsAuthenticated]
    serializer_class = ProductReviewCreateSerializer

    def post(self, request, *args, **kwargs):
        return super(ProductReviewCreateAPIView, self).post(request, *args, **kwargs)
        # if User.objects.filter(id=self.request.user.id).exists():
        #     uid = User.objects.get(id=self.request.user.id)
        #     if uid:
        #         return super(ProductReviewCreateAPIView, self).post(request, *args, **kwargs)
        # else:
        #     raise ValidationError({"msg": 'You are not a User.'})
        # return super(ProductReviewCreateAPIView, self).post(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     return super(ProductReviewCreateAPIView, self).post(request, *args, **kwargs)


class VendorProductListForFrondEndAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListSerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'vid'
    lookup_url_kwarg = "vid"

    def get_queryset(self):
        vid = self.kwargs['vid']
        if vid:
            try:
                vendor = Vendor.objects.get(id=vid)
                queryset = Product.objects.filter(
                    vendor=vendor, status='ACTIVE').order_by('-created_at')
            except:
                raise ValidationError({"details": "Vendor Not Valid.!"})
        else:
            queryset = Product.objects.filter(
                status='ACTIVE').order_by('-created_at')
        return queryset


class StoreProductDetailsAPI(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = StoreProductDetailsSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"

    def get_object(self):
        slug = self.kwargs['slug']
        try:
            query = Product.objects.get(slug=slug)
            return query
        except:
            raise ValidationError({"details": "Product doesn't exist!"})
