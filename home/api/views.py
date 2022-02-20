from rest_framework.views import APIView
from home.models import SliderImage
from home.serializers import SliderImagesListSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class HomeDataAPIView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        slider_images = SliderImage.objects.filter(is_active=True)
        slider_images_serializer = SliderImagesListSerializer(slider_images, many=True)

        return Response({"slider_images": slider_images_serializer.data})