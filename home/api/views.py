from rest_framework.views import APIView
from home.models import SliderImage, FAQ, ContactUs, HomeSingleRowData, PosterUnderSlider, PopularProductsUnderPoster, \
    FeaturedProductsUnderPoster
from home.serializers import SliderImagesListSerializer, product_catListSerializer,\
    ContactUsSerializer, FaqSerializer, SingleRowDataSerializer, PosterUnderSliderDataSerializer, PosterUnderPopularProductsDataSerializer, \
        PosterUnderFeaturedProductsDataSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q, Count

from product.models import Product, Category, Brand
from product.serializers import ProductListBySerializer, BrandListSerializer
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ValidationError


class   HomeDataAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        # slider images
        slider_images = SliderImage.objects.filter(is_active=True)
        slider_images_serializer = SliderImagesListSerializer(slider_images, many=True, context={"request": request})

        # featured_categories
        featured_categories = Category.objects.filter(is_featured=True, is_active=True).order_by('-created_at')
        featured_categories_serializer = product_catListSerializer(featured_categories, many=True, context={"request": request})

        # featured
        featured = Product.objects.filter(status='PUBLISH', is_featured=True).order_by('-created_at')
        featured_serializer = ProductListBySerializer(featured, many=True, context={"request": request})

        # most popular
        popular = Product.objects.filter(status="PUBLISH").annotate(count=Count('product_review_product')).order_by('-count')
        popular_serializer = ProductListBySerializer(popular, many=True, context={"request": request})

        # gaming product
        gaming_product = Product.objects.filter(status="PUBLISH").order_by('-created_at')
        gaming_serializer = ProductListBySerializer(gaming_product, many=True, context={"request": request})

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