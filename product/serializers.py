# from collections import OrderedDict
import collections
import base64
from itertools import product
from curses import meta
from email.policy import default
from pyexpat import model
from attr import fields
from rest_framework import serializers
from product.models import Category, ProductCombinationMedia, ProductCombinationsVariants, ProductImages, SubCategory, SubSubCategory, Product, ProductTags, ProductReview, ProductCombinations, ProductAttributes, Brand, DiscountTypes, Tags, Units, VariantType, CategoryFilterAttributes, Specification, SpecificationValue, AttributeValues, Seller
from user.models import User
from vendor.models import StoreSettings, Vendor, VendorReview
from django.db.models import Avg, Count, Q, F
from rest_framework.exceptions import ValidationError

class SellerDataSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(allow_null=True)

    class Meta:
        model = Seller
        fields = ['id', 'name', 'address', 'phone', 'email', 'logo', 'is_active']

class UserDataSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source="user_customer_profile.avatar",read_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'avatar'
        ]



# Store Data serializer
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
            'bio',
            'facebook',
            'twitter',
            'instagram',
            'youtube',
            'linkedin'
        ]

# Category serializer / Connect with ProductDetailsSerializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'subtitle', 'cover', 'logo']


# Sub Sub Category serializer / Connect with ProductDetailsSerializer
class SubSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSubCategory
        fields = ['id', 'title']


# Sub Category serializer / Connect with ProductDetailsSerializer
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = [
            'id',
            'title',
        ]


class SubCategorySerializerForMegaMenu(serializers.ModelSerializer):
    sub_sub_category = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = [
            'id',
            'title',
            'sub_sub_category'
        ]

    def get_sub_sub_category(self, obj):
        selected_sub_sub_category = SubSubCategory.objects.filter(
            sub_category=obj).distinct()
        return SubSubCategorySerializer(selected_sub_sub_category, many=True).data


# Brands serializer / Connect with ProductDetailsSerializer
class BrandSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)

    class Meta:
        model = Brand
        fields = ['id', 'title', 'logo']

    def create(self, validated_data):
        title_get = validated_data.pop('title')
        title_get_data = title_get.lower()
        if title_get:
            title_get_for_check = Brand.objects.filter(title=title_get.lower())
            if title_get_for_check:
                raise ValidationError('This Brand already exist.')

        brand_instance = Brand.objects.create(**validated_data, title=title_get_data)

        return brand_instance


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title', 'logo']


# Units serializer / Connect with ProductDetailsSerializer
class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = ['id', 'title']


# Discount Types serializer / Connect with ProductDetailsSerializer
class DiscountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountTypes
        fields = ['id', 'title']


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id', 'title']

# Product Tags serializer


class ProductTagsSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = ProductTags
        fields = ['id', 'title', 'tag']

    def get_title(self, obj):
        try:
            tag_title = Tags.objects.get(id=obj.tag.id).title
        except:
            tag_title = ''
        return tag_title


# Product Attributes serializer
# class ProductAttributesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductAttributes
#         fields = ['id', 'title']


# Product Review Create serializer
class ProductReviewCreateSerializer(serializers.ModelSerializer):
    # user = UserDataSerializer(read_only=True)
    user = serializers.SerializerMethodField()
    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'product', 'rating_number', 'review_text']

    def get_user(self, obj):
        try:
            serializer = UserDataSerializer(instance=obj.user, many=False, context={
                                                'request': self.context['request']})
            return serializer.data
        except:
            return []


# Product Review serializer
class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserDataSerializer()
    # user = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d %B, %Y %I:%M %p")

    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'rating_number', 'review_text', 'created_at']

    # def get_user(self, obj):
    #     # return obj.user.username
    #     # try:
    #         serializer = UserDataSerializer(instance=obj.user, many=True, context={
    #                                             'request': self.context['request']})
    #         return serializer.data
    #     # except:
    #     #     return []


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        # fields = ['id', 'image']
        fields = ['id', 'file']


# Product Attribute serializer
class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributes
        fields = ['id', 'title']


