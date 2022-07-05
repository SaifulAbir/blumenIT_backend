from curses import meta
from email.policy import default
from pyexpat import model
from attr import fields
from django.utils import timezone
from rest_framework import serializers
from product.models import \
    Category, \
    ProductCombinationMedia, \
    ProductCombinationsVariants, \
    SubCategory, \
    SubSubCategory, \
    Product, \
    ProductTags, \
    ProductReview, \
    ProductMedia, \
    ProductCombinations, \
    ProductAttributes, \
    Brand, \
    DiscountTypes, \
    Units, \
    VariantType
from user.models import User
from vendor.models import StoreSettings, Vendor
from django.db.models import Avg


# supporting serializers start
class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'first_name',
            'last_name',
            'email'
        ]

class StoreDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreSettings
        fields = [
            'id', 
            'store_name',
            'address',
            'email',
            'logo',
            'banner',
            'phone',
            'facebook',
            'twitter',
            'instagram',
            'youtube',
            'linkedin'
        ]

class VendorSerializer(serializers.ModelSerializer):
    store_data = serializers.SerializerMethodField()
    class Meta:
        model = Vendor
        fields = ['id', 'store_data']

    def get_store_data(self, obj):
        selected_store_data = StoreSettings.objects.filter(vendor=obj).distinct()
        return StoreDataSerializer(selected_store_data, many=True, context={'request': self.context['request']}).data

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']

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

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title', 'logo']

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = ['id', 'title']

class DiscountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountTypes
        fields = ['id', 'title']

class ProductTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTags
        fields = ['id', 'title']

class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserDataSerializer()
    created_at = serializers.DateTimeField(format="%d %B, %Y")
    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'rating_number', 'review_text', 'created_at']

class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = ['id', 'file']

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributes
        fields = ['id', 'title']

class ProductCombinationMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCombinationMedia
        fields = ['id', 'file']

class VariantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantType
        fields = [
                'id',
                'title'
        ]

class ProductCombinationsVariantsSerializer(serializers.ModelSerializer):
    variant_type = VariantTypeSerializer()
    discount_type = DiscountTypeSerializer()
    class Meta:
        model = ProductCombinationsVariants
        fields = [
                'id',
                'sku',
                'variant_type',
                'variant_value',
                'variant_price',
                'quantity',
                'discount_type',
                'discount_amount'
        ]

class ProductCombinationSerializerForProductDetails(serializers.ModelSerializer):
    product_attribute = ProductAttributeSerializer()
    combination_media = serializers.SerializerMethodField()
    variant = serializers.SerializerMethodField()
    class Meta:
        model = ProductCombinations
        fields = [
        'id',
        'product_attribute',
        'product_attribute_value',
        'product_attribute_color_code',
        'combination_media',
        'variant'
        ]

    def get_combination_media(self, obj):
        selected_combination_media = ProductCombinationMedia.objects.filter(product_combination=obj, status='COMPLETE').distinct()
        return ProductCombinationMediaSerializer(selected_combination_media, many=True).data
    def get_variant(self, obj):
        selected_variant = ProductCombinationsVariants.objects.filter(product_combination=obj, is_active=True).distinct()
        return ProductCombinationsVariantsSerializer(selected_variant, many=True).data
# supporting serializers end







# main serializers start
class MegaMenuDataAPIViewListSerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'title', 'logo', 'cover', 'sub_category']

    def get_sub_category(self, obj):
        selected_sub_category = SubCategory.objects.filter(category=obj).distinct()
        return SubCategorySerializer(selected_sub_category, many=True).data

