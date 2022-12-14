from rest_framework import serializers
from .models import *
from product.models import Product, Category, Brand
from product.serializers import \
    ProductDetailsSerializer

# # # list Serializer start


class SliderImagesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderImage
        fields = [
                'id',
                'image',
                'bold_text',
                'small_text',
                ]


class product_catListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
                'id',
                'title',
                'icon',
                'banner',
                ]


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = [
                'id',
                'question',
                'answer',
                'is_active',
                ]


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = [
                'id',
                'name',
                'email',
                'message',
                'is_active',
                ]