from django.utils import timezone
from rest_framework import serializers
from product.models import \
    Category, \
    SubCategory, \
    SubSubCategory


class SubSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSubCategory
        fields = ['id','title']

class SubCategorySerializer(serializers.ModelSerializer):
    sub_sub_category = serializers.SerializerMethodField()
    class Meta:
        model = SubCategory
        fields = [
                    'id',
                    'title',
                    'sub_sub_category'
                ]
    def get_sub_sub_category(self, obj):
        selected_sub_sub_category = SubSubCategory.objects.filter(sub_category=obj).distinct()
        return SubSubCategorySerializer(selected_sub_sub_category, many=True).data

class ProductAllCategoryListSerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = [
                'id',
                'title',
                'sub_category'
                ]
    def get_sub_category(self, obj):
        selected_sub_category = SubCategory.objects.filter(category=obj).distinct()
        return SubCategorySerializer(selected_sub_category, many=True).data


# # general Serializer start
# class ProductCategoriesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model =  ProductCategory
#         fields = ['name']

# class ProductBrandsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductBrand
#         fields = ['name']

# class ProductTagsSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = ProductTags
#         fields = ['id', 'name', 'product']

# class ProductColorsSerializer(serializers.ModelSerializer):
#     # title = serializers.CharField(source="Colors.title")
#     class Meta:
#         model = ProductColors
#         fields = ['name']

# class ProductSizesSerializer(serializers.ModelSerializer):
#     # title = serializers.CharField(source="Sizes.title")
#     class Meta:
#         model = ProductSizes
#         fields = ['name']

# class ProductMediaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductMedia
#         fields = ['id', 'type', 'file', 'status']

# class ProductDetailsSerializer(serializers.ModelSerializer):
#     tags = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(), many=True, write_only=True)
#     colors = serializers.PrimaryKeyRelatedField(queryset=Colors.objects.all(), many=True, write_only=True)
#     sizes = serializers.PrimaryKeyRelatedField(queryset=Sizes.objects.all(), many=True, write_only=True)
#     media = serializers.ListField(child=serializers.FileField(), write_only=True)

#     product_tags = ProductTagsSerializer(many=True, read_only=True)
#     product_colors = ProductColorsSerializer(many=True, read_only=True)
#     product_sizes = ProductSizesSerializer(many=True, read_only=True)
#     product_media = ProductMediaSerializer(many=True, read_only=True)
#     class Meta:
#         model = Product
#         fields = [
#             'id',
#             'title',
#             'price',
#             'full_description',
#             'short_description',
#             'quantity',
#             'warranty',
#             'variation',
#             'rating',
#             'status',
#             'is_featured',
#             'product_category',
#             'product_brand',
#             'thumbnail',
#             'vendor',
#             'tags',
#             'product_tags',
#             'colors',
#             'product_colors',
#             'sizes',
#             'product_sizes',
#             'media',
#             'product_media'
#         ]

# 

# # general Serializer end


# # create Serializer start
# class ProductCreateSerializer(serializers.ModelSerializer):

#     tags = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(), many=True, write_only=True, required=False)
#     colors = serializers.PrimaryKeyRelatedField(queryset=Colors.objects.all(), many=True, write_only=True, required=False)
#     sizes = serializers.PrimaryKeyRelatedField(queryset=Sizes.objects.all(), many=True, write_only=True, required=False)
#     media = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)

#     product_tags = ProductTagsSerializer(many=True, read_only=True)
#     product_colors = ProductColorsSerializer(many=True, read_only=True)
#     product_sizes = ProductSizesSerializer(many=True, read_only=True)
#     product_media = ProductMediaSerializer(many=True, read_only=True)


#     class Meta:
#         model = Product
#         fields = [
#             'id',
#             'title',
#             'price',
#             'full_description',
#             'short_description',
#             'quantity',
#             'warranty',
#             'variation',
#             'rating',
#             'status',
#             'is_featured',
#             'product_category',
#             'product_sub_category',
#             'product_child_category',
#             'product_brand',
#             'thumbnail',
#             'vendor',
#             'tags',
#             'product_tags',
#             'colors',
#             'product_colors',
#             'sizes',
#             'product_sizes',
#             'media',
#             'product_media'
#         ]

#     def create(self, validated_data):
#         product_instance = Product.objects.create(**validated_data, created_by=self.context['request'].user.id,)
#         try:
#             tags = validated_data.pop('tags')
#             colors = validated_data.pop('colors')
#             sizes = validated_data.pop('sizes')
#             media = validated_data.pop('media')

#             if tags:
#                 for tag in tags:
#                     ProductTags.objects.create(name=tag, product=product_instance)

#             if colors:
#                 for color in colors:
#                     ProductColors.objects.create(name=color, product=product_instance)

#             if sizes:
#                 for size in sizes:
#                     ProductSizes.objects.create(name=size, product=product_instance)
#             if media:
#                 for media_file in media:
#                     file_type = media_file.content_type.split('/')[0]
#                     ProductMedia.objects.create(product=product_instance, type=file_type, file=media_file, status="COMPLETE")

#             return product_instance
#         except:
#             return product_instance


# class TagCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tags
#         fields = ('id', 'name', 'is_active')
#         read_only_fields = ('id', 'is_active')
# # create Serializer end


