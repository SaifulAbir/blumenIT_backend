from django.utils import timezone
from rest_framework import serializers
from .models import *

class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = ['id', 'type', 'file', 'status']

class VendorProductListSerializer(serializers.ModelSerializer):
    product_media = ProductMediaSerializer(many=True, read_only=True)
    product_category_name = serializers.SerializerMethodField()
    product_brand_name = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = [
                'id',
                'title',
                'slug',
                'price',
                'old_price',
                'short_description',
                'quantity',
                'rating',
                'status',
                'is_featured',
                'product_category_name',
                'product_brand_name',
                'thumbnail',
                'product_media'
                ]

    def get_product_category_name(self, obj):
        if obj.product_category:
            get_product_category=ProductCategory.objects.get(id= obj.product_category.id)
            return get_product_category.name
        else :
            return obj.get_product_category
    def get_product_brand_name(self, obj):
        if obj.product_category:
            get_product_brand_name=ProductBrand.objects.get(id= obj.product_brand.id)
            return get_product_brand_name.name
        else :
            return obj.get_product_brand_name

class VendorProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
        ]