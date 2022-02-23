from rest_framework import serializers
from .models import *
from product.models import Product, ProductCategory

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

class productListSerializer(serializers.ModelSerializer):

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

class product_catListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = [
                'id',
                'name',
                'logo',
                'cover',
                ]

# list Serializer end
