from rest_framework.views import APIView
from home.models import SliderImage, FAQ, ContactUs, HomeSingleRowData, PosterUnderSlider, PopularProductsUnderPoster, \
    FeaturedProductsUnderPoster
from home.serializers import SliderImagesListSerializer, product_catListSerializer,\
    ContactUsSerializer, FaqSerializer, SingleRowDataSerializer, PosterUnderSliderDataSerializer, PosterUnderPopularProductsDataSerializer, \
    PosterUnderFeaturedProductsDataSerializer, StoreCategoryAPIViewListSerializer, product_sub_catListSerializer, \
    CorporateDealCreateSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q, Count

from product.models import Product, Category, SubCategory, Brand
from product.serializers import ProductListBySerializer, BrandListSerializer, ProductListBySerializerForHomeData
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.exceptions import ValidationError
from product.pagination import ProductCustomPagination


class   HomeDataAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        # slider images
        slider_images = SliderImage.objects.filter(Q(is_active=True))
        slider_images_serializer = SliderImagesListSerializer(slider_images, many=True, context={"request": request})

        # featured_categories
        featured_categories = Category.objects.filter(is_featured=True, is_active=True).order_by('-created_at')
        featured_categories_serializer = product_catListSerializer(featured_categories, many=True, context={"request": request})

        # featured
        featured = Product.objects.filter(status='PUBLISH', is_featured=True).order_by('-created_at')
        featured_serializer = ProductListBySerializerForHomeData(featured, many=True, context={"request": request})

        # most popular
        popular = Product.objects.filter(status="PUBLISH").annotate(count=Count('product_review_product')).order_by('-count')
        popular_serializer = ProductListBySerializerForHomeData(popular, many=True, context={"request": request})

        # gaming product
        gaming_product = Product.objects.filter(status="PUBLISH").order_by('-created_at')
        gaming_serializer = ProductListBySerializerForHomeData(gaming_product, many=True, context={"request": request})

        # brand list
        brand_list = Brand.objects.filter(is_active=True).order_by('-created_at')
        brand_list_serializer = BrandListSerializer(brand_list, many=True, context={"request": request})

        # single row data
        single_row_data = HomeSingleRowData.objects.filter(Q(is_active=True)).order_by('-created_at')[:1]
        single_row_data_serializer = SingleRowDataSerializer(single_row_data, many=True, context={"request": request})

        # poster under slider
        poster_under_data = PosterUnderSlider.objects.filter(Q(is_active=True)).order_by('-created_at')[:3]
        poster_under_data_serializer = PosterUnderSliderDataSerializer(poster_under_data, many=True, context={"request": request})

        # poster under popular products
        poster_under_popular_products_data = PopularProductsUnderPoster.objects.filter(Q(is_active=True)).order_by('-created_at')[:3]
        poster_under_popular_products_data_serializer = PosterUnderPopularProductsDataSerializer(poster_under_popular_products_data, many=True, context={"request": request})

        # poster under featured products
        poster_under_featured_products_data = FeaturedProductsUnderPoster.objects.filter(Q(is_active=True)).order_by('-created_at')[:3]
        poster_under_featured_products_data_serializer = PosterUnderFeaturedProductsDataSerializer(poster_under_featured_products_data, many=True, context={"request": request})

        return Response({
            "slider_images": slider_images_serializer.data,
            "featured_categories": featured_categories_serializer.data,
            "featured_products": featured_serializer.data,
            "popular_product": popular_serializer.data,
            "gaming_product": gaming_serializer.data,
            "brand_list": brand_list_serializer.data,
            "single_row_data_serializer": single_row_data_serializer.data,
            "poster_under_slider_data_serializer": poster_under_data_serializer.data,
            "poster_under_popular_products_data_serializer": poster_under_popular_products_data_serializer.data,
            "poster_under_featured_products_data_serializer": poster_under_featured_products_data_serializer.data,
        })


