from rest_framework import serializers
from .models import *
from product.models import Product, Category, Brand
from product.serializers import ProductDetailsSerializer, ProductMediaSerializer

# # list Serializer start
class SliderImagesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderImage
        fields = [
                'id',
                'file',
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

class productListSerializer(serializers.ModelSerializer):
    product_media = ProductMediaSerializer(many=True, read_only=True)
    category_name = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()
    # average_rating = serializers.CharField(read_only=True)
    class Meta:
        model = Product
        fields = [
                'id',
                'title',
                'slug',
                'unit_price',
                'short_description',
                'total_quantity',
                'status',
                'is_featured',
                'category_name',
                'brand_name',
                'thumbnail',
                'product_media'
                ]

    def get_category_name(self, obj):
        if obj.category:
            get_category=Category.objects.get(id= obj.category.id)
            return get_category.title
        else :
            return obj.category
    def get_brand_name(self, obj):
        if obj.brand:
            get_brand=Brand.objects.get(id= obj.brand.id)
            return get_brand.title
        else :
            return obj.brand

class product_catListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
                'id',
                'title',
                'logo',
                'cover',
                ]

# # list Serializer end




# # class mostPopularProductListSerializer(serializers.ModelSerializer):
# #     average_rating = serializers.CharField(read_only=True)
# #     class Meta:
# #         model = Product
# #         fields = [
# #                 'id',
# #                 'title',
# #                 'slug',
# #                 'price',
# #                 'rating',
# #                 'thumbnail',
# #                 'average_rating'
# #                 ]
