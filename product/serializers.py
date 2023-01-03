# from collections import OrderedDict
import collections
import base64
from itertools import product
from curses import meta
from email.policy import default
from pyexpat import model
from attr import fields
from rest_framework import serializers
from product.models import Category, ProductCombinationMedia, ProductImages, SubCategory, SubSubCategory, Product, ProductTags, ProductReview, ProductAttributes, Brand, DiscountTypes, Tags, Units, VariantType, Specification, SpecificationValue, AttributeValues, Seller, FilterAttributes

from user.models import User
from vendor.models import StoreSettings
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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'subtitle', 'icon', 'banner']


class SubSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSubCategory
        fields = ['id', 'title']


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


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = ['id', 'title']


class DiscountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountTypes
        fields = ['id', 'title']


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id', 'title']


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


class ProductReviewCreateSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        product_review_instance = ProductReview.objects.create(**validated_data, user=self.context['request'].user )
        return product_review_instance


class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserDataSerializer()
    created_at = serializers.DateTimeField(format="%d %B, %Y %I:%M %p")

    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'rating_number', 'review_text', 'created_at']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
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


class SpecificationValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationValue
        fields = [
            'id',
            'key',
            'value'
        ]


class SpecificationSerializer(serializers.ModelSerializer):
    specification_values = serializers.SerializerMethodField('get_existing_specification_values')
    title_name = serializers.CharField(source="title.title", read_only=True)
    class Meta:
        model = Specification
        fields = [
            'id',
            'title',
            'title_name',
            'specification_values'
        ]

    def get_existing_specification_values(self, instense):
        queryset = SpecificationValue.objects.filter(specification=instense.id, is_active = True)
        serializer = SpecificationValuesSerializer(instance=queryset, many=True)
        return serializer.data


class StoreCategoryAPIViewListSerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'icon', 'banner', 'sub_category']

    def get_sub_category(self, obj):
        try:
            queryset = SubCategory.objects.filter(category=obj.id, is_active=True).distinct()
            serializer = SubCategorySerializerForMegaMenu(instance=queryset, many=True)
            return serializer.data
        except:
            return []


class ProductDetailsSerializer(serializers.ModelSerializer):
    product_tags = serializers.SerializerMethodField()
    product_reviews = serializers.SerializerMethodField()
    seller = SellerDataSerializer()
    brand = BrandSerializer()
    unit = UnitSerializer()
    discount_type = DiscountTypeSerializer()
    avg_rating = serializers.SerializerMethodField()
    product_images = serializers.SerializerMethodField()
    product_specification = serializers.SerializerMethodField('get_product_specification')
    vat_type_title = serializers.CharField(source="vat_type.title",read_only=True)
    related_products = serializers.SerializerMethodField()

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
            'active_short_description',
            'seller',
            'thumbnail',
            'brand',
            'unit',
            'price',
            'old_price',
            'discount_type',
            'discount_amount',
            'discount_start_date',
            'discount_end_date',
            'quantity',
            'minimum_purchase_quantity',
            'bar_code',
            'refundable',
            'cash_on_delivery',
            'shipping_time',
            'pre_payment_amount',
            'vat',
            'vat_type',
            'vat_type_title',
            'product_tags',
            'product_images',
            'product_specification',
            'product_reviews',
            'warranty',
            'product_condition',
            'video_link',
            'related_products'
        ]

    def get_avg_rating(self, obj):
        return obj.product_review_product.all().aggregate(Avg('rating_number'))['rating_number__avg']

    def get_product_tags(self, obj):
        selected_product_tags = ProductTags.objects.filter(
            product=obj).distinct()
        return ProductTagsSerializer(selected_product_tags, many=True).data

    def get_product_specification(self, product):
        queryset = Specification.objects.filter(product=product, is_active = True)
        serializer = SpecificationSerializer(instance=queryset, many=True)
        return serializer.data

    def get_product_images(self, obj):
        try:
            queryset = ProductImages.objects.filter(
                product=obj, is_active=True).distinct()
            serializer = ProductImageSerializer(instance=queryset, many=True, context={
                                                'request': self.context['request']})
            return serializer.data
        except:
            return []

    def get_product_reviews(self, obj):
        selected_product_reviews = ProductReview.objects.filter(
            product=obj, is_active=True).distinct()
        return ProductReviewSerializer(selected_product_reviews, many=True).data

    def get_related_products(self, obj):
        selected_related_products = Product.objects.filter(
            category=obj.category.id, status='PUBLISH').exclude(id=obj.id).order_by('-sell_count')
        print(selected_related_products)
        return ProductListBySerializer(selected_related_products, many=True).data


