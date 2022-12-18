from rest_framework.views import APIView
from home.models import SliderImage, FAQ, ContactUs
from home.serializers import SliderImagesListSerializer, product_catListSerializer,\
    ContactUsSerializer, FaqSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from datetime import date, timedelta
from django.db.models import Avg, Prefetch, Q, Count

from product.models import Product, Category, Brand
from product.serializers import ProductListBySerializer, BrandListSerializer


class   HomeDataAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        # slider images
        slider_images = SliderImage.objects.filter(is_active=True)
        slider_images_serializer = SliderImagesListSerializer(slider_images, many=True, context={"request": request})

        # top category of the month
        # top_best_sellers = Product.objects.filter(status='PUBLISH').order_by('-sell_count')
        # category_ids = top_best_sellers.values_list('category__id', flat=True).distinct()
        # final_category_ids = []
        # for category_id in category_ids:
        #     if category_id not in final_category_ids:
        #         final_category_ids.append(category_id)
        # product_cat = Category.objects.filter(id__in=final_category_ids)[:6]
        # product_cat_serializer = product_catListSerializer(product_cat, many=True, context={"request": request})

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
        return Response({
            "slider_images": slider_images_serializer.data,
            "featured_categories": featured_categories_serializer.data,
            "featured_products": featured_serializer.data,
            "popular_product": popular_serializer.data,
            "gaming_product": gaming_serializer.data,
            "brand_list": brand_list_serializer.data
        })


class ContactUsAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ContactUsSerializer

    def post(self, request):
        try:
            name = request.data.get('name')
            email = request.data.get('email')
            message = request.data.get('message')
            contact = ContactUs(name=name, email=email, message=message)
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