class ProductDetailsSerializer(serializers.ModelSerializer):
    product_tags = serializers.SerializerMethodField()
    product_reviews = serializers.SerializerMethodField()
    product_media = serializers.SerializerMethodField()
    product_combinations = serializers.SerializerMethodField()
    vendor = VendorSerializer()
    category = CategorySerializer()
    sub_category = SubCategorySerializer()
    brand = BrandSerializer()
    unit = UnitSerializer()
    discount_type = DiscountTypeSerializer()
    avg_rating = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'slug',
            'sku',
            'warranty',
            'avg_rating',
            'full_description',
            'short_description',
            'status',
            'is_featured',
            'vendor',
            'category',
            'sub_category',
            'brand',
            'unit',
            'price',
            'old_price',
            'purchase_price',
            'tax_in_percent',
            'discount_type',
            'discount_amount',
            'total_quantity',
            'total_shipping_cost',
            'shipping_time',
            'thumbnail',
            'youtube_link',
            'product_tags',
            'product_reviews',
            'product_media',
            'product_combinations'
        ]

    def get_avg_rating(self, ob):
        return ob.product_review_product.all().aggregate(Avg('rating_number'))['rating_number__avg']
    def get_product_tags(self, obj):
        selected_product_tags = ProductTags.objects.filter(product=obj).distinct()
        return ProductTagsSerializer(selected_product_tags, many=True).data
    def get_product_reviews(self, obj):
        selected_product_reviews = ProductReview.objects.filter(product=obj, is_active=True).distinct()
        return ProductReviewSerializer(selected_product_reviews, many=True).data
    def get_product_media(self, obj):
        queryset = ProductMedia.objects.filter(product=obj).distinct()
        serializer = ProductMediaSerializer(instance=queryset, many=True, context={'request': self.context['request']})
        return serializer.data
    def get_product_combinations(self, obj):
        selected_product_combinations = ProductCombinations.objects.filter(product=obj, is_active=True).distinct()
        return ProductCombinationSerializerForProductDetails(selected_product_combinations, many=True).data

class ProductListSerializer(serializers.ModelSerializer):
    product_media = ProductMediaSerializer(many=True, read_only=True)
    category_name = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = [
                'id',
                'title',
                'slug',
                'sku',
                'price',
                'old_price',
                'short_description',
                'total_quantity',
                'status',
                'is_featured',
                'category_name',
                'brand_name',
                'thumbnail',
                'product_media',
                'avg_rating'
                ]

    def get_avg_rating(self, ob):
        return ob.product_review_product.all().aggregate(Avg('rating_number'))['rating_number__avg']

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
# main serializers end






















#     

# class ProductColorSerializerForProductCreate(serializers.ModelSerializer):
#     color = serializers.PrimaryKeyRelatedField(queryset=Colors.objects.all())
#     class Meta:
#         model = ProductColors
#         fields = [
#             'product', 'color'
#         ]

# class ProductAttributeSerializerForProductCreate(serializers.ModelSerializer):
#     attribute = serializers.PrimaryKeyRelatedField(queryset=Attributes.objects.all())
#     class Meta:
#         model = ProductAttributes
#         fields = [
#             'product', 'attribute'
#         ]

# class ProductAttributeValuesSerializerForProductCreate(serializers.ModelSerializer):
#     ProductAttributes = serializers.PrimaryKeyRelatedField(queryset=ProductAttributes.objects.all())
#     class Meta:
#         model = ProductAttributesValues
#         fields = [
#             'product', 'ProductAttributes', 'title'
#         ]
# class ProductCombinationSerializerForProductCreate(serializers.ModelSerializer):
#     sku = serializers.CharField(allow_blank=False, trim_whitespace=True, max_length=500)
#     varient = serializers.CharField(allow_blank=False, max_length=500)
#     varient_price = serializers.FloatField(default=0)
#     quantity = serializers.IntegerField(default=0)
#     product_color = ProductColorSerializerForProductCreate(required=False)
#     product_attribute = ProductAttributeSerializerForProductCreate(required=False)
#     product_attribute_values = ProductAttributeValuesSerializerForProductCreate(required=False)
#     discount_type = serializers.PrimaryKeyRelatedField(queryset=DiscountTypes.objects.all(), required=False)

#     class Meta:
#         model = ProductCombinations
#         fields = [
#             'sku',
#             'varient',
#             'varient_price',
#             'quantity',
#             'product_color',
#             'product_attribute',
#             'product_attribute_values',
#             'discount_type',
#             'discount_amount'
#         ]
# class ProductCreateSerializer(serializers.ModelSerializer):
#     # tags = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(), many=True, write_only=True, required=False)
#     # colors = serializers.PrimaryKeyRelatedField(queryset=Colors.objects.all(), many=True, write_only=True, required=False)
#     # sizes = serializers.PrimaryKeyRelatedField(queryset=Sizes.objects.all(), many=True, write_only=True, required=False)
#     # media = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)

#     # product_tags = ProductTagsSerializer(many=True, read_only=True)
#     # product_colors = ProductColorsSerializer(many=True, read_only=True)
#     # product_sizes = ProductSizesSerializer(many=True, read_only=True)
#     # product_media = ProductMediaSerializer(many=True, read_only=True)

