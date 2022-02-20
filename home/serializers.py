from rest_framework import serializers
from .models import *

# list Serializer start
class SliderImagesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderImage
        fields = [
                'id',
                'file',
                'text',
                ]
# list Serializer end
