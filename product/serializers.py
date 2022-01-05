from django.utils import timezone
from rest_framework import serializers

from .models import *


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()
    product_tags = ProductTagsGetSerializer(many=True,read_only=True)
    product_colors = ProductColorsGetSerializer(many=True,read_only=True)
    product_size = ProductSizeGetSerializer(many=True,read_only=True)


    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'price',
            'full_description',
            'short_description',
            'quantity',
            'thumbnail',
            'warranty',
            'variation',
            'rating',
            'status',
            'is_featured',
            'product_category',
            'category_name',
            'product_brand',
            'brand_name',
            'product_tags'
        ]

class ProductCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrand
        fields = ['name']

class ProductBrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['name']