# Product Combination Media serializer
class ProductCombinationMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCombinationMedia
        fields = ['id', 'file']


# Variant Types serializer
class VariantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantType
        fields = [
            'id',
            'title'
        ]


# Product Combination Variant serializer
class ProductCombinationsVariantsSerializer(serializers.ModelSerializer):
    variant_type = VariantTypeSerializer(required=False)
    discount_type = DiscountTypeSerializer(required=False)
    variant_value = serializers.CharField(required=False)

    class Meta:
        model = ProductCombinationsVariants
        fields = [
            'id',
            'variant_type',
            'variant_value',
            'variant_price',
            'quantity',
            'discount_type',
            'discount_amount'
        ]


# Product Combination serializer
class ProductCombinationSerializerForProductDetails(serializers.ModelSerializer):
    product_attribute = ProductAttributeSerializer()
    # combination_media = serializers.SerializerMethodField()
    variant = serializers.SerializerMethodField()

    class Meta:
        model = ProductCombinations
        fields = [
            'id',
            'product_attribute',
            'product_attribute_value',
            'product_attribute_color_code',
            'product_attribute_price',
            # 'combination_media',
            'variant'
        ]

    # def get_combination_media(self, obj):
    #     selected_combination_media = ProductCombinationMedia.objects.filter(
    #         product_combination=obj, status='COMPLETE').distinct()
    #     return ProductCombinationMediaSerializer(selected_combination_media, many=True).data

    def get_variant(self, obj):
        selected_variant = ProductCombinationsVariants.objects.filter(
            product_combination=obj, is_active=True).distinct()
        return ProductCombinationsVariantsSerializer(selected_variant, many=True).data


# Mega Menu Data serializer
class StoreCategoryAPIViewListSerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'logo', 'cover', 'sub_category']

    def get_sub_category(self, obj):
        selected_sub_category = SubCategory.objects.filter(
            category=obj).distinct()
        return SubCategorySerializerForMegaMenu(selected_sub_category, many=True).data


# Product Details serializer
class ProductDetailsSerializer(serializers.ModelSerializer):
    product_tags = serializers.SerializerMethodField()
    product_reviews = serializers.SerializerMethodField()
    product_combinations = serializers.SerializerMethodField()
    seller = SellerDataSerializer()
    category = CategorySerializer()
    sub_category = SubCategorySerializer()
    sub_sub_category = SubSubCategorySerializer()
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
            'avg_rating',
            'full_description',
            'short_description',
            'status',
            'is_featured',
            'seller',
            'category',
            'sub_category',
            'sub_sub_category',
            'brand',
            'unit',
            'price',
            'discount_type',
            'discount_amount',
            'total_quantity',
            'shipping_time',
            'thumbnail',
            'product_tags',
            'product_reviews',
            'product_combinations'
        ]

    def get_avg_rating(self, obj):
        return obj.product_review_product.all().aggregate(Avg('rating_number'))['rating_number__avg']

    def get_product_tags(self, obj):
        selected_product_tags = ProductTags.objects.filter(
            product=obj).distinct()
        return ProductTagsSerializer(selected_product_tags, many=True).data

    def get_product_reviews(self, obj):
        selected_product_reviews = ProductReview.objects.filter(
            product=obj, is_active=True).distinct()
        return ProductReviewSerializer(selected_product_reviews, many=True).data

    def get_product_combinations(self, obj):
        selected_product_combinations = ProductCombinations.objects.filter(
            product=obj, is_active=True).distinct()
        return ProductCombinationSerializerForProductDetails(selected_product_combinations, many=True).data


