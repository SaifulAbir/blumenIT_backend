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

class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = ('id', 'name', 'status',)


class ProductTagsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="tags.title")
    class Meta:
        model = ProductTags
        fields = ('tags','title',)

class ProductSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(), many=True, write_only=True)
    product_tags = ProductTagsSerializer(many=True, read_only=True)

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
            'product_tags'
            # 'product_colors',
            # 'product_sizes'
        ]

    def create(self, validated_data):
        print("validated_data")
        # return validated_data
        tags = validated_data.pop('tags')
        # product_colors = validated_data.pop('product_colors')
        # product_sizes = validated_data.pop('product_sizes')

        product_instance = Product.objects.create(**validated_data, created_by=self.context['request'].user.id,)

        if tags:
            for tag in tags:
                ProductTags.objects.create(name=tag, product=product_instance)

        # if product_colors:
        #     for product_color in product_colors:
        #         ProductColors.objects.create(name=product_color, product=product_instance)

        # if product_sizes:
        #     for product_size in product_sizes:
        #         ProductSize.objects.create(name=product_size, product=product_instance)

        return product_instance


