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
        fields = ['id', 'name', 'product']

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

class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = ['id', 'type', 'file', 'status']

class ProductCreateSerializer(serializers.ModelSerializer):

    tags = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(), many=True, write_only=True)
    colors = serializers.PrimaryKeyRelatedField(queryset=Colors.objects.all(), many=True, write_only=True)
    sizes = serializers.PrimaryKeyRelatedField(queryset=Sizes.objects.all(), many=True, write_only=True)
    media = serializers.ListField(child=serializers.FileField(), write_only=True)

    product_tags = ProductTagsSerializer(many=True, read_only=True)
    product_colors = ProductColorsSerializer(many=True, read_only=True)
    product_sizes = ProductSizesSerializer(many=True, read_only=True)
    product_media = ProductMediaSerializer(many=True, read_only=True)


    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'price',
            'full_description',
            'short_description',
            'quantity',
            'warranty',
            'variation',
            'rating',
            'status',
            'is_featured',
            'product_category',
            'product_brand',
            'thumbnail',
            'cover',
            'tags',
            'product_tags',
            'colors',
            'product_colors',
            'sizes',
            'product_sizes',
            'media',
            'product_media'
        ]

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        colors = validated_data.pop('colors')
        sizes = validated_data.pop('sizes')
        media = validated_data.pop('media')

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
        if media:
            for media_file in media:
                file_type = media_file.content_type.split('/')[0]
                ProductMedia.objects.create(product=product_instance, type=file_type, file=media_file, status="COMPLETE")

        return product_instance


class ProductUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(), many=True, write_only=True)
    colors = serializers.PrimaryKeyRelatedField(queryset=Colors.objects.all(), many=True, write_only=True)
    sizes = serializers.PrimaryKeyRelatedField(queryset=Sizes.objects.all(), many=True, write_only=True)
    media = serializers.ListField(child=serializers.FileField(), write_only=True)

    product_tags = ProductTagsSerializer(many=True, read_only=True)
    product_colors = ProductColorsSerializer(many=True, read_only=True)
    product_sizes = ProductSizesSerializer(many=True, read_only=True)
    product_media = ProductMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'price',
            'full_description',
            'short_description',
            'quantity',
            'warranty',
            'variation',
            'rating',
            'status',
            'is_featured',
            'product_category',
            'product_brand',
            'thumbnail',
            'cover',
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
        media = validated_data.pop('media')
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
        if media:
            for media_file in media:
                file_type = media_file.content_type.split('/')[0]
                ProductMedia.objects.create(product=instance, type=file_type, file=media_file, status="COMPLETE")

        validated_data.update({"modified_by": self.context['request'].user.id, "modified_at": timezone.now()})
        return super().update(instance, validated_data)

class ProductListSerializer(serializers.ModelSerializer):
    product_media = ProductMediaSerializer(many=True, read_only=True)
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
                'product_category',
                'product_brand',
                'thumbnail',
                'product_media'
                ]

class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name', 'is_active')
        read_only_fields = ('id', 'is_active')