#     # title = serializers.CharField(allow_blank=False)
#     product_media = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)
#     product_tags = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
#     # product_colors = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
#     # product_attributes = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
#     # product_attribute_values = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)


#     # prodcut_combinations
#     product_combination = serializers.ListField(child=ProductCombinationSerializerForProductCreate(), required=False)


#     class Meta:
#         model = Product
#         fields = [
#             'id',
#             'title',
#             'sku',
#             'warranty',
#             'full_description',
#             'short_description',
#             'category',
#             'sub_category',
#             'sub_sub_category',
#             'brand',
#             'unit',
#             'unit_price',
#             'purchase_price',
#             'tax_in_percent',
#             'discount_type',
#             'discount_amount',
#             'total_quantity',
#             'shipping_cost',
#             'shipping_time',
#             'thumbnail',
#             'youtube_link',

#             'product_media',
#             'product_tags',
#             # 'product_colors',
#             # 'product_attributes',
#             # 'product_attribute_values',
#             'product_combination'
#     #         'price',
#     #         'full_description',
#     #         'short_description',
#     #         'quantity',
#     #         'warranty',
#     #         'variation',
#     #         'rating',
#     #         'status',
#     #         'is_featured',
#     #         'product_category',
#     #         'product_sub_category',
#     #         'product_child_category',
#     #         'product_brand',
#     #         'thumbnail',
#     #         'vendor',
#     #         'tags',
#     #         'product_tags',
#     #         'colors',
#     #         'product_colors',
#     #         'sizes',
#     #         'product_sizes',
#     #         'media',
#     #         'product_media'
#         ]

#     def create(self, validated_data):
#         vendor = Vendor.objects.get(vendor_admin = self.context['request'].user.id)
#         product_instance = Product.objects.create(**validated_data, vendor=vendor)
#         return product_instance
#     #     try:
#     #         tags = validated_data.pop('tags')
#     #         colors = validated_data.pop('colors')
#     #         sizes = validated_data.pop('sizes')
#     #         media = validated_data.pop('media')

#     #         if tags:
#     #             for tag in tags:
#     #                 ProductTags.objects.create(name=tag, product=product_instance)

#     #         if colors:
#     #             for color in colors:
#     #                 ProductColors.objects.create(name=color, product=product_instance)

#     #         if sizes:
#     #             for size in sizes:
#     #                 ProductSizes.objects.create(name=size, product=product_instance)
#     #         if media:
#     #             for media_file in media:
#     #                 file_type = media_file.content_type.split('/')[0]
#     #                 ProductMedia.objects.create(product=product_instance, type=file_type, file=media_file, status="COMPLETE")

#     #         return product_instance
#     #     except:
#     #         return product_instance



# # # general Serializer start
# # class ProductCategoriesSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model =  ProductCategory
# #         fields = ['name']

# # class ProductBrandsSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = ProductBrand
# #         fields = ['name']

# # class ProductTagsSerializer(serializers.ModelSerializer):

# #     class Meta:
# #         model = ProductTags
# #         fields = ['id', 'name', 'product']

# # class ProductColorsSerializer(serializers.ModelSerializer):
# #     # title = serializers.CharField(source="Colors.title")
# #     class Meta:
# #         model = ProductColors
# #         fields = ['name']

# # class ProductSizesSerializer(serializers.ModelSerializer):
# #     # title = serializers.CharField(source="Sizes.title")
# #     class Meta:
# #         model = ProductSizes
# #         fields = ['name']

# # 

# # 

# # 

# # # general Serializer end


# # # create Serializer start
# # 


# # class TagCreateSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Tags
# #         fields = ('id', 'name', 'is_active')
# #         read_only_fields = ('id', 'is_active')
# # # create Serializer end


# # # list Serializer start
# #

# # class TagListSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Tags
# #         fields = ['id', 'name']

# # class ProductCategoryListSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = ProductCategory
# #         fields = ['id', 'name']


# # class ProductSubCategoryListSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = ProductSubCategory
# #         fields = ['id', 'name', 'category']

# # class ProductBrandListSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = ProductBrand
# #         fields = ['id', 'name']

# # class ProductSearchSerializer(serializers.Serializer):
# #     slug = serializers.CharField()
# #     title = serializers.CharField()
# #     price = serializers.CharField()
# #     img = serializers.CharField(required=False)

# # 

# # # list Serializer end

