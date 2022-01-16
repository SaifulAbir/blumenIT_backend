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

class ProductCreateSerializer(serializers.ModelSerializer):
    product_tags = ProductTagsSerializer(many=True, read_only=True)
    product_colors = ProductColorsSerializer(many=True, read_only=True)
    product_sizes = ProductSizesSerializer(many=True, read_only=True)

    tags = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(), many=True, write_only=True)
    colors = serializers.PrimaryKeyRelatedField(queryset=Colors.objects.all(), many=True, write_only=True)
    sizes = serializers.PrimaryKeyRelatedField(queryset=Sizes.objects.all(), many=True, write_only=True)

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

class ProductUpdateSerializer(serializers.ModelSerializer):
    product_tags = ProductTagsSerializer(many=True, read_only=True)
    product_colors = ProductColorsSerializer(many=True, read_only=True)
    product_sizes = ProductSizesSerializer(many=True, read_only=True)

    tags = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(), many=True, write_only=True)
    colors = serializers.PrimaryKeyRelatedField(queryset=Colors.objects.all(), many=True, write_only=True)
    sizes = serializers.PrimaryKeyRelatedField(queryset=Sizes.objects.all(), many=True, write_only=True)

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

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        colors = validated_data.pop('colors')
        sizes = validated_data.pop('sizes')
        if tags:
            ProductTags.objects.filter(product=instance).delete()
            for tag in tags:
                ProductTags.objects.create(name=tag, product=instance)

        if colors:
            ProductColors.objects.filter(product=instance).delete()
            for color in colors:
                ProductColors.objects.create(name=color, product=instance)

        if sizes:
            ProductSizes.objects.filter(product=instance).delete()
            for size in sizes:
                ProductSizes.objects.create(name=sizes, product=instance)

        validated_data.update({"modified_by": self.context['request'].user.id, "modified_at": timezone.now()})
        return super().update(instance, validated_data)

class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name', 'is_active')
        read_only_fields = ('id', 'is_active')