class  GamingDataAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        # slider images
        slider_images = SliderImage.objects.filter(Q(is_active=True), Q(is_gaming=True))
        slider_images_serializer = SliderImagesListSerializer(slider_images, many=True, context={"request": request})

        # sub_categories_with_logo
        categories_with_logo = SubCategory.objects.filter(category__is_gaming__icontains=True, is_active=True).order_by('-created_at')[:8]
        categories_with_logo_serializer = product_sub_catListSerializer(categories_with_logo, many=True, context={"request": request})

        # popular_categories
        popular_categories = SubCategory.objects.filter(category__is_gaming__icontains=True, is_active=True).order_by('-created_at')
        popular_categories_serializer = product_sub_catListSerializer(popular_categories, many=True, context={"request": request})

        # popular products
        popular = Product.objects.filter(category__is_gaming__icontains=True, status="PUBLISH").annotate(count=Count('product_review_product')).order_by('-count')
        popular_serializer = ProductListBySerializer(popular, many=True, context={"request": request})

        # poster under popular products
        poster_under_popular_products_data = PopularProductsUnderPoster.objects.filter(Q(is_active=True), Q(is_gaming=True)).order_by('-created_at')[:3]
        poster_under_popular_products_data_serializer = PosterUnderPopularProductsDataSerializer(poster_under_popular_products_data, many=True, context={"request": request})

        # featured
        featured = Product.objects.filter(category__is_gaming__icontains=True, status='PUBLISH', is_featured=True).order_by('-created_at')
        featured_serializer = ProductListBySerializer(featured, many=True, context={"request": request})

        # poster under featured products
        poster_under_featured_products_data = FeaturedProductsUnderPoster.objects.filter(Q(is_active=True), Q(is_gaming=True)).order_by('-created_at')[:3]
        poster_under_featured_products_data_serializer = PosterUnderFeaturedProductsDataSerializer(poster_under_featured_products_data, many=True, context={"request": request})

        # brand list
        brand_list = Brand.objects.filter(is_active=True, is_gaming=True).order_by('-created_at')
        brand_list_serializer = BrandListSerializer(brand_list, many=True, context={"request": request})

        # single row data
        single_row_data = HomeSingleRowData.objects.filter(Q(is_active=True)).order_by('-created_at')[:1]
        single_row_data_serializer = SingleRowDataSerializer(single_row_data, many=True, context={"request": request})

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
            contact = ContactUs(name=name, email=email, phone=phone, message=message)
            contact.save()
            return Response({"message": "Your message has been sent successfully."})
        except:
            return Response({"message": "Fill up all the fields."})

    def get(self, request):
        contact = ContactUs.objects.all()
        contact_serializer = ContactUsSerializer(contact, many=True)
        return Response(contact_serializer.data)


class CreateGetFaqAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = FaqSerializer

    def post(self, request):
        try:
            question = request.data.get('question')
            answer = request.data.get('answer')
            faq = FAQ(question=question, answer=answer)
            faq.save()
            return Response({"message": "Faq has been created successfully."})
        except:
            return Response({"message": "Fill up all the fields."})

    def get(self, request):
        faq = FAQ.objects.all()
        faq_serializer = FaqSerializer(faq, many=True)
        return Response(faq_serializer.data)


class ProductListHomeCompareAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListBySerializer

    def get_queryset(self):
        queryset = Product.objects.filter(status='PUBLISH').order_by('-created_at')
        if queryset:
            return queryset
        else:
            raise ValidationError({"msg": 'No Publish products available!'})


class GamingCategoryListAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = StoreCategoryAPIViewListSerializer

    def get_queryset(self):
        queryset = Category.objects.filter(title__icontains='gaming', is_active=True).order_by('ordering_number')
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

        queryset = Product.objects.filter(category__title__icontains='gaming', status='PUBLISH').annotate(count=Count('product_review_product')).order_by('-count')

        if id and type:
            if type == 'category':
                queryset = queryset.filter(Q(category=id))

            if type == 'sub_category':
                queryset = queryset.filter(Q(sub_category=id))

            if type == 'sub_sub_category':
                queryset = queryset.filter(Q(sub_sub_category=id))

        else:
            queryset = Product.objects.filter(category__title__icontains='gaming', status='PUBLISH').annotate(count=Count('product_review_product')).order_by('-count')

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

        queryset = Product.objects.filter(category__title__icontains='gaming', is_featured=True, status='PUBLISH').order_by('-created_at')

        return queryset


class CorporateDealCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CorporateDealCreateSerializer

    def post(self, request, *args, **kwargs):
        return super(CorporateDealCreateAPIView, self).post(request, *args, **kwargs)
