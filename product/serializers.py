# from collections import OrderedDict
import collections
import base64
from itertools import product
from curses import meta
from email.policy import default
from pyexpat import model
from attr import fields
from rest_framework import serializers
from product.models import Category, ProductCombinationMedia, ProductCombinationsVariants, ProductImages, SubCategory, SubSubCategory, Product, ProductTags, ProductReview, ProductCombinations, ProductAttributes, Brand, DiscountTypes, Tags, Units, VariantType
from user.models import User
from vendor.models import StoreSettings, Vendor, VendorReview
from django.db.models import Avg, Count, Q, F
from rest_framework.exceptions import ValidationError

# text color serializer
# User Data serializer


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email'
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


# Vendor serializer / Connect with ProductDetailsSerializer
class VendorSerializer(serializers.ModelSerializer):
    store_data = serializers.SerializerMethodField()
    vendor_first_name = serializers.CharField(source="vendor_admin.first_name")
    vendor_last_name = serializers.CharField(source="vendor_admin.last_name")
    avg_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        fields = [
            'id',
            'vendor_first_name',
            'vendor_last_name',
            'avg_rating',
            'review_count',
            'store_data'
        ]

    def get_avg_rating(self, ob):
        return ob.vendor_review_vendor.all().aggregate(Avg('rating_number'))['rating_number__avg']

    def get_review_count(self, obj):
        re_count = VendorReview.objects.filter(
            vendor=obj, is_active=True).count()
        return re_count

    def get_store_data(self, obj):
        selected_store_data = StoreSettings.objects.filter(
            vendor=obj).distinct()
        return StoreDataSerializer(selected_store_data, many=True, context={'request': self.context['request']}).data


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
    class Meta:
        model = Brand
        fields = ['id', 'title', 'logo']


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
    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'product', 'rating_number', 'review_text']


# Product Review serializer
class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserDataSerializer()
    created_at = serializers.DateTimeField(format="%d %B, %Y %I:%M %p")

    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'rating_number', 'review_text', 'created_at']


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
    vendor = VendorSerializer()
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
            'vendor',
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


# Product List serializer
class ProductListSerializer(serializers.ModelSerializer):
    product_tags = serializers.SerializerMethodField()
    product_reviews = serializers.SerializerMethodField()
    product_combinations = serializers.SerializerMethodField()
    vendor = VendorSerializer()
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
            'vendor',
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
            'product_combinations',
            'is_gaming'

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

# store front serializer


class StoreProductDetailsSerializer(serializers.ModelSerializer):
    product_tags = serializers.SerializerMethodField()
    product_reviews = serializers.SerializerMethodField()
    product_combinations = serializers.SerializerMethodField()
    vendor = VendorSerializer()
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
            'vendor',
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
            'product_combinations',
            'is_gaming'
        ]
        read_only_field = [
            'id',
            'title',
            'slug',
            'sku',
            'avg_rating',
            'full_description',
            'short_description',
            'status',
            'is_featured',
            'vendor',
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
            'product_combinations',
            'is_gaming'
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
# Product create serializer