# # list Serializer start
# class ProductListSerializer(serializers.ModelSerializer):
#     product_media = ProductMediaSerializer(many=True, read_only=True)
#     product_category_name = serializers.SerializerMethodField()
#     product_brand_name = serializers.SerializerMethodField()
#     class Meta:
#         model = Product
#         fields = [
#                 'id',
#                 'title',
#                 'slug',
#                 'price',
#                 'old_price',
#                 'short_description',
#                 'quantity',
#                 'rating',
#                 'status',
#                 'is_featured',
#                 'product_category_name',
#                 'product_brand_name',
#                 'thumbnail',
#                 'product_media'
#                 ]

#     def get_product_category_name(self, obj):
#         if obj.product_category:
#             get_product_category=ProductCategory.objects.get(id= obj.product_category.id)
#             return get_product_category.name
#         else :
#             return obj.get_product_category
#     def get_product_brand_name(self, obj):
#         if obj.product_category:
#             get_product_brand_name=ProductBrand.objects.get(id= obj.product_brand.id)
#             return get_product_brand_name.name
#         else :
#             return obj.get_product_brand_name

# class TagListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tags
#         fields = ['id', 'name']

# class ProductCategoryListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductCategory
#         fields = ['id', 'name']


# class ProductSubCategoryListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductSubCategory
#         fields = ['id', 'name', 'category']

# class ProductBrandListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductBrand
#         fields = ['id', 'name']

# class ProductSearchSerializer(serializers.Serializer):
#     slug = serializers.CharField()
#     title = serializers.CharField()
#     price = serializers.CharField()
#     img = serializers.CharField(required=False)

# class MegaMenuDataAPIViewListSerializer(serializers.ModelSerializer):
#     product_sub_category = SubCategorySerializer(many=True)
#     class Meta:
#         model = ProductCategory
#         fields = ['id', 'name', 'logo', 'cover', 'product_sub_category']

# # list Serializer end

# # update Serializer start
# class ProductUpdateSerializer(serializers.ModelSerializer):
#     tags = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(), many=True, write_only=True)
#     colors = serializers.PrimaryKeyRelatedField(queryset=Colors.objects.all(), many=True, write_only=True)
#     sizes = serializers.PrimaryKeyRelatedField(queryset=Sizes.objects.all(), many=True, write_only=True)
#     media = serializers.ListField(child=serializers.FileField(), write_only=True)

#     product_tags = ProductTagsSerializer(many=True, read_only=True)
#     product_colors = ProductColorsSerializer(many=True, read_only=True)
#     product_sizes = ProductSizesSerializer(many=True, read_only=True)
#     product_media = ProductMediaSerializer(many=True, read_only=True)

#     class Meta:
#         model = Product
#         fields = [
#             'id',
#             'title',
#             'price',
#             'full_description',
#             'short_description',
#             'quantity',
#             'warranty',
#             'variation',
#             'rating',
#             'status',
#             'is_featured',
#             'product_category',
#             'product_sub_category',
#             'product_child_category',
#             'product_brand',
#             'thumbnail',
#             'vendor',
#             'tags',
#             'product_tags',
#             'colors',
#             'product_colors',
#             'sizes',
#             'product_sizes',
#             'media',
#             'product_media'
#         ]

#     def update(self, instance, validated_data):
#         try:
#             tags = validated_data.pop('tags')
#             colors = validated_data.pop('colors')
#             sizes = validated_data.pop('sizes')
#             media = validated_data.pop('media')
#             if tags:
#                 ProductTags.objects.filter(product=instance).delete()
#                 for tag in tags:
#                     ProductTags.objects.create(name=tag, product=instance)

#             if colors:
#                 ProductColors.objects.filter(product=instance).delete()
#                 for color in colors:
#                     ProductColors.objects.create(name=color, product=instance)

#             if sizes:
#                 ProductSizes.objects.filter(product=instance).delete()
#                 for size in sizes:
#                     ProductSizes.objects.create(name=sizes, product=instance)
#             if media:
#                 for media_file in media:
#                     file_type = media_file.content_type.split('/')[0]
#                     ProductMedia.objects.create(product=instance, type=file_type, file=media_file, status="COMPLETE")

#             validated_data.update({"modified_by": self.context['request'].user.id, "modified_at": timezone.now()})
#             return super().update(instance, validated_data)
#         except:
#             validated_data.update({"modified_by": self.context['request'].user.id, "modified_at": timezone.now()})
#             return super().update(instance, validated_data)
# # update Serializer end



# # vendor serializers start
# class VendorProductListSerializer(serializers.ModelSerializer):
#     product_media = ProductMediaSerializer(many=True, read_only=True)
#     product_category_name = serializers.SerializerMethodField()
#     product_brand_name = serializers.SerializerMethodField()
#     class Meta:
#         model = Product
#         fields = [
#                 'id',
#                 'title',
#                 'slug',
#                 'price',
#                 'old_price',
#                 'short_description',
#                 'quantity',
#                 'rating',
#                 'status',
#                 'is_featured',
#                 'product_category_name',
#                 'product_brand_name',
#                 'thumbnail',
#                 'product_media'
#                 ]

#     def get_product_category_name(self, obj):
#         try:
#             if obj.product_category:
#                 get_product_category=ProductCategory.objects.get(id= obj.product_category.id)
#                 return get_product_category.name
#             else :
#                 return obj.get_product_category
#         except:
#             return None
#     def get_product_brand_name(self, obj):
#         try:
#             if obj.product_category:
#                 get_product_brand_name=ProductBrand.objects.get(id= obj.product_brand.id)
#                 return get_product_brand_name.name
#             else :
#                 return obj.get_product_brand_name
#         except:
#             return None

# # vendor serializers end