class ProductListBySerializer(serializers.ModelSerializer):
    product_specification = serializers.SerializerMethodField('get_product_specification')
    product_tags = serializers.SerializerMethodField()
    discount_type = DiscountTypeSerializer()
    avg_rating = serializers.SerializerMethodField()
    brand_title= serializers.CharField(source="brand.title",read_only=True)
    product_condition_title= serializers.CharField(source="product_condition.title",read_only=True)
    review_count = serializers.SerializerMethodField('get_review_count')
    product_reviews = serializers.SerializerMethodField()
    seller = SellerDataSerializer()
    category = CategorySerializer()
    sub_category = SubCategorySerializer()
    sub_sub_category = SubSubCategorySerializer()
    brand = BrandSerializer()
    unit = UnitSerializer()

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'slug',
            'sku',
            'avg_rating',
            'status',
            'is_featured',
            'seller',
            'category',
            'sub_category',
            'sub_sub_category',
            'price',
            'old_price',
            'discount_type',
            'discount_amount',
            'total_quantity',
            'thumbnail',
            'product_tags',
            'product_specification',
            'brand',
            'unit',
            'brand_title',
            'product_condition',
            'product_condition_title',
            'short_description',
            'review_count',
            'shipping_time',
            'product_reviews',
            'warranty'
        ]

    def get_avg_rating(self, ob):
        return ob.product_review_product.all().aggregate(Avg('rating_number'))['rating_number__avg']

    def get_product_tags(self, obj):
        selected_product_tags = ProductTags.objects.filter(
            product=obj).distinct()
        return ProductTagsSerializer(selected_product_tags, many=True).data

    def get_product_specification(self, product):
        queryset = Specification.objects.filter(product=product, is_active = True)
        serializer = SpecificationSerializer(instance=queryset, many=True)
        return serializer.data

    def get_review_count(self, product):
        review_count = ProductReview.objects.filter(product=product, is_active = True).count()
        return review_count

    def get_product_reviews(self, obj):
        selected_product_reviews = ProductReview.objects.filter(
            product=obj, is_active=True).distinct()
        return ProductReviewSerializer(selected_product_reviews, many=True).data


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


class FilterAttributeSerializer(serializers.ModelSerializer):
    attribute_values = serializers.SerializerMethodField('get_attribute_values')
    attribute_title = serializers.CharField(source="attribute.title", read_only=True)
    class Meta:
        model = FilterAttributes
        fields = [
            'id',
            'attribute',
            'attribute_title',
            'attribute_values'
        ]

    def get_attribute_values(self, instance):
        # queryset = AttributeValues.objects.filter(attribute=instance.id, is_active = True)
        queryset = AttributeValues.objects.filter(attribute=instance.attribute.id, is_active = True)
        serializer = AttributeValuesSerializer(instance=queryset, many=True)
        return serializer.data


# class PcBuilderDataListSerializer(serializers.ModelSerializer):
#     specification = serializers.SerializerMethodField()
#     filtering_attributes = serializers.SerializerMethodField()

#     class Meta:
#         model = Product
#         fields = [
#             'id',
#             'thumbnail',
#             'title',
#             'slug',
#             'specification',
#             'filtering_attributes',
#             'price'
#         ]

    def get_specification(self, obj):
        try:
            queryset = Specification.objects.filter(product=obj, is_active = True)
            serializer = PcBuilderSpecificationSerializer(instance=queryset, many=True)
            return serializer.data
        except:
            return []

    def get_filtering_attributes(self, obj):
        try:
            selected_category_filtering_attributes = FilterAttributes.objects.filter(
                category=obj.category, is_active=True).distinct()
            return FilterAttributeSerializer(selected_category_filtering_attributes, many=True).data
        except:
            return []


class PcBuilderCategoryListSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'title', 'icon', 'type']

    def get_type(self, obj):
        return 'category'


class PcBuilderSubCategoryListSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    class Meta:
        model = SubCategory
        fields = ['id', 'title', 'icon', 'type']

    def get_type(self, obj):
        return 'sub_category'


class PcBuilderSubSubCategoryListSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    class Meta:
        model = SubSubCategory
        fields = ['id', 'title', 'icon', 'type']

    def get_type(self, obj):
        return 'sub_sub_category'

# work with pc builder end


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title', 'logo']