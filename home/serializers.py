from rest_framework import serializers
from .models import *
from product.models import Category

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
                'phone',
                'message',
                'is_active',
                ]


class SingleRowDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSingleRowData
        fields = [
                'id',
                'phone',
                'whats_app_number',
                'email',
                'bottom_banner',
                'is_active',
                ]


class PosterUnderSliderDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosterUnderSlider
        fields = [
                'id',
                'image',
                'is_active',
                ]


class PosterUnderPopularProductsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularProductsUnderPoster
        fields = [
                'id',
                'image',
                'bold_text',
                'small_text',
                'is_active',
                ]


class PosterUnderFeaturedProductsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedProductsUnderPoster
        fields = [
                'id',
                'image',
                'bold_text',
                'small_text',
                'is_active',
                ]

