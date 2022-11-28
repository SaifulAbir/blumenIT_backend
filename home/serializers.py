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
                'background_img',
                'static_img',
                'text',
                ]


class DealsOfTheDayListSerializer(serializers.ModelSerializer):
    product = ProductDetailsSerializer(many=True, read_only=True)
    class Meta:
        model = DealsOfTheDay
        fields = [
                'id',
                'product',
                'discount_price',
                'discount_price_type',
                'start_date',
                'end_date'
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

# # # list Serializer end




# # # class mostPopularProductListSerializer(serializers.ModelSerializer):
# # #     average_rating = serializers.CharField(read_only=True)
# # #     class Meta:
# # #         model = Product
# # #         fields = [
# # #                 'id',
# # #                 'title',
# # #                 'slug',
# # #                 'price',
# # #                 'rating',
# # #                 'thumbnail',
# # #                 'average_rating'
# # #                 ]



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