from django.utils import timezone
from rest_framework import serializers
from .models import *

class ProductCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ProductCategory
        fields = ['name']

class ProductBrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrand
        fields = ['name']

class ProductTagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductTags
        fields = ('name')

class ProductColorsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="Colors.title")
    class Meta:
        model = ProductColors
        fields = ('name')

class ProductSizesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="Sizes.title")
    class Meta:
        model = ProductSizes
        fields = ('name')

class ProductSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(), many=True, write_only=True)
    product_tags = ProductTagsSerializer(many=True, read_only=True)
    colors = serializers.PrimaryKeyRelatedField(queryset=Colors.objects.all(), many=True, write_only=True)
    product_colors = ProductColorsSerializer(many=True, read_only=True)
    sizes = serializers.PrimaryKeyRelatedField(queryset=Sizes.objects.all(), many=True, write_only=True)
    product_sizes = ProductSizesSerializer(many=True, read_only=True)

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
            'product_brand',
            'tags',
            'product_tags',
            'colors',
            'product_colors',
            'sizes',
            'product_sizes'
        ]

    def create(self, validated_data):
        print("validated_data")
        tags = validated_data.pop('tags')
        colors = validated_data.pop('colors')
        sizes = validated_data.pop('sizes')
        product_instance = Product.objects.create(**validated_data, created_by=self.context['request'].user.id,)
        if tags:
            for tag in tags:
                ProductTags.objects.create(name=tag, product=product_instance)

        if colors:
            for color in colors:
                ProductColors.objects.create(name=color, product=product_instance)

        if sizes:
            for size in sizes:
                ProductSizes.objects.create(name=sizes, product=product_instance)

        return product_instance


