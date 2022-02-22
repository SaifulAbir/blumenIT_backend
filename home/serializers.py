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

class DealsOfTheDayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealsOfTheDay
        fields = [
                'id',
                'product',
                'discount_price',
                'discount_price_type'
                ]

class top_20_best_sellerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
                'id',
                'title',
                'slug',
                'price',
                'rating',
                'thumbnail',
                ]
# list Serializer end
