from rest_framework.views import APIView
from home.models import SliderImage, DealsOfTheDay
from home.serializers import SliderImagesListSerializer, DealsOfTheDayListSerializer
# from home.serializers import SliderImagesListSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from datetime import date
from django.db.models import Q
class HomeDataAPIView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        slider_images = SliderImage.objects.filter(is_active=True)
        slider_images_serializer = SliderImagesListSerializer(slider_images, many=True)

        today = date.today()
        deals_of_the_day = DealsOfTheDay.objects.filter( start_date__lte=today, end_date__gte=today, is_active = True)
        deals_of_the_day_serializer = DealsOfTheDayListSerializer(deals_of_the_day, many=True)

        return Response({"slider_images": slider_images_serializer.data, "deals_of_the_day": deals_of_the_day_serializer.data})