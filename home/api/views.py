from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView, UpdateAPIView
from home.models import FAQ, ContactUs, HomeSingleRowData, Advertisement, Pages, MediaFiles, AboutUs
from home.serializers import product_catListSerializer, PagesSerializer,\
    ContactUsSerializer, FaqSerializer, SingleRowDataSerializer, SliderAdvertisementDataSerializer, AdvertisementDataSerializer, \
    StoreCategoryAPIViewListSerializer, product_sub_catListSerializer, MediaSerializer, MediaDataSerializer, \
    CorporateDealCreateSerializer, RequestQuoteSerializer, AboutUsSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q, Count

from product.models import Product, Category, SubCategory, Brand
from product.serializers import ProductListBySerializer, BrandSerializer, ProductListBySerializerForHomeData
from rest_framework.exceptions import ValidationError
from product.pagination import ProductCustomPagination
from vendor.pagination import OrderCustomPagination


class HomeDataAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        # slider images
        slider_images = Advertisement.objects.filter(Q(work_for='SLIDER'), Q(
            is_active=True), Q(is_gaming=False)).order_by('-created_at')[:3]
        slider_images_serializer = AdvertisementDataSerializer(
            slider_images, many=True, context={"request": request})

        # Offer slider images
        offer_slider_images = Advertisement.objects.filter(Q(work_for='OFFER'), Q(
            is_active=True), Q(is_gaming=False)).order_by('-created_at')[:3]
        offer_slider_images_serializer = AdvertisementDataSerializer(
            offer_slider_images, many=True, context={"request": request})

        # categories
        categories = Category.objects.filter(
            is_featured=True, is_active=True).order_by('-ordering_number')
        categories_serializer = product_catListSerializer(
            categories, many=True, context={"request": request})

        # categories
        sub_categories = SubCategory.objects.filter(
            is_featured=True, is_active=True).order_by('-ordering_number')
        sub_categories_serializer = product_sub_catListSerializer(
            sub_categories, many=True, context={"request": request})

        featured_categories_serializer = categories_serializer.data + \
            sub_categories_serializer.data

        # featured
        featured = Product.objects.filter(
            status='PUBLISH', is_featured=True, is_active=True).order_by('-created_at')
        featured_serializer = ProductListBySerializerForHomeData(
            featured, many=True, context={"request": request})

        # most popular
        popular = Product.objects.filter(status="PUBLISH").annotate(
            count=Count('product_review_product')).order_by('-count')
        popular_serializer = ProductListBySerializerForHomeData(
            popular, many=True, context={"request": request})

        # gaming product
        gaming_product = Product.objects.filter(
            status="PUBLISH").order_by('-created_at')
        gaming_serializer = ProductListBySerializerForHomeData(
            gaming_product, many=True, context={"request": request})

        # brand list
        brand_list = Brand.objects.filter(
            is_active=True).order_by('-created_at')
        brand_list_serializer = BrandSerializer(
            brand_list, many=True, context={"request": request})

        # single row data
        single_row_data = HomeSingleRowData.objects.filter(
            Q(is_active=True)).order_by('-created_at')[:1]
        single_row_data_serializer = SingleRowDataSerializer(
            single_row_data, many=True, context={"request": request})

        # poster under slider static
        poster_under_static_data = Advertisement.objects.filter(Q(work_for='SLIDER_SMALL_STATIC'), Q(
            is_active=True), Q(is_gaming=False)).order_by('-created_at')[:2]
        poster_under_static_data_serializer = SliderAdvertisementDataSerializer(
            poster_under_static_data, many=True, context={"request": request})

        # poster under slider carousel
        poster_under_carousel_data = Advertisement.objects.filter(
            Q(work_for='SLIDER_SMALL_CAROUSEL'), Q(is_active=True), Q(is_gaming=False)).order_by('-created_at')
        poster_under_carousel_data_serializer = SliderAdvertisementDataSerializer(
            poster_under_carousel_data, many=True, context={"request": request})

        # poster under popular products
        poster_under_popular_products_data = Advertisement.objects.filter(
            Q(work_for='POPULAR_PRODUCT_POSTER'), Q(is_active=True), Q(is_gaming=False)).order_by('-created_at')[:3]
        poster_under_popular_products_data_serializer = AdvertisementDataSerializer(
            poster_under_popular_products_data, many=True, context={"request": request})

        # poster under featured products
        poster_under_featured_products_data = Advertisement.objects.filter(
            Q(work_for='FEATURED_PRODUCT_POSTER'), Q(is_active=True), Q(is_gaming=False)).order_by('-created_at')[:3]
        poster_under_featured_products_data_serializer = AdvertisementDataSerializer(
            poster_under_featured_products_data, many=True, context={"request": request})

        # info pages
        info_pages = Pages.objects.filter(
            Q(type='INFO'), Q(is_active=True)).order_by('-created_at')
        info_pages_serializer = PagesSerializer(
            info_pages, many=True, context={"request": request})

        # Customer Service pages
        customer_service_pages = Pages.objects.filter(
            Q(type='CS'), Q(is_active=True)).order_by('-created_at')
        customer_service_pages_serializer = PagesSerializer(
            customer_service_pages, many=True, context={"request": request})

        # faqs datas
        faqs = FAQ.objects.filter(is_active=True).order_by('-created_at')
        faqs_serializer = FaqSerializer(
            faqs, many=True, context={"request": request})

        return Response({
            "slider_images": slider_images_serializer.data,
            "offer_slider_images": offer_slider_images_serializer.data,
            "featured_categories": featured_categories_serializer,
            "featured_products": featured_serializer.data,
            "popular_product": popular_serializer.data,
            "gaming_product": gaming_serializer.data,
            "brand_list": brand_list_serializer.data,
            "single_row_data_serializer": single_row_data_serializer.data,
            "poster_under_carousel_data_serializer": poster_under_carousel_data_serializer.data,
            "poster_under_static_data_serializer": poster_under_static_data_serializer.data,
            "poster_under_popular_products_data_serializer": poster_under_popular_products_data_serializer.data,
            "poster_under_featured_products_data_serializer": poster_under_featured_products_data_serializer.data,
            "info_pages": info_pages_serializer.data,
            "customer_service": customer_service_pages_serializer.data,
            "faqs_serializer": faqs_serializer.data
        })


class GamingDataAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        # slider images
        slider_images = Advertisement.objects.filter(Q(work_for='SLIDER'), Q(
            is_active=True), Q(is_gaming=True)).order_by('-created_at')[:3]
        slider_images_serializer = AdvertisementDataSerializer(
            slider_images, many=True, context={"request": request})

        # sub_categories_with_logo
        categories_with_logo = SubCategory.objects.filter(
            category__is_gaming__icontains=True, is_active=True).order_by('-created_at')[:8]
        categories_with_logo_serializer = product_sub_catListSerializer(
            categories_with_logo, many=True, context={"request": request})

        # popular_sub_categories
        popular_categories = SubCategory.objects.filter(
            category__is_gaming__icontains=True, is_active=True).order_by("ordering_number")
        popular_categories_serializer = product_sub_catListSerializer(
            popular_categories, many=True, context={"request": request})

        # popular products
        popular = Product.objects.filter(category__is_gaming__icontains=True, status="PUBLISH").annotate(
            count=Count('product_review_product')).order_by('-count')
        popular_serializer = ProductListBySerializer(
            popular, many=True, context={"request": request})

        # poster under popular products
        poster_under_popular_products_data = Advertisement.objects.filter(
            Q(work_for='POPULAR_PRODUCT_POSTER'), Q(is_active=True), Q(is_gaming=True)).order_by('-created_at')[:3]
        poster_under_popular_products_data_serializer = AdvertisementDataSerializer(
            poster_under_popular_products_data, many=True, context={"request": request})

        # featured
        featured = Product.objects.filter(
            category__is_gaming__icontains=True, status='PUBLISH', is_featured=True).order_by('-created_at')
        featured_serializer = ProductListBySerializer(
            featured, many=True, context={"request": request})

        # poster under featured products
        poster_under_featured_products_data = Advertisement.objects.filter(
            Q(work_for='FEATURED_PRODUCT_POSTER'), Q(is_active=True), Q(is_gaming=True)).order_by('-created_at')[:3]
        poster_under_featured_products_data_serializer = AdvertisementDataSerializer(
            poster_under_featured_products_data, many=True, context={"request": request})

        # brand list
        brand_list = Brand.objects.filter(
            is_active=True, is_gaming=True).order_by('-created_at')
        brand_list_serializer = BrandSerializer(
            brand_list, many=True, context={"request": request})

        # single row data
        single_row_data = HomeSingleRowData.objects.filter(
            Q(is_active=True)).order_by('-created_at')[:1]
        single_row_data_serializer = SingleRowDataSerializer(
            single_row_data, many=True, context={"request": request})

        return Response({
            "poster_under_featured_products_data_serializer": poster_under_featured_products_data_serializer.data,
            "slider_images": slider_images_serializer.data,
            "categories_with_logo_serializer": categories_with_logo_serializer.data,
            "popular_categories_serializer": popular_categories_serializer.data,
            "popular_product": popular_serializer.data,
            "poster_under_popular_products_data_serializer": poster_under_popular_products_data_serializer.data,
            "featured_products": featured_serializer.data,
            "brand_list": brand_list_serializer.data,
            "single_row_data_serializer": single_row_data_serializer.data,
        })


class ContactUsAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ContactUsSerializer

    def post(self, request):
        try:
            name = request.data.get('name')
            email = request.data.get('email')
            phone = request.data.get('phone')
            message = request.data.get('message')
            contact = ContactUs(name=name, email=email,
                                phone=phone, message=message)
            contact.save()
            return Response({"message": "Your message has been sent successfully."})
        except:
            return Response({"message": "Fill up all the fields."})

    def get(self, request):
        contact = ContactUs.objects.all()
        contact_serializer = ContactUsSerializer(contact, many=True)
        return Response(contact_serializer.data)


class AboutUsAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AboutUsSerializer

    def get(self, request):
        contact = AboutUs.objects.filter(
            is_active=True).order_by('-created_at')[:1]
        contact_serializer = AboutUsSerializer(
            contact, many=True, context={"request": request})
        return Response(contact_serializer.data)


class ProductListHomeCompareAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListBySerializer

    def get_queryset(self):
        queryset = Product.objects.filter(
            status='PUBLISH').order_by('-created_at')
        if queryset:
            return queryset
        else:
            raise ValidationError({"msg": 'No Publish products available!'})


class GamingCategoryListAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = StoreCategoryAPIViewListSerializer

    def get_queryset(self):
        queryset = Category.objects.filter(
            title__icontains='gaming', is_active=True).order_by('ordering_number')
        return queryset


class ProductListByCategoryGamingPopularProductsAPI(ListAPIView):
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

        queryset = Product.objects.filter(category__title__icontains='gaming', status='PUBLISH').annotate(
            count=Count('product_review_product')).order_by('-count')

        if id and type:
            if type == 'category':
                queryset = queryset.filter(Q(category=id))

            if type == 'sub_category':
                queryset = queryset.filter(Q(sub_category=id))

            if type == 'sub_sub_category':
                queryset = queryset.filter(Q(sub_sub_category=id))

        else:
            queryset = Product.objects.filter(category__title__icontains='gaming', status='PUBLISH').annotate(
                count=Count('product_review_product')).order_by('-count')

        return queryset


class GamingFeaturedProductListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListBySerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        # work with dynamic pagination page_size
        try:
            pagination = self.kwargs['pagination']
        except:
            pagination = 10
        self.pagination_class.page_size = pagination

        queryset = Product.objects.filter(
            category__title__icontains='gaming', is_featured=True, status='PUBLISH').order_by('-created_at')

        return queryset


class CorporateDealCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CorporateDealCreateSerializer

    def post(self, request, *args, **kwargs):
        return super(CorporateDealCreateAPIView, self).post(request, *args, **kwargs)


class RequestQuoteAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RequestQuoteSerializer

    def post(self, request, *args, **kwargs):
        return super(RequestQuoteAPIView, self).post(request, *args, **kwargs)


class SingleRowDataAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        # single row data
        single_row_data = HomeSingleRowData.objects.filter(
            Q(is_active=True)).order_by('-created_at')[:1]
        single_row_data_serializer = SingleRowDataSerializer(
            single_row_data, many=True, context={"request": request})

        return Response({
            "single_row_data": single_row_data_serializer.data,
        })


# pages
class PagesListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PagesSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = Pages.objects.filter(
                is_active=True).order_by('-created_at')
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Pages data does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not view Pages list, because you are not an Admin or a Staff!'})


class PagesCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PagesSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(PagesCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create Pages, because you are not an Admin or a Staff!'})


class PagesUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PagesSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        target_id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            query = Pages.objects.filter(id=target_id)
            if query:
                return query
            else:
                raise ValidationError({"msg": 'Page data not found'})
        else:
            raise ValidationError(
                {"msg": 'You can not update  Page, because you are not an Admin, Staff or owner!'})

# media


class MediaListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MediaDataSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            request = self.request
            query = request.GET.get('search')

            queryset = MediaFiles.objects.filter(
                is_active=True).order_by('-created_at')
            if query:
                queryset = queryset.filter(Q(title__icontains=query))
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Media Files does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not view Media Files list, because you are not an Admin or a Staff!'})


class MediaCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MediaSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(MediaCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not upload Media file, because you are not an Admin or a Staff!'})


class MediaUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MediaDataSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        target_id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            query = MediaFiles.objects.filter(id=target_id)
            if query:
                return query
            else:
                raise ValidationError({"msg": 'Media file data not found'})
        else:
            raise ValidationError(
                {"msg": 'You can not update Media file, because you are not an Admin, Staff or owner!'})


# faq
class AdminFaqListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FaqSerializer
    pagination_class = OrderCustomPagination

    def get_queryset(self):
        request = self.request
        search = request.GET.get('search')
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = FAQ.objects.filter(
                is_active=True).order_by('-created_at')
            if search:
                queryset = queryset.filter(Q(question__icontains=search))
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No faq data available! "})
        else:
            raise ValidationError(
                {"msg": 'You can not see faq list, because you are not an Admin or a Staff!'})


class AdminFaqCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FaqSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminFaqCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create faq, because you are not an Admin or a Staff!'})


class AdminFaqUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FaqSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            query = FAQ.objects.filter(id=id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'FAQ does not found!'})
        else:
            raise ValidationError(
                {"msg": 'You can not update FAQ, because you are not an Admin or a Staff!'})


class AdminFaqDeleteAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = FaqSerializer
    queryset = FAQ.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        faq_id = self.kwargs['id']
        faq_obj = FAQ.objects.filter(id=faq_id).exists()
        if faq_obj:
            faq_obj = FAQ.objects.filter(id=faq_id)
            faq_obj.update(is_active=False)

            queryset = FAQ.objects.filter(
                is_active=True).order_by('-created_at')
            return queryset
        else:
            raise ValidationError(
                {"msg": 'FAQ Does not exist!'}
            )
