from datetime import datetime

from django.db.models.functions import Concat, text, Coalesce
from django.db.models import Q, Count, Value, F, CharField, Prefetch, Subquery, Max, Min, ExpressionWrapper, \
    IntegerField, Sum, DecimalField
from ecommerce.settings import MEDIA_URL
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.views import APIView

from home.models import ProductView
from product.serializers import ProductCreateSerializer, ProductUpdateSerializer, ProductListSerializer, TagCreateSerializer,ProductTagsSerializer,  TagListSerializer, ProductCategoryListSerializer, ProductBrandListSerializer, ProductSubCategoryListSerializer, ProductDetailsSerializer, ProductSearchSerializer, ProductAllCategoryListSerializer

from product.models import Product, Tags, ProductTags, ProductCategory, ProductSubCategory, ProductChildCategory, ProductBrand

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from product.pagination import ProductCustomPagination
from itertools import chain



# create API views start
from user.models import CustomerProfile


class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductCreateSerializer

    def post(self, request, *args, **kwargs):
        return super(ProductCreateAPIView, self).post(request, *args, **kwargs)

class TagCreateAPIView(CreateAPIView):
    serializer_class = TagCreateSerializer
    queryset = Tags.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if self.request.data =={}:
            raise ValidationError({"name":'this field may not be null'
            })
        else:
            tag_name = self.request.data['name'].upper()
            tags = Tags.objects.filter(name = tag_name)
            # print(tags)
            if not tags.exists():
                obj = Tags()
                obj.name = tag_name
                obj.is_active = True
                obj.created_by = self.request.user.id
                obj.save()
                return Response({"id":self.request.user.id,"name":tag_name}, status=status.HTTP_200_OK)
            else:
                raise ValidationError({"name": str(tag_name)+' Tag name already exist.'})
# create API views end

# list API views start
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
            queryset = Product.objects.filter(product_category=cid, status='ACTIVE').order_by('-created_at')
        else:
            queryset = Product.objects.filter(status='ACTIVE').order_by('-created_at')
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
            queryset = Product.objects.filter(product_sub_category=subcid, status='ACTIVE').order_by('-created_at')
        else:
            queryset = Product.objects.filter(status='ACTIVE').order_by('-created_at')
        return queryset

class ProductListByChildCategoryAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListSerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'childcid'
    lookup_url_kwarg = "childcid"
    def get_queryset(self):
        childcid = self.kwargs['childcid']
        if childcid:
            queryset = Product.objects.filter(product_child_category=childcid, status='ACTIVE').order_by('-created_at')
        else:
            queryset = Product.objects.filter(status='ACTIVE').order_by('-created_at')
        return queryset


class ProductTagsListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = ProductTags.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ProductTagsSerializer

class TagsListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Tags.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = TagListSerializer

class ProductAllCategoryListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductAllCategoryListSerializer
    def get_queryset(self):
        query = ProductCategory.objects.filter(is_active=True).order_by('-created_at')
        return query

class ProductCategoryListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = ProductCategory.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ProductCategoryListSerializer

class ProductSubCategoryListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductSubCategoryListSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"
    def get_queryset(self):
        slug = self.kwargs['slug']
        if slug == 'all':
            queryset = ProductSubCategory.objects.filter(is_active=True).order_by('-created_at')
        else:
            queryset = ProductSubCategory.objects.filter(category=slug).order_by('-created_at')
        return queryset

class ProductBrandListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = ProductBrand.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ProductBrandListSerializer


class ProductDetailsAPI(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductDetailsSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"
    def get_object(self):
        slug = self.kwargs['slug']
        query = Product.objects.get(slug=slug)
        if self.request.user.is_authenticated:
            try:
                product_view = ProductView.objects.get(user=self.request.user, product=query)
                product_view.view_date = datetime.now()
                product_view.view_count += 1
                product_view.save()
            except ProductView.DoesNotExist:
                customer = CustomerProfile.objects.get(user=self.request.user)
                ProductView.objects.create(user=self.request.user, product=query, customer=customer, view_date=datetime.now())
        return query

class ProductSearchAPIView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        query = request.GET.get('query')
        if query:
            # products = Product.objects.filter(title__icontains=query).annotate(img=Concat(Value(MEDIA_URL), 'thumbnail', output_field=CharField())).values("title", "img", uid=F("slug")).annotate(type = Value("PRODUCT"))
            products = Product.objects.filter(Q(title__icontains=query) | Q(price__icontains = query) | Q(product_category__name__icontains = query) | Q(product_brand__name__icontains = query) | Q(vendor__organization_name__icontains = query)).annotate(img=Concat(Value(MEDIA_URL), 'thumbnail', output_field=CharField()))
            search_result = list(products)
        else:
            search_result = []
        serializer = ProductSearchSerializer(search_result, many=True)
        return Response({"search_result": serializer.data})
# list API views end


# update API views start
class ProductUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ProductUpdateSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs['slug']
        query = Product.objects.filter(slug=slug)
        return query

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
# update API views end

