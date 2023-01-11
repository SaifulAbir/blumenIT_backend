from datetime import datetime
from django.db.models import Q, Count
from ecommerce.settings import MEDIA_URL
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from home.models import ProductView
from product.serializers import ProductDetailsSerializer, ProductReviewCreateSerializer, \
StoreCategoryAPIViewListSerializer, ProductListBySerializer, FilterAttributeSerializer, PcBuilderCategoryListSerializer, PcBuilderSubCategoryListSerializer, PcBuilderSubSubCategoryListSerializer, BrandListSerializer

from product.models import Category, SubCategory, SubSubCategory, Product, Brand, AttributeValues
from product.models import FilterAttributes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from product.pagination import ProductCustomPagination
from itertools import chain
from user.models import CustomerProfile, User
from vendor.models import Vendor


class StoreCategoryListAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = StoreCategoryAPIViewListSerializer

    def get_queryset(self):
        queryset = Category.objects.filter(is_active=True).order_by('ordering_number')
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
    serializer_class = ProductListBySerializer
    pagination_class = ProductCustomPagination


class ProductListByCategoryAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListBySerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'cid'
    lookup_url_kwarg = "cid"

    def get_queryset(self):
        # work with dynamic pagination page_size
        try:
            pagination = self.kwargs['pagination']
        except:
            pagination = 10
        self.pagination_class.page_size = pagination


        cid = self.kwargs['cid']
        if cid:
            queryset = Product.objects.filter(category=cid, status='PUBLISH').order_by('-created_at')
        else:
            queryset = Product.objects.filter(status='PUBLISH').order_by('-created_at')

        # filtering start
        request = self.request
        filter_price = request.GET.get('filter_price')
        attr_value_ids = request.GET.get('attr_value_ids')

        if filter_price:
            price_list = []
            filter_prices = filter_price.split("-")
            for filter_price in filter_prices:
                price_list.append(int(filter_price))

            min_price = price_list[0]
            max_price = price_list[1]
            queryset = queryset.filter(price__range=(min_price, max_price)).order_by('-created_at')

        # if attr_value_ids:
        #     attr_value_ids_list = attr_value_ids.split(",")
        #     for attr_value_id in attr_value_ids_list:
        #         attr_value_id = int(attr_value_id)
        #         queryset = queryset.filter(Q(product_filter_attributes_product__attribute_value__id=attr_value_id)).order_by('-created_at')

                # attr_id = AttributeValues.objects.get(id = attr_value_id).attribute
                # f_att_id = FilterAttributes.objects.get(attribute = attr_id)
                # p_f_att_id = ProductFilterAttributes.objects.get(filter_attribute = f_att_id)
                # queryset = queryset.filter(id=p_f_att_id.product.id).order_by('-created_at')

                # attr_value_id = int(attr_value_id)
                # attr_id = AttributeValues.objects.get(id = attr_value_id).attribute
                # cat_id = FilterAttributes.objects.get(attribute = attr_id).category.id
                # queryset = queryset.filter(Q(category__id=cat_id)).order_by('-created_at')

        new_attr_value_ids = []
        if attr_value_ids:
            attr_value_ids_list = attr_value_ids.split(",")
            for attr_value_id in attr_value_ids_list:
                attr_value_id = int(attr_value_id)
                new_attr_value_ids.append(attr_value_id)

        if new_attr_value_ids:
            queryset = queryset.filter(Q(product_filter_attributes_product__attribute_value__id__in = new_attr_value_ids)).order_by('-id').distinct("id")

        return queryset


class ProductListByCategoryPopularProductsAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListBySerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        # work with dynamic pagination page_size
        try:
            pagination = self.kwargs['pagination']
        except:
            pagination = 10
        self.pagination_class.page_size = pagination

        id = self.kwargs['id']
        type = self.kwargs['type']

        queryset = Product.objects.filter(status='PUBLISH').annotate(count=Count('product_review_product')).order_by('-count')

        if id and type:
            if type == 'category':
                queryset = queryset.filter(Q(category=id))

            if type == 'sub_category':
                queryset = queryset.filter(Q(sub_category=id))

            if type == 'sub_sub_category':
                queryset = queryset.filter(Q(sub_sub_category=id))

        else:
            queryset = Product.objects.filter(status='PUBLISH').annotate(count=Count('product_review_product')).order_by('-count')



        return queryset


class FilterAttributesAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FilterAttributeSerializer

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


class ProductListBySubCategoryAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListBySerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'subcid'
    lookup_url_kwarg = "subcid"

    def get_queryset(self):
        # work with dynamic pagination page_size
        try:
            pagination = self.kwargs['pagination']
        except:
            pagination = 10
        self.pagination_class.page_size = pagination


        subcid = self.kwargs['subcid']
        if subcid:
            queryset = Product.objects.filter(
                sub_category=subcid, status='PUBLISH').order_by('-created_at')
        else:
            queryset = Product.objects.filter(
                status='PUBLISH').order_by('-created_at')

        # filtering start
        request = self.request
        filter_price = request.GET.get('filter_price')
        attr_value_ids = request.GET.get('attr_value_ids')

        if filter_price:
            price_list = []
            filter_prices = filter_price.split("-")
            for filter_price in filter_prices:
                price_list.append(int(filter_price))

            min_price = price_list[0]
            max_price = price_list[1]
            queryset = queryset.filter(price__range=(min_price, max_price)).order_by('-created_at')

        new_attr_value_ids = []
        if attr_value_ids:
            attr_value_ids_list = attr_value_ids.split(",")
            for attr_value_id in attr_value_ids_list:
                attr_value_id = int(attr_value_id)
                new_attr_value_ids.append(attr_value_id)

        if new_attr_value_ids:
            queryset = queryset.filter(Q(product_filter_attributes_product__attribute_value__id__in = new_attr_value_ids)).order_by('-id').distinct("id")

        return queryset


class ProductListBySubSubCategoryAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListBySerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'subsubcid'
    lookup_url_kwarg = "subsubcid"

    def get_queryset(self):
        # work with dynamic pagination page_size
        try:
            pagination = self.kwargs['pagination']
        except:
            pagination = 10
        self.pagination_class.page_size = pagination


        subsubcid = self.kwargs['subsubcid']
        if subsubcid:
            queryset = Product.objects.filter(
                sub_sub_category=subsubcid, status='PUBLISH').order_by('-created_at')
        else:
            queryset = Product.objects.filter(
                status='PUBLISH').order_by('-created_at')

        # filtering start
        request = self.request
        filter_price = request.GET.get('filter_price')
        attr_value_ids = request.GET.get('attr_value_ids')

        if filter_price:
            price_list = []
            filter_prices = filter_price.split("-")
            for filter_price in filter_prices:
                price_list.append(int(filter_price))

            min_price = price_list[0]
            max_price = price_list[1]
            queryset = queryset.filter(price__range=(min_price, max_price)).order_by('-created_at')

        new_attr_value_ids = []
        if attr_value_ids:
            attr_value_ids_list = attr_value_ids.split(",")
            for attr_value_id in attr_value_ids_list:
                attr_value_id = int(attr_value_id)
                new_attr_value_ids.append(attr_value_id)

        if new_attr_value_ids:
            queryset = queryset.filter(Q(product_filter_attributes_product__attribute_value__id__in = new_attr_value_ids)).order_by('-id').distinct("id")

        return queryset


class ProductSearchAPI(ListAPIView):
    permission_classes = ()
    pagination_class = ProductCustomPagination
    serializer_class = ProductListBySerializer

    def get_queryset(self):
        request = self.request
        query = request.GET.get('search')
        category = request.GET.get('category_id')

        queryset = Product.objects.filter(
            status='PUBLISH').order_by('-created_at')

        if query:
            queryset = queryset.filter(Q(title__icontains=query))

        if category:
            queryset = queryset.filter(category__id=category)

        return queryset


class ProductReviewCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductReviewCreateSerializer

    def post(self, request, *args, **kwargs):
        # return super(ProductReviewCreateAPIView, self).post(request, *args, **kwargs)
        if User.objects.filter(id=self.request.user.id).exists():
            uid = User.objects.get(id=self.request.user.id)
            if uid:
                return super(ProductReviewCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError({"msg": 'You are not a User.'})


class VendorProductListForFrondEndAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListBySerializer
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


class PcBuilderChooseAPIView(ListAPIView):
    permission_classes = (AllowAny,) 
    serializer_class = ProductListBySerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        request = self.request
        component_id = request.GET.get('component_id')
        type = request.GET.get('type')
        filter_price = request.GET.get('filter_price')
        attr_value_ids = request.GET.get('attr_value_ids')

        queryset = Product.objects.filter(
            status='PUBLISH').order_by('-created_at')

        if component_id and type:
            if type == 'category':
                queryset = queryset.filter(Q(category__id=component_id)).order_by('-created_at')
            if type == 'sub_category':
                queryset = queryset.filter(Q(sub_category__id=component_id)).order_by('-created_at')
            if type == 'sub_sub_category':
                queryset = queryset.filter(Q(sub_sub_category__id=component_id)).order_by('-created_at')

        if filter_price:
            price_list = []
            filter_prices = filter_price.split("-")
            for filter_price in filter_prices:
                price_list.append(int(filter_price))

            min_price = price_list[0]
            max_price = price_list[1]
            queryset = queryset.filter(price__range=(min_price, max_price)).order_by('-created_at')

        # if attr_value_ids:
        #     attr_value_ids_list = attr_value_ids.split(",")
        #     for attr_value_id in attr_value_ids_list:
        #         attr_value_id = int(attr_value_id)
        #         queryset = queryset.filter(Q(product_filter_attributes_product__attribute_value__id=attr_value_id)).order_by('-created_at')

        new_attr_value_ids = []
        if attr_value_ids:
            attr_value_ids_list = attr_value_ids.split(",")
            for attr_value_id in attr_value_ids_list:
                attr_value_id = int(attr_value_id)
                new_attr_value_ids.append(attr_value_id)

        if new_attr_value_ids:
            queryset = queryset.filter(Q(product_filter_attributes_product__attribute_value__id__in = new_attr_value_ids)).order_by('-id').distinct("id")


        return queryset


class PcBuilderCategoryAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        data_list = []
        category_queryset = Category.objects.filter(is_active=True, pc_builder=True).order_by('ordering_number')
        category_serializer = PcBuilderCategoryListSerializer(category_queryset, many=True, context={"request": request})

        for cat_data_l in category_serializer.data:
            data_list.append(cat_data_l)

        sub_category_queryset = SubCategory.objects.filter(is_active=True, pc_builder=True).order_by('ordering_number')
        sub_category_serializer = PcBuilderSubCategoryListSerializer(sub_category_queryset, many=True, context={"request": request})

        for sub_cat_data_l in sub_category_serializer.data:
            data_list.append(sub_cat_data_l)

        sub_sub_category_queryset = SubSubCategory.objects.filter(is_active=True, pc_builder=True).order_by('ordering_number')
        sub_sub_category_serializer = PcBuilderSubSubCategoryListSerializer(sub_sub_category_queryset, many=True, context={"request": request})

        for sub_sub_cat_data_l in sub_sub_category_serializer.data:
            data_list.append(sub_sub_cat_data_l)

        return Response(data_list)


class OnlyTitleAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        id = request.GET.get('id')
        type = request.GET.get('type')

        if id and type:
            title = ''
            if type == 'category':
                if Category.objects.filter(id=id).exists():
                    title = Category.objects.get(id=id).title
                else:
                    title = ''
            if type == 'sub_category':
                if SubCategory.objects.filter(id=id).exists():
                    title = SubCategory.objects.get(id=id).title
                else:
                    title = ''
            if type == 'sub_sub_category':
                if SubSubCategory.objects.filter(id=id).exists():
                    title = SubSubCategory.objects.get(id=id).title
                else:
                    title = ''
            return Response({"id": id, "title": title, "type": type }, status=status.HTTP_200_OK)
        else:
            raise ValidationError({"msg":'id or type missing!'})


class BrandListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BrandListSerializer

    def get_queryset(self):
        queryset = Brand.objects.filter(is_active=True)
        if queryset:
            return queryset
        else:
            raise ValidationError({"msg": "No brand available! " })


