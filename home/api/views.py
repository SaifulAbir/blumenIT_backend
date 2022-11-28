from rest_framework.views import APIView
from home.models import SliderImage, DealsOfTheDay, ProductView, FAQ, ContactUs
from home.serializers import SliderImagesListSerializer, DealsOfTheDayListSerializer, product_catListSerializer,\
    ContactUsSerializer, FaqSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from datetime import date, timedelta
from django.db.models import Avg, Prefetch, Q, Count

from product.models import Product, Category, ProductReview, Brand
from product.serializers import ProductListSerializer, BrandListSerializer


class HomeDataAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        # slider images
        slider_images = SliderImage.objects.filter(is_active=True)
        slider_images_serializer = SliderImagesListSerializer(slider_images, many=True, context={"request": request})

        # deals of the day
        # today = date.today()
        # deals_of_the_day = DealsOfTheDay.objects.filter(start_date__lte=today, end_date__gte=today, is_active=True)
        # deals_of_the_day_serializer = DealsOfTheDayListSerializer(deals_of_the_day, many=True,
        #                                                           context={"request": request})

        # top 20 best seller
        # top_20_best_seller = Product.objects.filter(status='PUBLISH').order_by('-sell_count')[:10]
        # top_20_best_seller_serializer = ProductListSerializer(top_20_best_seller, many=True,
        #                                                       context={"request": request})

        # top category of the month
        top_best_sellers = Product.objects.filter(status='PUBLISH').order_by('-sell_count')
        category_ids = top_best_sellers.values_list('category__id', flat=True).distinct()
        final_category_ids = []
        for category_id in category_ids:
            if category_id not in final_category_ids:
                final_category_ids.append(category_id)
        product_cat = Category.objects.filter(id__in=final_category_ids)[:6]
        product_cat_serializer = product_catListSerializer(product_cat, many=True, context={"request": request})

        # new arrivals
        # new_arrivals = Product.objects.filter(status='PUBLISH').order_by('-created_at')[:10]
        # new_arrivals_serializer = ProductListSerializer(new_arrivals, many=True, context={"request": request})

        # featured
        featured = Product.objects.filter(status='PUBLISH', is_featured=True).order_by('-created_at')
        featured_serializer = ProductListSerializer(featured, many=True, context={"request": request})

        # most popular
        # most_popular = Product.objects.filter(status="ACTIVE").annotate(Avg("product_review_product__rating_number")).
        # order_by('-product_review_product__rating_number')
        popular = Product.objects.filter(status="PUBLISH").annotate(count=Count('product_review_product')).order_by('-count')
        popular_serializer = ProductListSerializer(popular, many=True, context={"request": request})

        # gaming product
        # gaming_product = Product.objects.filter(is_gaming=True, status="PUBLISH").order_by('-created_at')
        gaming_product = Product.objects.filter(status="PUBLISH").order_by('-created_at')
        gaming_serializer = ProductListSerializer(gaming_product, many=True, context={"request": request})

        # brand list
        brand_list = Brand.objects.filter(is_active=True).order_by('-created_at')
        brand_list_serializer = BrandListSerializer(brand_list, many=True, context={"request": request})
        return Response({
            "slider_images": slider_images_serializer.data,
            "featured_categories": product_cat_serializer.data,
            "featured_products": featured_serializer.data,
            "popular_product": popular_serializer.data,
            "gaming_product": gaming_serializer.data,
            "brand_list": brand_list_serializer.data
        })

# # class RecentAPIView(APIView):
# #     def get(self, request):
# #         today = date.today()
# #         last_week = today - timedelta(days=7)
# #         user = self.request.user.id
# #         recent_view = Product.objects.filter(product_view_count__view_date__gt=last_week).order_by('-product_view_count__view_date')[:24]
# #         recent_view_serializer = productListSerializer(recent_view, many=True)
# #         return Response({"recent_view":recent_view_serializer.data })


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

