from django.template.loader import render_to_string
from product.serializers import BrandSerializer, CategorySerializer, DiscountTypeSerializer, ProductCombinationSerializer, ProductCombinationSerializerForProductDetails, ProductMediaSerializer, ProductReviewSerializer, ProductTagsSerializer, SubCategorySerializer, SubSubCategorySerializer, UnitSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ecommerce.common.emails import send_email_without_delay
from product.models import Brand, Category, Product, ProductCombinations, ProductCombinationsVariants, ProductMedia, ProductReview, ProductTags, SubCategory, SubSubCategory, Units
from user.models import User
from user.serializers import UserRegisterSerializer
from vendor.models import VendorRequest, Vendor, StoreSettings
from django.db.models import Avg

# Vendor Request serializer


class VendorRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorRequest
        fields = ['id', 'first_name', 'last_name', 'organization_name',
                  'email', 'vendor_type', 'nid', 'trade_license']
        # fields = ['id', 'email', 'organization_name', 'first_name', 'last_name', 'vendor_type', 'nid', 'trade_license']


# Vendor Create serializer
class VendorCreateSerializer(serializers.ModelSerializer):
    is_verified = serializers.BooleanField(write_only=True)
    request_id = serializers.IntegerField(write_only=True)
    vendor_request = VendorRequestSerializer(read_only=True)
    vendor_admin = UserRegisterSerializer(read_only=True)

    class Meta:
        model = Vendor
        fields = ['id', 'organization_name', 'address', 'vendor_admin',
                  'vendor_request', 'phone', 'is_verified', 'request_id']
        read_only_fields = ('organization_name', 'address',
                            'vendor_admin', 'vendor_request', 'phone')

    def create(self, validated_data):
        is_verified = validated_data.pop('is_verified')
        request_id = validated_data.pop('request_id')
        if is_verified is True:
            password = User.objects.make_random_password()
            vendor_request = VendorRequest.objects.get(id=request_id)
            vendor_request.is_verified = True
            vendor_request.save()

            user = User.objects.create(username=vendor_request.email, email=vendor_request.email,
                                       first_name=vendor_request.first_name, last_name=vendor_request.last_name)
            user.set_password(password)
            user.save()

            vendor_instance = Vendor.objects.create(organization_name=vendor_request.organization_name,
                                                    vendor_admin=user, vendor_request=vendor_request, password=password)
            if vendor_instance:
                email_list = user.email
                subject = "Your Account"
                html_message = render_to_string('vendor_email.html',
                                                {'username': user.first_name, 'email': user.email, 'password': password})
                send_email_without_delay(subject, html_message, email_list)
            return vendor_instance
        else:
            raise ValidationError("You should verify first to create a vendor")


# Organization Name serializer
class OrganizationNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorRequest
        fields = ['organization_name']


# Vendor Detail serializer
class VendorDetailSerializer(serializers.ModelSerializer):
    vendor_request = VendorRequestSerializer(read_only=True)
    vendor_admin = UserRegisterSerializer(read_only=True)

    class Meta:
        model = Vendor
        fields = ['id', 'organization_name', 'vendor_admin',
                  'vendor_request', 'address', 'phone']


# Store Settings serializer
class StoreSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreSettings
        fields = ['id', 'store_name', 'address', 'email', 'phone', 'logo',
                  'banner', 'facebook', 'twitter', 'instagram', 'youtube', 'linkedin']

    def create(self, validated_data):
        user = self.context['request'].user
        vendor = Vendor.objects.get(vendor_admin=user)
        store_settings_instance = StoreSettings.objects.create(
            **validated_data, vendor=vendor)
        return store_settings_instance


# Vendor Category serializer
class VendorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "vendor category serializer"
        model = Category
        fields = ['id', 'title']


# Vendor Sub Category serializer
class VendorSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'title']


# Vendor Sub Sub Category serializer
class VendorSubSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSubCategory
        fields = ['id', 'title']


# Vendor Brand serializer
class VendorBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title']


# Vendor Unit serializer
class VendorUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = ['id', 'title']


class VendorProductListSerializer(serializers.ModelSerializer):
    product_media = ProductMediaSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    brand_name = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    discount_type = serializers.CharField()

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
            'category',
            'brand_name',
            'thumbnail',
            'product_media',
            'avg_rating',
            'review_count',
            'discount_type',
            'discount_amount'
        ]

    def get_avg_rating(self, obj):
        return obj.product_review_product.all().aggregate(Avg('rating_number'))['rating_number__avg']

    def get_brand_name(self, obj):
        if obj.brand:
            get_brand = Brand.objects.get(id=obj.brand.id)
            return get_brand.title
        else:
            return obj.brand

    def get_review_count(self, obj):
        re_count = ProductReview.objects.filter(
            product=obj, is_active=True).count()
        return re_count


class ProductCombinationSerializerForVendorProductDetails(serializers.ModelSerializer):
    # sku = serializers.CharField(required=False)
    variant_type = serializers.SerializerMethodField()
    variant_value = serializers.SerializerMethodField()
    variant_price = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    discount_type = serializers.SerializerMethodField()
    discount_amount = serializers.SerializerMethodField()

    class Meta:
        model = ProductCombinations
        fields = [
            'id',
            'product_attribute',
            'product_attribute_value',
            'product_attribute_color_code',

            'variant_type',
            'variant_value',
            'variant_price',
            'quantity',
            'discount_type',
            'discount_amount'
        ]

    def get_variant_type(self, obj):
        variant_type = ProductCombinationsVariants.objects.get(
            product_combination=obj, is_active=True).variant_type.id
        return variant_type

    def get_variant_value(self, obj):
        variant_value = ProductCombinationsVariants.objects.get(
            product_combination=obj, is_active=True).variant_value
        return variant_value

    def get_variant_price(self, obj):
        variant_price = ProductCombinationsVariants.objects.get(
            product_combination=obj, is_active=True).variant_price
        return variant_price

    def get_quantity(self, obj):
        quantity = ProductCombinationsVariants.objects.get(
            product_combination=obj, is_active=True).quantity
        return quantity

    def get_discount_type(self, obj):
        discount_type = ProductCombinationsVariants.objects.get(
            product_combination=obj, is_active=True).discount_type.id
        return discount_type

    def get_discount_amount(self, obj):
        discount_amount = ProductCombinationsVariants.objects.get(
            product_combination=obj, is_active=True).discount_amount
        return discount_amount


class VendorProductDetailsSerializer(serializers.ModelSerializer):
    product_tags = serializers.SerializerMethodField()
    product_reviews = serializers.SerializerMethodField()
    product_media = serializers.SerializerMethodField()
    product_combinations = serializers.SerializerMethodField()
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
        # return ProductCombinationSerializerForProductDetails(selected_product_combinations, many=True).data
        return ProductCombinationSerializerForVendorProductDetails(selected_product_combinations, many=True).data
