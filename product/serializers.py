# from collections import OrderedDict
import collections
import base64
from itertools import product
from curses import meta
from email.policy import default
from pyexpat import model
from attr import fields
from django.utils import timezone
from rest_framework import serializers
from product.models import Category, ProductCombinationMedia, ProductCombinationsVariants, SubCategory, SubSubCategory, Product, ProductTags, ProductReview, ProductMedia, ProductCombinations, ProductAttributes, Brand, DiscountTypes, Units, VariantType
from user.models import User
from vendor.models import StoreSettings, Vendor, VendorReview
from django.db.models import Avg, Count, Q, F
from rest_framework.exceptions import ValidationError


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


# Product Tags serializer
class ProductTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTags
        fields = ['id', 'title']


# Product Attributes serializer
class ProductAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributes
        fields = ['id', 'title']


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


# Product Media serializer
class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
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


# Product Combination serializer / Connect with ProductCreateSerializer
class ProductCombinationSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(required=False)
    variant_type = serializers.PrimaryKeyRelatedField(
        queryset=VariantType.objects.all(), many=False, write_only=True, required=False)
    variant_value = serializers.CharField(required=False)
    variant_price = serializers.FloatField(default=0.0, required=False)
    quantity = serializers.IntegerField(required=False)
    discount_type = serializers.PrimaryKeyRelatedField(
        queryset=DiscountTypes.objects.all(), many=False, write_only=True, required=False)
    discount_amount = serializers.FloatField(default=0.0, required=False)

    class Meta:
        model = ProductCombinations
        fields = [
            'id',
            'product_attribute',
            'product_attribute_value',
            'product_attribute_color_code',

            'sku',
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
class MegaMenuDataAPIViewListSerializer(serializers.ModelSerializer):
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
    product_media = serializers.SerializerMethodField()
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
            'warranty',
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
        selected_product_tags = ProductTags.objects.filter(
            product=obj).distinct()
        return ProductTagsSerializer(selected_product_tags, many=True).data

    def get_product_reviews(self, obj):
        selected_product_reviews = ProductReview.objects.filter(
            product=obj, is_active=True).distinct()
        return ProductReviewSerializer(selected_product_reviews, many=True).data

    def get_product_media(self, obj):
        queryset = ProductMedia.objects.filter(product=obj).distinct()
        serializer = ProductMediaSerializer(instance=queryset, many=True, context={
                                            'request': self.context['request']})
        return serializer.data

    def get_product_combinations(self, obj):
        selected_product_combinations = ProductCombinations.objects.filter(
            product=obj, is_active=True).distinct()
        return ProductCombinationSerializerForProductDetails(selected_product_combinations, many=True).data


# Product List serializer
class ProductListSerializer(serializers.ModelSerializer):
    product_tags = serializers.SerializerMethodField()
    product_reviews = serializers.SerializerMethodField()
    product_media = serializers.SerializerMethodField()
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
            'warranty',
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
        selected_product_tags = ProductTags.objects.filter(
            product=obj).distinct()
        return ProductTagsSerializer(selected_product_tags, many=True).data

    def get_product_reviews(self, obj):
        selected_product_reviews = ProductReview.objects.filter(
            product=obj, is_active=True).distinct()
        return ProductReviewSerializer(selected_product_reviews, many=True).data

    def get_product_media(self, obj):
        queryset = ProductMedia.objects.filter(product=obj).distinct()
        serializer = ProductMediaSerializer(instance=queryset, many=True, context={
                                            'request': self.context['request']})
        return serializer.data

    def get_product_combinations(self, obj):
        selected_product_combinations = ProductCombinations.objects.filter(
            product=obj, is_active=True).distinct()
        return ProductCombinationSerializerForProductDetails(selected_product_combinations, many=True).data

# Product create serializer
class ProductCreateSerializer(serializers.ModelSerializer):
    product_tags = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False)
    product_media = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False)
    product_combinations = ProductCombinationSerializer(
        many=True, required=False)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'sku',
            'warranty',
            'short_description',
            'full_description',
            'category',
            'sub_category',
            'sub_sub_category',
            'brand',
            'unit',
            'price',
            'purchase_price',
            'tax_in_percent',
            'discount_type',
            'discount_amount',
            'total_quantity',
            'shipping_cost',
            'shipping_cost_multiply',
            'shipping_time',
            'thumbnail',
            'youtube_link',
            'product_media',
            'product_tags',
            'product_combinations'
        ]

        read_only_fields = ('slug', 'is_featured', 'old_price',
                            'total_shipping_cost', 'sell_count')

    def create(self, validated_data):
        # validation for sku start
        try:
            sku = validated_data["sku"]
        except:
            sku = ''

        if sku:
            check_sku = Product.objects.filter(sku=sku)
            if check_sku:
                raise ValidationError('This SKU already exist.')
        # validation for sku end

        # validation for sub category and sub sub category start
        try:
            category_id = validated_data["category"].id
        except:
            category_id = ''

        try:
            sub_category = validated_data["sub_category"].id
        except:
            sub_category = ''

        if sub_category:
            check_sub_category = SubCategory.objects.filter(
                id=sub_category, category=category_id)
            if not check_sub_category:
                raise ValidationError(
                    'This Sub category is not under your selected parent category.')

        try:
            sub_sub_category = validated_data["sub_sub_category"].id
        except:
            sub_sub_category = ''

        if sub_sub_category:
            check_sub_sub_category = SubSubCategory.objects.filter(
                id=sub_sub_category, sub_category=sub_category, category=category_id)
            if not check_sub_sub_category:
                raise ValidationError(
                    'This Sub Sub category is not under your selected parent category.')
        # validation for sub category and sub sub category end

        try:
            product_media = validated_data.pop('product_media')
        except:
            product_media = ''

        try:
            product_tags = validated_data.pop('product_tags')
        except:
            product_tags = ''

        try:
            product_combinations = validated_data.pop('product_combinations')
        except:
            product_combinations = ''
        product_instance = Product.objects.create(**validated_data, vendor=Vendor.objects.get(vendor_admin=User.objects.get(
            id=self.context['request'].user.id)))
        try:
            if product_media:
                for media_file in product_media:
                    ProductMedia.objects.create(
                        product=product_instance, file=media_file, status="COMPLETE")
            if product_tags:
                for tag in product_tags:
                    ProductTags.objects.create(
                        title=tag, product=product_instance)
            if product_combinations:
                for product_combination in product_combinations:
                    product_attribute = product_combination['product_attribute']
                    product_attribute_value = product_combination['product_attribute_value']
                    product_attribute_color_code = product_combination['product_attribute_color_code']
                    product_combination_instance = ProductCombinations.objects.create(
                        product_attribute=product_attribute, product_attribute_value=product_attribute_value, product_attribute_color_code=product_attribute_color_code, product=product_instance)

                    variant_type = product_combination['variant_type']
                    variant_value = product_combination['variant_value']
                    variant_price = product_combination['variant_price']
                    quantity = product_combination['quantity']
                    discount_type = product_combination['discount_type']
                    discount_amount = product_combination['discount_amount']
                    ProductCombinationsVariants.objects.create(
                        variant_type=variant_type,  variant_value=variant_value, variant_price=variant_price, quantity=quantity, discount_type=discount_type, discount_amount=discount_amount, product_combination=product_combination_instance)
            return product_instance
        except:
            return product_instance

