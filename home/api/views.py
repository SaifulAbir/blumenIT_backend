from rest_framework.views import APIView
from home.models import SliderImage, DealsOfTheDay
from home.serializers import SliderImagesListSerializer, DealsOfTheDayListSerializer, top_20_best_sellerListSerializer
# from home.serializers import SliderImagesListSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from datetime import date
from django.db.models import Q

from product.models import Product
class HomeDataAPIView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        # slider images
        slider_images = SliderImage.objects.filter(is_active=True)
        slider_images_serializer = SliderImagesListSerializer(slider_images, many=True)

        # deals of the day
        today = date.today()
        deals_of_the_day = DealsOfTheDay.objects.filter( start_date__lte=today, end_date__gte=today, is_active = True)
        deals_of_the_day_serializer = DealsOfTheDayListSerializer(deals_of_the_day, many=True)

        # top 20 best seller
        top_20_best_seller = Product.objects.filter(status='ACTIVE').order_by('-sell_count')[:20]
        top_20_best_seller_serializer = top_20_best_sellerListSerializer(top_20_best_seller, many=True)

        return Response({"slider_images": slider_images_serializer.data, "deals_of_the_day": deals_of_the_day_serializer.data, "top_20_best_seller": top_20_best_seller_serializer.data})