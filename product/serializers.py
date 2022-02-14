from django.utils import timezone
from rest_framework import serializers
from .models import *


# general Serializer start
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
    # title = serializers.CharField(source="Colors.title")
    class Meta:
        model = ProductColors
        fields = ['name']

class ProductSizesSerializer(serializers.ModelSerializer):
    # title = serializers.CharField(source="Sizes.title")
    class Meta:
        model = ProductSizes
        fields = ['name']

class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = ['id', 'type', 'file', 'status']

class ProductDetailsSerializer(serializers.ModelSerializer):
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
            'vendor',
            'tags',
            'product_tags',
            'colors',
            'product_colors',
            'sizes',
            'product_sizes',
            'media',
            'product_media'
        ]

class ChildCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductChildCategory
        fields = ['id','name']
class SubCategorySerializer(serializers.ModelSerializer):
    child_category = serializers.SerializerMethodField()
    class Meta:
        model = ProductSubCategory
        fields = ['id','name','child_category']
    def get_child_category(self, obj):
        selected_child_category = ProductChildCategory.objects.filter(sub_category=obj).distinct()
        return ChildCategorySerializer(selected_child_category, many=True).data
# general Serializer end


# create Serializer start
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
            'vendor',
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
                ProductSizes.objects.create(name=size, product=product_instance)
        if media:
            for media_file in media:
                file_type = media_file.content_type.split('/')[0]
                ProductMedia.objects.create(product=product_instance, type=file_type, file=media_file, status="COMPLETE")

        return product_instance

class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name', 'is_active')
        read_only_fields = ('id', 'is_active')
# create Serializer end


# list Serializer start
class ProductListSerializer(serializers.ModelSerializer):
    product_media = ProductMediaSerializer(many=True, read_only=True)
    product_category_name = serializers.SerializerMethodField()
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
                'product_brand',
                'thumbnail',
                'product_media'
                ]

    def get_product_category_name(self, obj):
        if obj.product_category:
            get_product_category=ProductCategory.objects.get(id= obj.product_category.id)
            return get_product_category.name
        else :
            return obj.get_product_category

class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id', 'name']

class ProductCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name']

class ProductAllCategoryListSerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()
    class Meta:
        model = ProductCategory
        fields = [
                'id',
                'name',
                'sub_category'
                ]
    def get_sub_category(self, obj):
        selected_sub_category = ProductSubCategory.objects.filter(category=obj).distinct()
        return SubCategorySerializer(selected_sub_category, many=True).data

class ProductSubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSubCategory
        fields = ['id', 'name', 'category']

class ProductBrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrand
        fields = ['id', 'name']

class ProductSearchSerializer(serializers.Serializer):
    slug = serializers.CharField()
    title = serializers.CharField()
    price = serializers.CharField()
    img = serializers.CharField(required=False)
# list Serializer end

# update Serializer start
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
            'tags',
            'product_tags',
            'colors',
            'product_colors',
            'sizes',
            'product_sizes',
            'media',
            'product_media'
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
# update Serializer end