# Product update serializer


class ProductUpdateSerializer(serializers.ModelSerializer):
    #     # #     tags = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(), many=True, write_only=True)
    #     # #     media = serializers.ListField(child=serializers.FileField(), write_only=True)

    #     # #     product_tags = ProductTagsSerializer(many=True, read_only=True)
    #     # #     product_media = ProductMediaSerializer(many=True, read_only=True)

    # product_tags = serializers.SerializerMethodField()
    # product_tags = serializers.ListField(
    #     child=serializers.CharField(), write_only=True, required=False)
    # product_media = serializers.SerializerMethodField()
    # product_media = serializers.ListField(
    #     child=serializers.FileField(), write_only=True, required=False)
    # product_combinations = serializers.SerializerMethodField()

    # category = CategorySerializer()
    # sub_category = SubCategorySerializer()
    # sub_sub_category = SubSubCategorySerializer()
    # brand = BrandSerializer()
    # unit = UnitSerializer()
    # discount_type = DiscountTypeSerializer()

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'sku',
            # 'warranty',
            # 'full_description',
            # 'short_description',
            # 'status',
            # 'category',
            # 'sub_category',
            # 'sub_sub_category',
            # 'brand',
            # 'unit',
            'price',
            # 'purchase_price',
            # 'tax_in_percent',
            # 'discount_type',
            # 'discount_amount',
            # 'total_quantity',
            # 'total_shipping_cost',
            # 'shipping_time',
            # 'thumbnail',
            # 'youtube_link',
            # 'product_tags',
            # 'product_media',
            # 'product_combinations'
        ]

    # def get_product_tags(self, obj):
    #     selected_product_tags = ProductTags.objects.filter(
    #         product=obj).distinct()
    #     return ProductTagsSerializer(selected_product_tags, many=True).data

    # def get_product_media(self, obj):
    #     queryset = ProductMedia.objects.filter(product=obj).distinct()
    #     serializer = ProductMediaSerializer(instance=queryset, many=True, context={
    #                                         'request': self.context['request']})
    #     return serializer.data

    def update(self, instance, validated_data):
        # validation for sub category and sub sub category start
        # try:
        #     category_id = validated_data["category"].id
        # except:
        #     category_id = ''

        # sub_category = validated_data["sub_category"].id
        # if sub_category:
        #     check_sub_category = SubCategory.objects.filter(
        #         id=sub_category, category=category_id)
        #     if not check_sub_category:
        #         raise ValidationError(
        #             'This Sub category is not under your selected parent category.')

        # sub_sub_category = validated_data["sub_sub_category"].id
        # if sub_sub_category:
        #     check_sub_sub_category = SubSubCategory.objects.filter(
        #         id=sub_sub_category, sub_category=sub_category, category=category_id)
        #     if not check_sub_sub_category:
        #         raise ValidationError(
        #             'This Sub Sub category is not under your selected parent category.')
        # validation for sub category and sub sub category end

        # product price update start
        price = validated_data["price"]
        print('price')
        print(price)
        price_from_product = Product.objects.filter(id=instance)[0].price
        print('price_from_product')
        print(price_from_product)
        # if float(price) != float(price_from_product):

        # product price update end

        # try:
        # try:
        #     product_media = validated_data.pop('product_media')
        # except:
        #     product_media = ''

        # try:
        #     product_tags = validated_data.pop('product_tags')
        # except:
        #     product_tags = ''

#             try:
#                 product_combinations = validated_data.pop(
#                     'product_combinations')
#             except:
#                 product_combinations = ''

        # try:
        #     if product_tags:
        #         ProductTags.objects.filter(product=instance).delete()
        #         for product_tag in product_tags:
        #             ProductTags.objects.create(
        #                 name=product_tag, product=instance)

# #             if media:
# #                 for media_file in media:
# #                     file_type = media_file.content_type.split('/')[0]
# #                     ProductMedia.objects.create(product=instance, type=file_type, file=media_file, status="COMPLETE")

        #     validated_data.update(
        #         {"modified_by": self.context['request'].user.id, "modified_at": timezone.now()})
        #     return super().update(instance, validated_data)
        # except:
        #     return instance
        # except:
        #     validated_data.update(
        #         {"modified_by": self.context['request'].user.id, "modified_at": timezone.now()})
        #     return super().update(instance, validated_data)


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
