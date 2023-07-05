from datetime import datetime
from django.db.models import Q, Count, F, FloatField, ExpressionWrapper, Prefetch, Subquery, OuterRef, DecimalField
from django.db.models.functions import Coalesce
from ecommerce.settings import MEDIA_URL
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from home.models import ProductView
from product.serializers import ProductDetailsSerializer, ProductReviewCreateSerializer, \
    StoreCategoryAPIViewListSerializer, ProductListBySerializer, FilterAttributeSerializer, PcBuilderCategoryListSerializer, PcBuilderSubCategoryListSerializer, PcBuilderSubSubCategoryListSerializer, BrandSerializer, CategoryBannerImageSerializer

from vendor.serializers import AdminOfferSerializer

from product.models import Category, SubCategory, SubSubCategory, Product, Brand, Offer, OfferProduct, CategoryBannerImages
from product.models import FilterAttributes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from product.pagination import ProductCustomPagination
from itertools import chain
from user.models import CustomerProfile, User
from vendor.models import Vendor
from django.utils import timezone
from django.db.models import F, Case, When, DecimalField
from fuzzywuzzy import fuzz


class StoreCategoryListAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = StoreCategoryAPIViewListSerializer

    def get_queryset(self):
        queryset = Category.objects.filter(
            is_active=True).order_by('-ordering_number')
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
    pagination_class = ProductCustomPagination
    serializer_class = ProductListBySerializer

    def get_queryset(self):
        request = self.request
        seller = request.GET.get('seller')

        # queryset = Product.objects.filter(Q(status='PUBLISH') | Q(is_active=True)).order_by('-created_at')
        if seller:
            queryset = Product.objects.filter(
                status='PUBLISH', is_active=True, seller__id=seller).order_by('-created_at')
        else:
            queryset = Product.objects.filter(
                status='PUBLISH', is_active=True).order_by('-created_at')

        return queryset