# # # update Serializer start
# # class ProductUpdateSerializer(serializers.ModelSerializer):
# #     tags = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(), many=True, write_only=True)
# #     colors = serializers.PrimaryKeyRelatedField(queryset=Colors.objects.all(), many=True, write_only=True)
# #     sizes = serializers.PrimaryKeyRelatedField(queryset=Sizes.objects.all(), many=True, write_only=True)
# #     media = serializers.ListField(child=serializers.FileField(), write_only=True)

# #     product_tags = ProductTagsSerializer(many=True, read_only=True)
# #     product_colors = ProductColorsSerializer(many=True, read_only=True)
# #     product_sizes = ProductSizesSerializer(many=True, read_only=True)
# #     product_media = ProductMediaSerializer(many=True, read_only=True)

# #     class Meta:
# #         model = Product
# #         fields = [
# #             'id',
# #             'title',
# #             'price',
# #             'full_description',
# #             'short_description',
# #             'quantity',
# #             'warranty',
# #             'variation',
# #             'rating',
# #             'status',
# #             'is_featured',
# #             'product_category',
# #             'product_sub_category',
# #             'product_child_category',
# #             'product_brand',
# #             'thumbnail',
# #             'vendor',
# #             'tags',
# #             'product_tags',
# #             'colors',
# #             'product_colors',
# #             'sizes',
# #             'product_sizes',
# #             'media',
# #             'product_media'
# #         ]

# #     def update(self, instance, validated_data):
# #         try:
# #             tags = validated_data.pop('tags')
# #             colors = validated_data.pop('colors')
# #             sizes = validated_data.pop('sizes')
# #             media = validated_data.pop('media')
# #             if tags:
# #                 ProductTags.objects.filter(product=instance).delete()
# #                 for tag in tags:
# #                     ProductTags.objects.create(name=tag, product=instance)

# #             if colors:
# #                 ProductColors.objects.filter(product=instance).delete()
# #                 for color in colors:
# #                     ProductColors.objects.create(name=color, product=instance)

# #             if sizes:
# #                 ProductSizes.objects.filter(product=instance).delete()
# #                 for size in sizes:
# #                     ProductSizes.objects.create(name=sizes, product=instance)
# #             if media:
# #                 for media_file in media:
# #                     file_type = media_file.content_type.split('/')[0]
# #                     ProductMedia.objects.create(product=instance, type=file_type, file=media_file, status="COMPLETE")

# #             validated_data.update({"modified_by": self.context['request'].user.id, "modified_at": timezone.now()})
# #             return super().update(instance, validated_data)
# #         except:
# #             validated_data.update({"modified_by": self.context['request'].user.id, "modified_at": timezone.now()})
# #             return super().update(instance, validated_data)
# # # update Serializer end



# # # vendor serializers start
# # class VendorProductListSerializer(serializers.ModelSerializer):
# #     product_media = ProductMediaSerializer(many=True, read_only=True)
# #     product_category_name = serializers.SerializerMethodField()
# #     product_brand_name = serializers.SerializerMethodField()
# #     class Meta:
# #         model = Product
# #         fields = [
# #                 'id',
# #                 'title',
# #                 'slug',
# #                 'price',
# #                 'old_price',
# #                 'short_description',
# #                 'quantity',
# #                 'rating',
# #                 'status',
# #                 'is_featured',
# #                 'product_category_name',
# #                 'product_brand_name',
# #                 'thumbnail',
# #                 'product_media'
# #                 ]

# #     def get_product_category_name(self, obj):
# #         try:
# #             if obj.product_category:
# #                 get_product_category=ProductCategory.objects.get(id= obj.product_category.id)
# #                 return get_product_category.name
# #             else :
# #                 return obj.get_product_category
# #         except:
# #             return None
# #     def get_product_brand_name(self, obj):
# #         try:
# #             if obj.product_category:
# #                 get_product_brand_name=ProductBrand.objects.get(id= obj.product_brand.id)
# #                 return get_product_brand_name.name
# #             else :
# #                 return obj.get_product_brand_name
# #         except:
# #             return None

# # # vendor serializers end


# # class ProductAllCategoryListSerializer(serializers.ModelSerializer):
# #     sub_category = serializers.SerializerMethodField()
# #     class Meta:
# #         model = Category
# #         fields = [
# #                 'id',
# #                 'title',
# #                 'sub_category'
# #                 ]
# #     def get_sub_category(self, obj):
# #         selected_sub_category = SubCategory.objects.filter(category=obj).distinct()
# #         return SubCategorySerializer(selected_sub_category, many=True).data