class ProductListSerializer(serializers.ModelSerializer):
    product_tags = serializers.SerializerMethodField()
    product_reviews = serializers.SerializerMethodField()
    product_combinations = serializers.SerializerMethodField()
    seller = SellerDataSerializer()
    category = CategorySerializer()
    sub_category = SubCategorySerializer()
    sub_sub_category = SubSubCategorySerializer()
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
            'avg_rating',
            'full_description',
            'short_description',
            'status',
            'is_featured',
            'seller',
            'category',
            'sub_category',
            'sub_sub_category',
            'brand',
            'unit',
            'price',
            'discount_type',
            'discount_amount',
            'total_quantity',
            'shipping_time',
            'thumbnail',
            'product_tags',
            'product_reviews',
            'product_combinations'

        ]

    def get_avg_rating(self, ob):
        return ob.product_review_product.all().aggregate(Avg('rating_number'))['rating_number__avg']

    def get_product_tags(self, obj):
        selected_product_tags = ProductTags.objects.filter(
            product=obj).distinct()
        return ProductTagsSerializer(selected_product_tags, many=True).data

    def get_product_reviews(self, obj):
        selected_product_reviews = ProductReview.objects.filter(
            product=obj, is_active=True).distinct()
        return ProductReviewSerializer(selected_product_reviews, many=True).data

    def get_product_combinations(self, obj):
        selected_product_combinations = ProductCombinations.objects.filter(
            product=obj, is_active=True).distinct()
        return ProductCombinationSerializerForProductDetails(selected_product_combinations, many=True).data

class ProductListBySerializer(serializers.ModelSerializer):
    product_tags = serializers.SerializerMethodField()
    discount_type = DiscountTypeSerializer()
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'slug',
            'avg_rating',
            'status',
            'price',
            'discount_type',
            'discount_amount',
            'total_quantity',
            'thumbnail',
            'product_tags'
        ]

    def get_avg_rating(self, ob):
        return ob.product_review_product.all().aggregate(Avg('rating_number'))['rating_number__avg']

    def get_product_tags(self, obj):
        selected_product_tags = ProductTags.objects.filter(
            product=obj).distinct()
        return ProductTagsSerializer(selected_product_tags, many=True).data

# work with pc builder start
class PcBuilderSpecificationValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationValue
        fields = [
            'id',
            'key',
            'value'
        ]

class PcBuilderSpecificationSerializer(serializers.ModelSerializer):
    specification_values = serializers.SerializerMethodField('get_existing_specification_values')
    title_name = serializers.CharField(source="title.title",read_only=True)
    class Meta:
        model = Specification
        fields = [
            'id',
            'title',
            'title_name',
            'specification_values'
        ]

    def get_existing_specification_values(self, instence):
        queryset = SpecificationValue.objects.filter(specification=instence.id, is_active = True)
        serializer = PcBuilderSpecificationValuesSerializer(instance=queryset, many=True)
        return serializer.data

class AttributeValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValues
        fields = [
            'id',
            'value',
        ]

class CategoryFilterAttributeSerializer(serializers.ModelSerializer):
    attribute_values = serializers.SerializerMethodField('get_attribute_values')
    attribute_title = serializers.CharField(source="attribute.title", read_only=True)
    class Meta:
        model = CategoryFilterAttributes
        fields = [
            'id',
            'attribute',
            'attribute_title',
            'attribute_values'
        ]

    def get_attribute_values(self, instense):
        queryset = AttributeValues.objects.filter(attribute=instense.id, is_active = True)
        serializer = AttributeValuesSerializer(instance=queryset, many=True)
        return serializer.data

class PcBuilderDataListSerializer(serializers.ModelSerializer):
    specification = serializers.SerializerMethodField()
    category_filtering_attributes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'thumbnail',
            'title',
            'specification',
            'category_filtering_attributes',
            'price'
        ]

    def get_specification(self, obj):
        try:
            queryset = Specification.objects.filter(product=obj, is_active = True)
            serializer = PcBuilderSpecificationSerializer(instance=queryset, many=True)
            return serializer.data
        except:
            return []

    def get_category_filtering_attributes(self, obj):
        try:
            selected_category_filtering_attributes = CategoryFilterAttributes.objects.filter(
                category=obj.category, is_active=True).distinct()
            return CategoryFilterAttributeSerializer(selected_category_filtering_attributes, many=True).data
        except:
            return []

# work with pc builder end