class ProductListForOfferCreateAPI(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductListBySerializer

    def get_queryset(self):
        offer_id = self.request.GET.get('offer_id')
        product_list = [p.id for p in Product.objects.filter(
            is_active=True, status='PUBLISH').order_by('-created_at')]

        active_offers_products_list = [p.product.id for p in OfferProduct.objects.filter(
            is_active=True, offer__is_active=True, offer__end_date__gte=datetime.today()
        )]

        offers_products_list = [p.product.id for p in
                                OfferProduct.objects.filter(offer=offer_id, is_active=True)] if offer_id else []

        list_joined = [i for i in product_list if
                       i not in active_offers_products_list] + (
            offers_products_list if offers_products_list else list())

        return Product.objects.filter(id__in=list_joined).order_by(
            '-created_at') if list_joined else Product.objects.filter(is_active=True, status='PUBLISH').order_by('-created_at')

    # def get_queryset(self):
    #     if self.request.user.is_superuser == True or self.request.user.is_staff == True:
    #         a = []
    #         b = []
    #         active_products = Product.objects.filter(is_active=True, status='PUBLISH')
    #         for aa in active_products:
    #             a.append(aa.id)
    #         offer_products = OfferProduct.objects.filter(offer__is_active=True)
    #         for bb in offer_products:
    #             b.append(bb.product.id)
    #         new_product_id_list = [x for x in a if x not in b]
    #         queryset = Product.objects.filter(id__in=new_product_id_list)
    #         if queryset:
    #             return queryset
    #         else:
    #             raise ValidationError({"msg": 'Products do not exist!'})
    #     else:
    #         raise ValidationError(
    #             {"msg": 'You cannot view the offers list because you are not an admin or a staff member!'})


class ProductListByCategoryForOfferCreateAPI(ListAPIView):
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

        # order id get from offer update
        request = self.request
        offer_id = request.GET.get('offer_id')

        cid = self.kwargs['cid']
        if cid:
            all_products = Product.objects.filter(
                category=cid, status='PUBLISH').order_by('-created_at')

        product_list = []
        for q in all_products:
            p_id = q.id
            product_list.append(p_id)

        active_offers_products_list = []
        today_date = datetime.today()
        active_offers_products = OfferProduct.objects.filter(
            is_active=True, offer__is_active=True, offer__end_date__gte=today_date)
        for q_a in active_offers_products:
            p_id = q_a.product.id
            active_offers_products_list.append(p_id)

        # if offer_id id exist
        offers_products_list = []
        if offer_id:
            offers_products = OfferProduct.objects.filter(
                offer=offer_id, is_active=True)
            for a_p in offers_products:
                p_id = a_p.product.id
                offers_products_list.append(p_id)

        if offers_products_list:
            list_joined = [
                i for i in product_list if i not in active_offers_products_list] + offers_products_list
        else:
            list_joined = [
                i for i in product_list if i not in active_offers_products_list]

        if list_joined:
            queryset = Product.objects.filter(
                id__in=list_joined).order_by('-created_at')
        else:
            queryset = Product.objects.filter(
                status='PUBLISH').order_by('-created_at')

        return queryset


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
            queryset = Product.objects.filter(
                category=cid, status='PUBLISH').order_by('-created_at')
        else:
            queryset = Product.objects.filter(
                status='PUBLISH').order_by('-created_at')

        # filtering start
        request = self.request
        filter_price = request.GET.get('filter_price')
        attr_value_ids = request.GET.get('attr_value_ids')
        price_low_to_high = request.GET.get('price_low_to_high')
        price_high_to_low = request.GET.get('price_high_to_low')

        if filter_price:
            price_list = []
            filter_prices = filter_price.split("-")
            for filter_price in filter_prices:
                price_list.append(int(filter_price))

            min_price = price_list[0]
            max_price = price_list[1]
            queryset = queryset.filter(price__range=(
                min_price, max_price)).order_by('-created_at')

        new_attr_value_ids = []
        if attr_value_ids:
            attr_value_ids_list = attr_value_ids.split(",")
            for attr_value_id in attr_value_ids_list:
                attr_value_id = int(attr_value_id)
                new_attr_value_ids.append(attr_value_id)

        if new_attr_value_ids:
            queryset = queryset.filter(
                Q(product_filter_attributes_product__attribute_value__id__in=new_attr_value_ids)).order_by('-id').distinct("id")

        if price_low_to_high:
            # queryset = queryset.order_by('price').distinct('price')
            today_date = timezone.now().date()
            queryset = queryset.annotate(d_price=ExpressionWrapper((
                F('price') - Coalesce(Subquery(
                    Offer.objects.filter(offer_product_offer__product=OuterRef(
                        'pk'), is_active=True, end_date__gte=today_date).values('discount_price')[:1]
                ), 0)), output_field=DecimalField())).order_by('d_price')

        if price_high_to_low:
            # queryset = queryset.order_by('-price').distinct('-price')
            today_date = timezone.now().date()
            queryset = queryset.annotate(d_price=ExpressionWrapper((
                F('price') - Coalesce(Subquery(
                    Offer.objects.filter(offer_product_offer__product=OuterRef(
                        'pk'), is_active=True, end_date__gte=today_date).values('discount_price')[:1]
                ), 0)), output_field=DecimalField())).order_by('-d_price')

        return queryset


class GamingProductListByCategoryPopularProductsAPI(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductListBySerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        try:
            pagination = self.kwargs['pagination']
        except:
            pagination = 10
        self.pagination_class.page_size = pagination

        id = self.kwargs['id']
        type = self.kwargs['type']

        queryset = Product.objects.filter(category__is_gaming__icontains=True, status='PUBLISH').\
            annotate(count=Count('product_review_product')).order_by('-count')

        if id and type:
            if type == 'category':
                queryset = queryset.filter(Q(category=id))

            if type == 'sub_category':
                queryset = queryset.filter(Q(sub_category=id))

            if type == 'sub_sub_category':
                queryset = queryset.filter(Q(sub_sub_category=id))

        else:
            queryset = Product.objects.filter(category__is_gaming__icontains=True, status='PUBLISH').annotate(
                count=Count('product_review_product')).order_by('-count')

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

        queryset = Product.objects.filter(status='PUBLISH').annotate(
            count=Count('product_review_product')).order_by('-count')

        if id and type:
            if type == 'category':
                queryset = queryset.filter(Q(category=id))

            if type == 'sub_category':
                queryset = queryset.filter(Q(sub_category=id))

            if type == 'sub_sub_category':
                queryset = queryset.filter(Q(sub_sub_category=id))

        else:
            queryset = Product.objects.filter(status='PUBLISH').annotate(
                count=Count('product_review_product')).order_by('-count')

        return queryset


class FilterAttributesAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FilterAttributeSerializer

    def get_queryset(self):
        id = self.kwargs['id']
        type = self.kwargs['type']

        if id and type:
            if type == 'category':
                queryset = FilterAttributes.objects.filter(
                    Q(category__id=id) & Q(is_active=True)).order_by('-created_at')
            if type == 'sub_category':
                queryset = FilterAttributes.objects.filter(
                    Q(sub_category__id=id) & Q(is_active=True)).order_by('-created_at')
            if type == 'sub_sub_category':
                queryset = FilterAttributes.objects.filter(
                    Q(sub_sub_category__id=id) & Q(is_active=True)).order_by('-created_at')

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
        price_low_to_high = request.GET.get('price_low_to_high')
        price_high_to_low = request.GET.get('price_high_to_low')

        if filter_price:
            price_list = []
            filter_prices = filter_price.split("-")
            for filter_price in filter_prices:
                price_list.append(int(filter_price))

            min_price = price_list[0]
            max_price = price_list[1]
            queryset = queryset.filter(price__range=(
                min_price, max_price)).order_by('-created_at')

        new_attr_value_ids = []
        if attr_value_ids:
            attr_value_ids_list = attr_value_ids.split(",")
            for attr_value_id in attr_value_ids_list:
                attr_value_id = int(attr_value_id)
                new_attr_value_ids.append(attr_value_id)

        if new_attr_value_ids:
            queryset = queryset.filter(
                Q(product_filter_attributes_product__attribute_value__id__in=new_attr_value_ids)).order_by('-id').distinct("id")

        if price_low_to_high:
            # queryset = queryset.order_by('price').distinct('price')
            today_date = timezone.now().date()
            queryset = queryset.annotate(d_price=ExpressionWrapper((
                F('price') - Coalesce(Subquery(
                    Offer.objects.filter(offer_product_offer__product=OuterRef(
                        'pk'), is_active=True, end_date__gte=today_date).values('discount_price')[:1]
                ), 0)), output_field=DecimalField())).order_by('d_price')

        if price_high_to_low:
            # queryset = queryset.order_by('-price').distinct('-price')
            today_date = timezone.now().date()
            queryset = queryset.annotate(d_price=ExpressionWrapper((
                F('price') - Coalesce(Subquery(
                    Offer.objects.filter(offer_product_offer__product=OuterRef(
                        'pk'), is_active=True, end_date__gte=today_date).values('discount_price')[:1]
                ), 0)), output_field=DecimalField())).order_by('-d_price')

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
        price_low_to_high = request.GET.get('price_low_to_high')
        price_high_to_low = request.GET.get('price_high_to_low')

        if filter_price:
            price_list = []
            filter_prices = filter_price.split("-")
            for filter_price in filter_prices:
                price_list.append(int(filter_price))

            min_price = price_list[0]
            max_price = price_list[1]
            queryset = queryset.filter(price__range=(
                min_price, max_price)).order_by('-created_at')

        new_attr_value_ids = []
        if attr_value_ids:
            attr_value_ids_list = attr_value_ids.split(",")
            for attr_value_id in attr_value_ids_list:
                attr_value_id = int(attr_value_id)
                new_attr_value_ids.append(attr_value_id)

        if new_attr_value_ids:
            queryset = queryset.filter(
                Q(product_filter_attributes_product__attribute_value__id__in=new_attr_value_ids)).order_by('-id').distinct("id")

        if price_low_to_high:
            # queryset = queryset.order_by('price').distinct('price')
            today_date = timezone.now().date()
            queryset = queryset.annotate(d_price=ExpressionWrapper((
                F('price') - Coalesce(Subquery(
                    Offer.objects.filter(offer_product_offer__product=OuterRef(
                        'pk'), is_active=True, end_date__gte=today_date).values('discount_price')[:1]
                ), 0)), output_field=DecimalField())).order_by('d_price')

        if price_high_to_low:
            # queryset = queryset.order_by('-price').distinct('-price')
            today_date = timezone.now().date()
            queryset = queryset.annotate(d_price=ExpressionWrapper((
                F('price') - Coalesce(Subquery(
                    Offer.objects.filter(offer_product_offer__product=OuterRef(
                        'pk'), is_active=True, end_date__gte=today_date).values('discount_price')[:1]
                ), 0)), output_field=DecimalField())).order_by('-d_price')

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
            status='PUBLISH', is_active=True).order_by('-created_at')

        if query:
            queryset = queryset.filter(Q(title__icontains=query))

            if queryset.count() == 0:
                title_matches = [(product, fuzz.ratio(query, product.title))
                                 for product in Product.objects.all()]
                title_matches.sort(key=lambda x: x[1], reverse=True)
                top_match = title_matches[0][0]
                queryset = Product.objects.filter(
                    title__icontains=top_match.title)

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
                    vendor=vendor, status='PUBLISH').order_by('-created_at')
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
        price_low_to_high = request.GET.get('price_low_to_high')
        price_high_to_low = request.GET.get('price_high_to_low')

        queryset = Product.objects.filter(
            status='PUBLISH').order_by('-created_at')

        if component_id and type:
            if type == 'category':
                queryset = queryset.filter(
                    Q(category__id=component_id)).order_by('-created_at')
            if type == 'sub_category':
                queryset = queryset.filter(
                    Q(sub_category__id=component_id)).order_by('-created_at')
            if type == 'sub_sub_category':
                queryset = queryset.filter(
                    Q(sub_sub_category__id=component_id)).order_by('-created_at')

        if filter_price:
            price_list = []
            filter_prices = filter_price.split("-")
            for filter_price in filter_prices:
                price_list.append(int(filter_price))

            min_price = price_list[0]
            max_price = price_list[1]
            queryset = queryset.filter(price__range=(
                min_price, max_price)).order_by('-created_at')

        new_attr_value_ids = []
        if attr_value_ids:
            attr_value_ids_list = attr_value_ids.split(",")
            for attr_value_id in attr_value_ids_list:
                attr_value_id = int(attr_value_id)
                new_attr_value_ids.append(attr_value_id)

        if new_attr_value_ids:
            queryset = queryset.filter(
                Q(product_filter_attributes_product__attribute_value__id__in=new_attr_value_ids)).order_by(
                '-id').distinct("id")

        today = timezone.now()
        active_offers = OfferProduct.objects.filter(
            offer__is_active=True,
            offer__start_date__lte=today,
            offer__end_date__gte=today
        ).values_list('offer_id', flat=True)

        if active_offers:
            queryset = queryset.annotate(
                discount_price=Case(
                    When(id__in=active_offers, then=F(
                        'price') - F('discount_amount')),
                    default=F('price'),
                    output_field=DecimalField(max_digits=10, decimal_places=2)
                )
            )

            if price_low_to_high:
                # queryset = queryset.order_by('discount_price').distinct()
                today_date = timezone.now().date()
                queryset = queryset.annotate(d_price=ExpressionWrapper((
                    F('price') - Coalesce(Subquery(
                        Offer.objects.filter(offer_product_offer__product=OuterRef(
                            'pk'), is_active=True, end_date__gte=today_date).values('discount_price')[:1]
                    ), 0)), output_field=DecimalField())).order_by('d_price').distinct()
            elif price_high_to_low:
                # queryset = queryset.order_by('-discount_price').distinct()
                today_date = timezone.now().date()
                queryset = queryset.annotate(d_price=ExpressionWrapper((
                    F('price') - Coalesce(Subquery(
                        Offer.objects.filter(offer_product_offer__product=OuterRef(
                            'pk'), is_active=True, end_date__gte=today_date).values('discount_price')[:1]
                    ), 0)), output_field=DecimalField())).order_by('-d_price').distinct()

        else:
            if price_low_to_high:
                # queryset = queryset.order_by('price').distinct()
                today_date = timezone.now().date()
                queryset = queryset.annotate(d_price=ExpressionWrapper((
                    F('price') - Coalesce(Subquery(
                        Offer.objects.filter(offer_product_offer__product=OuterRef(
                            'pk'), is_active=True, end_date__gte=today_date).values('discount_price')[:1]
                    ), 0)), output_field=DecimalField())).order_by('d_price').distinct()
            elif price_high_to_low:
                # queryset = queryset.order_by('-price').distinct()
                today_date = timezone.now().date()
                queryset = queryset.annotate(d_price=ExpressionWrapper((
                    F('price') - Coalesce(Subquery(
                        Offer.objects.filter(offer_product_offer__product=OuterRef(
                            'pk'), is_active=True, end_date__gte=today_date).values('discount_price')[:1]
                    ), 0)), output_field=DecimalField())).order_by('-d_price').distinct()

        return queryset


class PcBuilderCategoryAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        data_list = []
        category_queryset = Category.objects.filter(
            is_active=True, pc_builder=True).order_by('id')
        category_serializer = PcBuilderCategoryListSerializer(
            category_queryset, many=True, context={"request": request})

        for cat_data_l in category_serializer.data:
            data_list.append(cat_data_l)

        sub_category_queryset = SubCategory.objects.filter(
            is_active=True, pc_builder=True).order_by('id')
        sub_category_serializer = PcBuilderSubCategoryListSerializer(
            sub_category_queryset, many=True, context={"request": request})

        for sub_cat_data_l in sub_category_serializer.data:
            data_list.append(sub_cat_data_l)

        sub_sub_category_queryset = SubSubCategory.objects.filter(
            is_active=True, pc_builder=True).order_by('id')
        sub_sub_category_serializer = PcBuilderSubSubCategoryListSerializer(
            sub_sub_category_queryset, many=True, context={"request": request})

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

                category_banner_data = CategoryBannerImages.objects.filter(
                    category=id, is_active=True).order_by('-created_at')
                category_banner_data_serializer = CategoryBannerImageSerializer(
                    category_banner_data, many=True, context={"request": request})
            if type == 'sub_category':
                if SubCategory.objects.filter(id=id).exists():
                    title = SubCategory.objects.get(id=id).title
                else:
                    title = ''

                category_banner_data = CategoryBannerImages.objects.filter(
                    category__sub_category_category__id=id, is_active=True).order_by('-created_at')
                category_banner_data_serializer = CategoryBannerImageSerializer(
                    category_banner_data, many=True, context={"request": request})
            if type == 'sub_sub_category':
                if SubSubCategory.objects.filter(id=id).exists():
                    title = SubSubCategory.objects.get(id=id).title
                else:
                    title = ''

                category_banner_data = CategoryBannerImages.objects.filter(
                    category__sub_sub_category_category__id=id, is_active=True).order_by('-created_at')
                category_banner_data_serializer = CategoryBannerImageSerializer(
                    category_banner_data, many=True, context={"request": request})
            return Response({"id": id, "title": title, "type": type, "category_banner_data": category_banner_data_serializer.data}, status=status.HTTP_200_OK)
        else:
            raise ValidationError({"msg": 'id or type missing!'})


class BrandListAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = BrandSerializer

    def get_queryset(self):

        queryset = Brand.objects.filter(is_active=True).order_by('-created_at')

        # filtering start
        request = self.request
        alphabetic = request.GET.get('alphabetic')
        popularity = request.GET.get('popularity')
        newest = request.GET.get('newest')

        if alphabetic:
            queryset = queryset.order_by('title')

        if popularity:
            queryset = queryset.order_by('-rating_number')

        if newest:
            queryset = queryset.order_by('-created_at')

        if queryset:
            return queryset
        else:
            raise ValidationError({"msg": "No brand available! "})


class ProductListByBrandAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListBySerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'bid'
    lookup_url_kwarg = "bid"

    def get_queryset(self):
        # work with dynamic pagination page_size
        try:
            pagination = self.kwargs['pagination']
        except:
            pagination = 10
        self.pagination_class.page_size = pagination

        bid = self.kwargs['bid']
        if bid:
            queryset = Product.objects.filter(
                brand=bid, status='PUBLISH').order_by('-created_at')
        else:
            queryset = Product.objects.filter(
                status='PUBLISH').order_by('-created_at')

        # filtering start
        request = self.request
        popularity = request.GET.get('popularity')
        newest = request.GET.get('newest')
        price_high_to_low = request.GET.get('price_high_to_low')
        price_low_to_high = request.GET.get('price_low_to_high')
        name = request.GET.get('name')

        if popularity:
            queryset = queryset.order_by('-total_average_rating_number')

        if newest:
            queryset = queryset.order_by('-created_at')

        if price_high_to_low:
            # queryset = queryset.order_by('-price')
            today_date = timezone.now().date()
            queryset = queryset.annotate(d_price=ExpressionWrapper((
                F('price') - Coalesce(Subquery(
                    Offer.objects.filter(offer_product_offer__product=OuterRef(
                        'pk'), is_active=True, end_date__gte=today_date).values('discount_price')[:1]
                ), 0)), output_field=DecimalField())).order_by('-d_price')

        if price_low_to_high:
            # queryset = queryset.order_by('price')
            today_date = timezone.now().date()
            queryset = queryset.annotate(d_price=ExpressionWrapper((
                F('price') - Coalesce(Subquery(
                    Offer.objects.filter(offer_product_offer__product=OuterRef(
                        'pk'), is_active=True, end_date__gte=today_date).values('discount_price')[:1]
                ), 0)), output_field=DecimalField())).order_by('d_price')

        if name:
            queryset = queryset.order_by('title')

        if queryset:
            return queryset
        else:
            raise ValidationError({"msg": "No products available! "})


class OffersListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = AdminOfferSerializer

    def get_queryset(self):
        today_date = datetime.today()
        queryset = Offer.objects.filter(
            end_date__gte=today_date, is_active=True).order_by('-created_at')
        if queryset:
            return queryset
        else:
            raise ValidationError({"msg": "No offers available! "})


class OfferDetailsAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = AdminOfferSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_object(self):
        offer_id = self.kwargs['id']
        try:
            query = Offer.objects.get(id=offer_id)
            return query
        except:
            raise ValidationError({"details": "Offer doesn't exist!"})


class OfferProductsListAPIView(ListAPIView):
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

        products = []
        offer_obj = Offer.objects.get(id=id)
        offer_products = OfferProduct.objects.filter(offer=offer_obj)
        for offer_product in offer_products:
            products.append(offer_product.product.id)

        if products:
            queryset = Product.objects.filter(
                id__in=products, status='PUBLISH').order_by('-created_at')
        else:
            queryset = Product.objects.filter(
                status='PUBLISH').order_by('-created_at')

        # filtering start
        request = self.request
        filter_price = request.GET.get('filter_price')
        attr_value_ids = request.GET.get('attr_value_ids')
        price_low_to_high = request.GET.get('price_low_to_high')
        price_high_to_low = request.GET.get('price_high_to_low')

        if filter_price:
            price_list = []
            filter_prices = filter_price.split("-")
            for filter_price in filter_prices:
                price_list.append(int(filter_price))

            min_price = price_list[0]
            max_price = price_list[1]
            queryset = queryset.filter(price__range=(
                min_price, max_price)).order_by('-created_at')

        new_attr_value_ids = []
        if attr_value_ids:
            attr_value_ids_list = attr_value_ids.split(",")
            for attr_value_id in attr_value_ids_list:
                attr_value_id = int(attr_value_id)
                new_attr_value_ids.append(attr_value_id)

        if new_attr_value_ids:
            queryset = queryset.filter(
                Q(product_filter_attributes_product__attribute_value__id__in=new_attr_value_ids)).order_by('-id').distinct("id")

        if price_low_to_high:
            # queryset = queryset.order_by('price')
            today_date = timezone.now().date()
            queryset = queryset.annotate(d_price=ExpressionWrapper((
                F('price') - Coalesce(Subquery(
                    Offer.objects.filter(offer_product_offer__product=OuterRef(
                        'pk'), is_active=True, end_date__gte=today_date).values('discount_price')[:1]
                ), 0)), output_field=DecimalField())).order_by('d_price')
        if price_high_to_low:
            # queryset = queryset.order_by('-price')
            today_date = timezone.now().date()
            queryset = queryset.annotate(d_price=ExpressionWrapper((
                F('price') - Coalesce(Subquery(
                    Offer.objects.filter(offer_product_offer__product=OuterRef(
                        'pk'), is_active=True, end_date__gte=today_date).values('discount_price')[:1]
                ), 0)), output_field=DecimalField())).order_by('-d_price')

        return queryset


class ProductListForProductCompareAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListBySerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        # filtering start
        request = self.request
        product_ids = request.GET.get('product_ids')

        new_product_ids = []
        if product_ids:
            product_ids_list = product_ids.split(",")
            for product_id in product_ids_list:
                product_id = int(product_id)
                new_product_ids.append(product_id)

        if new_product_ids:
            queryset = Product.objects.filter(
                status='PUBLISH').order_by('-created_at')
            queryset = queryset.filter(
                Q(id__in=new_product_ids)).order_by('-created_at')
        else:
            queryset = []

        return queryset
