from django.template.loader import render_to_string
from product.serializers import BrandSerializer, CategorySerializer, DiscountTypeSerializer, ProductImageSerializer, ProductMediaSerializer, ProductReviewSerializer, ProductTagsSerializer, SubCategorySerializer, SubSubCategorySerializer, UnitSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ecommerce.common.emails import send_email_without_delay
from product.models import Brand, Category, Color, DiscountTypes, FlashDealProduct, Inventory, InventoryVariation, Product, ProductAttributeValues, ProductAttributes, ProductColor, ProductCombinations, ProductCombinationsVariants, ProductImages, ProductMedia, ProductReview, ProductTags, ProductVariation, ProductVideoProvider, ShippingClass, Specification, SpecificationValue, SubCategory, SubSubCategory, Tags, Units, VariantType, VatType
from user.models import User
# from user.serializers import UserRegisterSerializer
from vendor.models import VendorRequest, Vendor, StoreSettings, Seller
from django.db.models import Avg
from django.utils import timezone


# Seller Create serializer

class SellerSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(allow_null=True)

    class Meta:
        model = Seller
        fields = ['id', 'name', 'address', 'phone', 'email', 'logo', 'is_active']


# Seller Detail serializer
class SellerDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = ['id', 'name', 'email', 'address', 'phone', 'logo']




# Vendor Request serializer
class VendorRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorRequest
        fields = ['id', 'first_name', 'last_name', 'organization_name',
                  'email', 'vendor_type', 'nid', 'trade_license']
        read_only_field =['first_name', 'last_name', 'organization_name', 'email', 'vendor_type', 'nid', 'trade_license']
        # fields = ['id', 'email', 'organization_name', 'first_name', 'last_name', 'vendor_type', 'nid', 'trade_license']


# Vendor Create serializer
class VendorCreateSerializer(serializers.ModelSerializer):
    # is_verified = serializers.BooleanField(allow_null=True)
    # request_id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Vendor
        fields = ['id', 'name', 'address', 'vendor_admin',
                  'vendor_request', 'phone', 'email', 'logo']
        read_only_fields = ('organization_name', 'vendor_admin', 'vendor_request')

    # def create(self):
    #
    #
    #     return Vendor.objects.create()
        #     is_verified = validated_data.pop('is_verified')
    #     request_id = validated_data.pop('request_id')
    #     if is_verified is True:
    #         password = User.objects.make_random_password()
    #         vendor_request = VendorRequest.objects.get(id=request_id)
    #         vendor_request.is_verified = True
    #         vendor_request.save()
    #
    #         user = User.objects.create(username=vendor_request.email, email=vendor_request.email,
    #                                    first_name=vendor_request.first_name, last_name=vendor_request.last_name)
    #         user.set_password(password)
    #         user.save()
    #
    #         vendor_instance = Vendor.objects.create(organization_name=vendor_request.organization_name,
    #                                                 vendor_admin=user, vendor_request=vendor_request, password=password)
    #         if vendor_instance:
    #             email_list = user.email
    #             subject = "Your Account"
    #             html_message = render_to_string('vendor_email.html',
    #                                             {'username': user.first_name, 'email': user.email, 'password': password})
    #             send_email_without_delay(subject, html_message, email_list)
    #         return vendor_instance
    #     else:
    #         raise ValidationError("You should verify first to create a vendor")
# Vendor Detail serializer
class VendorDetailSerializer(serializers.ModelSerializer):
    # vendor_request = VendorRequestSerializer(read_only=True)
    # vendor_admin = UserRegisterSerializer(read_only=True)

    class Meta:
        model = Vendor
        fields = ['id', 'name', 'address', 'phone', 'email', 'organization_name', 'vendor_admin', 'facebook', 'twitter', 'instagram', 'youtube',
                  'vendor_request', 'logo', 'banner', 'linkedin', 'bio']
        read_only_fields = ('organization_name', 'vendor_admin', 'vendor_request')



# Organization Name serializer
class OrganizationNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorRequest
        fields = ['organization_name']



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


class VendorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "vendor category serializer"
        model = Category
        fields = ['id', 'title', 'ordering_number', 'type', 'banner', 'icon', 'filtering_attributes']
class VendorAddNewCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= True)
    ordering_number = serializers.CharField(required= True)
    class Meta:
        model = Category
        fields = ['id', 'title', 'ordering_number', 'type', 'banner', 'icon', 'filtering_attributes']

    def create(self, validated_data):
        # work with category title 
        title_get = validated_data.pop('title')
        title_get_data = title_get.lower()
        if title_get:
            title_get_for_check = Category.objects.filter(title=title_get.lower())
            if title_get_for_check:
                raise ValidationError('This category title already exist in Category.')

        # work with order number
        ordering_number_get = validated_data.pop('ordering_number')
        ordering_number_get_data = ordering_number_get.lower()
        if ordering_number_get:
            ordering_number_get_for_check = Category.objects.filter(ordering_number=ordering_number_get)
            if ordering_number_get_for_check:
                raise ValidationError('This category ordering number already exist in Category.')

        category_instance = Category.objects.create(**validated_data, title=title_get_data, ordering_number=ordering_number_get_data )
        return category_instance
class VendorUpdateCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= True)
    ordering_number = serializers.CharField(required= True)
    class Meta:
        model = Category
        fields = ['id', 'title', 'ordering_number', 'type', 'banner', 'icon', 'filtering_attributes', 'is_active']

    def update(self, instance, validated_data):
        # work with category title
        title_get = validated_data.pop('title')
        title_get_data = title_get.lower()
        if title_get:
            title_get_for_check = Category.objects.filter(title=title_get.lower())
            if title_get_for_check:
                raise ValidationError('This category title already exist in Category.')

        # work with order number
        ordering_number_get = validated_data.pop('ordering_number')
        ordering_number_get_data = ordering_number_get.lower()
        if ordering_number_get:
            ordering_number_get_for_check = Category.objects.filter(ordering_number=ordering_number_get)
            if ordering_number_get_for_check:
                raise ValidationError('This category ordering number already exist in Category.')

        validated_data.update({"updated_at": timezone.now(), "title":title_get_data, "ordering_number":ordering_number_get_data})
        return super().update(instance, validated_data)


class VendorSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'title', 'ordering_number', 'category']
class VendorAddNewSubCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= True)
    ordering_number = serializers.CharField(required= True)
    class Meta:
        model = SubCategory
        fields = ['id', 'title', 'ordering_number', 'category']

    def create(self, validated_data):
        # work with category title 
        title_get = validated_data.pop('title')
        title_get_data = title_get.lower()
        if title_get:
            title_get_for_check = SubCategory.objects.filter(title=title_get.lower())
            if title_get_for_check:
                raise ValidationError('This Sub category title already exist in Sub Category.')

        # work with order number
        ordering_number_get = validated_data.pop('ordering_number')
        ordering_number_get_data = ordering_number_get.lower()
        if ordering_number_get:
            ordering_number_get_for_check = SubCategory.objects.filter(ordering_number=ordering_number_get)
            if ordering_number_get_for_check:
                raise ValidationError('This Sub category ordering number already exist in SubCategory.')

        sub_category_instance = SubCategory.objects.create(**validated_data, title=title_get_data, ordering_number=ordering_number_get_data )
        return sub_category_instance
class VendorUpdateSubCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= True)
    ordering_number = serializers.CharField(required= True)
    class Meta:
        model = SubCategory
        fields = ['id', 'title', 'ordering_number', 'category', 'is_active']

    def update(self, instance, validated_data):
        # work with category title
        title_get = validated_data.pop('title')
        title_get_data = title_get.lower()
        if title_get:
            title_get_for_check = SubCategory.objects.filter(title=title_get.lower())
            if title_get_for_check:
                raise ValidationError('This Sub category title already exist in Sub Category.')

        # work with order number
        ordering_number_get = validated_data.pop('ordering_number')
        ordering_number_get_data = ordering_number_get.lower()
        if ordering_number_get:
            ordering_number_get_for_check = SubCategory.objects.filter(ordering_number=ordering_number_get)
            if ordering_number_get_for_check:
                raise ValidationError('This Sub category ordering number already exist in Sub Category.')

        validated_data.update({"updated_at": timezone.now(), "title":title_get_data, "ordering_number":ordering_number_get_data})
        return super().update(instance, validated_data)


class VendorSubSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSubCategory
        fields = ['id', 'title', 'ordering_number', 'category', 'sub_category', 'is_active']
class VendorAddNewSubSubCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= True)
    ordering_number = serializers.CharField(required= True)
    class Meta:
        model = SubSubCategory
        fields = ['id', 'title', 'ordering_number', 'category', 'sub_category']

    def create(self, validated_data):
        # work with category title 
        title_get = validated_data.pop('title')
        title_get_data = title_get.lower()
        if title_get:
            title_get_for_check = SubSubCategory.objects.filter(title=title_get.lower())
            if title_get_for_check:
                raise ValidationError('This Sub Sub category title already exist in Sub Sub Category.')

        # work with order number
        ordering_number_get = validated_data.pop('ordering_number')
        ordering_number_get_data = ordering_number_get.lower()
        if ordering_number_get:
            ordering_number_get_for_check = SubSubCategory.objects.filter(ordering_number=ordering_number_get)
            if ordering_number_get_for_check:
                raise ValidationError('This Sub Sub category ordering number already exist in Sub Sub Category.')

        sub_category_instance = SubSubCategory.objects.create(**validated_data, title=title_get_data, ordering_number=ordering_number_get_data )
        return sub_category_instance
class VendorUpdateSubSubCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= True)
    ordering_number = serializers.CharField(required= True)
    class Meta:
        model = SubSubCategory
        fields = ['id', 'title', 'ordering_number', 'category', 'sub_category', 'is_active']

    def update(self, instance, validated_data):
        # work with category title
        title_get = validated_data.pop('title')
        title_get_data = title_get.lower()
        if title_get:
            title_get_for_check = SubSubCategory.objects.filter(title=title_get.lower())
            if title_get_for_check:
                raise ValidationError('This Sub Sub category title already exist in Sub Sub Category.')

        # work with order number
        ordering_number_get = validated_data.pop('ordering_number')
        ordering_number_get_data = ordering_number_get.lower()
        if ordering_number_get:
            ordering_number_get_for_check = SubSubCategory.objects.filter(ordering_number=ordering_number_get)
            if ordering_number_get_for_check:
                raise ValidationError('This Sub Sub category ordering number already exist in Sub Sub Category.')

        validated_data.update({"updated_at": timezone.now(), "title":title_get_data, "ordering_number":ordering_number_get_data})
        return super().update(instance, validated_data)

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
    # product_media = ProductMediaSerializer(many=True, read_only=True)
    # category = CategorySerializer(read_only=True)
    # brand_name = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    # review_count = serializers.SerializerMethodField()
    # discount_type = serializers.CharField()

    vendor_organization_name = serializers.CharField(source="vendor.organization_name",read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'thumbnail',
            'title',
            'vendor_organization_name',
            'sell_count',
            'price',
            'avg_rating',
            'quantity',
            'low_stock_quantity_warning',
            'todays_deal',
            'is_published',
            'is_featured'
        ]

    # class Meta:
    #     model = Product
    #     fields = [
    #         'id',
    #         'title',
    #         'slug',
    #         'sku',
    #         'price',
    #         'old_price',
    #         'short_description',
    #         'total_quantity',
    #         'status',
    #         'is_featured',
    #         'category',
    #         'brand_name',
    #         'thumbnail',
    #         'product_media',
    #         'avg_rating',
    #         'review_count',
    #         'discount_type',
    #         'discount_amount'
    #     ]

    def get_avg_rating(self, obj):
        return obj.product_review_product.all().aggregate(Avg('rating_number'))['rating_number__avg']

    # def get_brand_name(self, obj):
    #     if obj.brand:
    #         get_brand = Brand.objects.get(id=obj.brand.id)
    #         return get_brand.title
    #     else:
    #         return obj.brand

    # def get_review_count(self, obj):
    #     re_count = ProductReview.objects.filter(
    #         product=obj, is_active=True).count()
    #     return re_count

# Product Combination serializer / Connect with ProductCreateSerializer


class ProductCombinationSerializer(serializers.ModelSerializer):
    # sku = serializers.CharField(required=False)
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

            # 'sku',
            'variant_type',
            'variant_value',
            'variant_price',
            'quantity',
            'discount_type',
            'discount_amount'
        ]

class ProductCombinationSerializerForVendorProductDetails(serializers.ModelSerializer):
    # sku = serializers.CharField(required=False)
    product_attribute = serializers.SerializerMethodField()
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

    def get_product_attribute(self, obj):
        try:
            product_attribute = ProductCombinations.objects.get(
                id=obj.id, is_active=True).product_attribute.title
            return product_attribute
        except:
            return ''

    def get_variant_type(self, obj):
        try:
            variant_type = ProductCombinationsVariants.objects.get(
                product_combination=obj, is_active=True).variant_type.title
            return variant_type
        except:
            return ''

    def get_variant_value(self, obj):
        try:
            variant_value = ProductCombinationsVariants.objects.get(
                product_combination=obj, is_active=True).variant_value
            return variant_value
        except:
            return ''

    def get_variant_price(self, obj):
        try:
            variant_price = ProductCombinationsVariants.objects.get(
                product_combination=obj, is_active=True).variant_price
            return variant_price
        except:
            return ''

    def get_quantity(self, obj):
        try:
            quantity = ProductCombinationsVariants.objects.get(
                product_combination=obj, is_active=True).quantity
            return quantity
        except:
            return ''

    def get_discount_type(self, obj):
        try:
            discount_type = ProductCombinationsVariants.objects.get(
                product_combination=obj, is_active=True).discount_type.title
            return discount_type
        except:
            return ''

    def get_discount_amount(self, obj):
        try:
            discount_amount = ProductCombinationsVariants.objects.get(
                product_combination=obj, is_active=True).discount_amount
            return discount_amount
        except:
            return ''

class ProductCombinationSerializerForVendorProductUpdate(serializers.ModelSerializer):
    product_attribute = serializers.SerializerMethodField()
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

    def get_product_attribute(self, obj):
        try:
            product_attribute = ProductCombinations.objects.get(
                id=obj.id, is_active=True).product_attribute.id
            return product_attribute
        except:
            return ''

    def get_variant_type(self, obj):
        try:
            variant_type = ProductCombinationsVariants.objects.get(
                product_combination=obj, is_active=True).variant_type.id
            return variant_type
        except:
            return ''

    def get_variant_value(self, obj):
        try:
            variant_value = ProductCombinationsVariants.objects.get(
                product_combination=obj, is_active=True).variant_value
            return variant_value
        except:
            return ''

    def get_variant_price(self, obj):
        try:
            variant_price = ProductCombinationsVariants.objects.get(
                product_combination=obj, is_active=True).variant_price
            return variant_price
        except:
            return ''

    def get_quantity(self, obj):
        try:
            quantity = ProductCombinationsVariants.objects.get(
                product_combination=obj, is_active=True).quantity
            return quantity
        except:
            return ''

    def get_discount_type(self, obj):
        try:
            discount_type = ProductCombinationsVariants.objects.get(
                product_combination=obj, is_active=True).discount_type.id
            return discount_type
        except:
            return ''

    def get_discount_amount(self, obj):
        try:
            discount_amount = ProductCombinationsVariants.objects.get(
                product_combination=obj, is_active=True).discount_amount
            return discount_amount
        except:
            return ''

class ProductAttributeValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValues
        fields = [
            'id',
            'value'
        ]

class ProductAttributesSerializer(serializers.ModelSerializer):
    product_attribute_values = ProductAttributeValuesSerializer(
        many=True, required=False)
    class Meta:
        model = ProductAttributes
        fields = [
            'id',
            'attribute',
            'product_attribute_values'
        ]

class ProductVariantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = [
            'id',
            'variation',
            'variation_price',
            'sku',
            'quantity',
            'image'
        ]

class SpecificationValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationValue
        fields = [
            'id',
            'key',
            'value'
        ]

class VatTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VatType
        fields = [
            'id',
            'title'
        ]

class ProductSpecificationSerializer(serializers.ModelSerializer):
    specification_values = SpecificationValuesSerializer(
        many=True, required=False)
    class Meta:
        model = Specification
        fields = [
            'id',
            'title',
            'specification_values'
        ]

class FlashDealSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashDealProduct
        fields = [
            'id',
            'flashDealInfo',
            'discount_amount',
            'discount_type'
        ]

class VendorProductCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=False, write_only=True, required= True)
    sub_category = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), many=False, write_only=True, required= False)
    sub_sub_category = serializers.PrimaryKeyRelatedField(queryset=SubSubCategory.objects.all(), many=False, write_only=True, required= False)
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), many=False, write_only=True, required= False)
    unit = serializers.PrimaryKeyRelatedField(queryset=Units.objects.all(), many=False, write_only=True, required= False)
    minimum_purchase_quantity = serializers.IntegerField(required=True)
    price = serializers.FloatField(required=True)
    quantity = serializers.IntegerField(required=False, write_only=True)
    vat_type = VatTypeSerializer(many=False, required=False)
    shipping_class = serializers.PrimaryKeyRelatedField(queryset=ShippingClass.objects.all(), many=False, write_only=True, required= False)

    product_tags = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=True)
    product_images = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False)
    product_colors = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Color.objects.all()), write_only=True, required=False)
    product_attributes = ProductAttributesSerializer(
        many=True, required=False)
    product_variants = ProductVariantsSerializer(many=True, required=False)
    product_specification = ProductSpecificationSerializer(
        many=True, required=False)
    flash_deal = FlashDealSerializer(many=False, required=False)

    

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'category',
            'sub_category',
            'sub_sub_category',
            'brand',
            'vendor',
            'unit',
            'minimum_purchase_quantity',
            'product_tags',
            'bar_code',
            'refundable',
            'product_images',
            'thumbnail',
            'video_provider',
            'video_link',
            'product_colors',
            'product_attributes',
            'price',
            'pre_payment_amount',
            'discount_start_date',
            'discount_end_date',
            'discount_amount',
            'discount_type',
            'quantity',
            'sku',
            'external_link',
            'external_link_button_text',
            'product_variants',
            'full_description',
            'active_short_description',
            'short_description',
            'product_specification',
            'low_stock_quantity_warning',
            'show_stock_quantity',
            'cash_on_delivery',
            'is_featured',
            'todays_deal',
            'flash_deal',
            'shipping_time',
            'shipping_class',
            'vat',
            'vat_type'
        ]

        read_only_fields = ('slug', 'sell_count')

    def create(self, validated_data):
        # validation for sku start
        try:
            sku = validated_data["sku"]
        except:
            sku = ''

        if sku:
            product_check_sku = Product.objects.filter(sku=sku)
            if product_check_sku:
                raise ValidationError('This SKU already exist in product.')
            variation_check_sku = ProductVariation.objects.filter(sku=sku)
            if variation_check_sku:
                raise ValidationError('This SKU already exist in product variation.')
        # validation for sku end

        # validation for category sub category and sub sub category start
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
        # validation for category sub category and sub sub category end

        # product_tags
        try:
            product_tags = validated_data.pop('product_tags')
        except:
            product_tags = ''

        # product_images
        try:
            product_images = validated_data.pop('product_images')
        except:
            product_images = ''

        # product_colors
        try:
            product_colors = validated_data.pop('product_colors')
        except:
            product_colors = ''

        # product_attributes
        try:
            product_attributes = validated_data.pop('product_attributes')
        except:
            product_attributes = ''

        # product_variants
        try:
            product_variants = validated_data.pop('product_variants')
        except:
            product_variants = ''

        # product_specification
        try:
            product_specification = validated_data.pop('product_specification')
        except:
            product_specification = ''

        # flash_deal
        try:
            flash_deal = validated_data.pop('flash_deal')
        except:
            flash_deal = ''


        # product_instance = Product.objects.create(**validated_data, vendor=Vendor.objects.get(vendor_admin=User.objects.get(
            # id=self.context['request'].user.id)))
        product_instance = Product.objects.create(**validated_data)

        try:
            # tags
            if product_tags:
                for tag in product_tags:
                    tag_s = tag.lower()
                    if Tags.objects.filter(title=tag_s).exists():
                        tag_obj = Tags.objects.get(title=tag_s)
                        try:
                            ProductTags.objects.create(
                                tag=tag_obj, product=product_instance)
                        except:
                            pass
                    else:
                        tag_instance = Tags.objects.create(title=tag_s)
                        try:
                            ProductTags.objects.create(
                                tag=tag_instance, product=product_instance)
                        except:
                            pass

            # product_images
            if product_images:
                for media_file in product_images:
                    ProductImages.objects.create(
                        product=product_instance, file=media_file, status="COMPLETE")

            # product_colors
            if product_colors:
                for color in product_colors:
                    if Color.objects.filter(title=color).exists():
                        color_obj = Color.objects.get(title=color)
                        if color_obj:
                            ProductColor.objects.create(
                                color=color_obj, product=product_instance)
                        else:
                            pass
                    else:
                        pass

            # product_attributes
            if product_attributes:
                for product_attribute in product_attributes:
                    attribute_attribute = product_attribute['attribute']
                    if product_instance and attribute_attribute:
                        product_attributes_instance = ProductAttributes.objects.create(attribute=attribute_attribute, product=product_instance)
                    product_attribute_values = product_attribute['product_attribute_values']
                    for product_attribute_value in product_attribute_values:
                        attribute_value_value = product_attribute_value['value']
                        product_attributes_value_instance = ProductAttributeValues.objects.create(product_attribute = product_attributes_instance, value= attribute_value_value, product=product_instance)

            # product with out variants
            single_quantity = validated_data["quantity"]
            total_quan = 0
            if single_quantity:
                total_quan += single_quantity
                Product.objects.filter(id=product_instance.id).update(total_quantity=total_quan)
                # inventory update
                Inventory.objects.create(product=product_instance, initial_quantity=single_quantity, current_quantity=single_quantity)
            
            # product with variants
            if product_variants:
                variation_total_quan = 0
                for product_variant in product_variants:
                    attribute = product_variant['attribute']
                    variation = product_variant['variation']
                    variation_price = product_variant['variation_price']
                    sku = product_variant['sku']
                    if sku:
                        product_check_sku = Product.objects.filter(sku=sku)
                        if product_check_sku:
                            raise ValidationError('This SKU already exist in product.')
                        variation_check_sku = ProductVariation.objects.filter(sku=sku)
                        if variation_check_sku:
                            raise ValidationError('This SKU already exist in product variation.')

                    variant_quantity = product_variant['quantity']
                    if variant_quantity:
                        variation_total_quan += variant_quantity
                        Product.objects.filter(id=product_instance.id).update(total_quantity=variation_total_quan)


                    v_image = product_variant['image']

                    if attribute and variation and variation_price and sku and variant_quantity and v_image:
                        total_price = float(variation_price) * float(variant_quantity)
                        product_variation_instance = ProductVariation.objects.create(product=product_instance, attribute=attribute,
                        variation=variation, variation_price=variation_price, sku=sku, quantity=variant_quantity, image=v_image, total_price=total_price)

                        # inventory update
                        if variation_total_quan:
                            if variation_total_quan != 0:
                                inventory_instance = Inventory.objects.create(product=product_instance)
                                inventory_variation_instance = InventoryVariation.objects.create(inventory=inventory_instance, variation_initial_quantity=variation_total_quan, variation_current_quantity=variation_total_quan)

            # product_specification
            if product_specification:
                for p_specification in product_specification:
                    s_title = p_specification['title']
                    if s_title:
                        specification_instance = Specification.objects.create(
                        title=s_title, product=product_instance)
                    specification_values = p_specification['specification_values']
                    for specification_value in specification_values:
                        key = specification_value['key']
                        value = specification_value['value']
                        product_specification_instance = SpecificationValue.objects.create(specification = specification_instance, key=key, value= value)

            # flash_deal
            if flash_deal:
                for f_deal in flash_deal:
                    flashDealInfo = f_deal['flashDealInfo']
                    discount_type = f_deal['discount_type']
                    discount_amount = f_deal['discount_amount']
                    if s_title:
                        flash_deal_product_instance = FlashDealProduct.objects.create(product=product_instance, flashDealInfo=flashDealInfo, discount_type=discount_type, discount_amount=discount_amount)

            return product_instance
        except:
            return product_instance

class VendorProductViewSerializer(serializers.ModelSerializer):
    product_images = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    product_attributes =serializers.SerializerMethodField('get_product_attributes')
    product_variants = serializers.SerializerMethodField('get_product_variants')
    product_specification = serializers.SerializerMethodField('get_product_specification')
    product_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'product_images',
            'title',
            'avg_rating',
            'review_count',
            'in_house_product',
            'digital',
            'price',
            'colors',
            'product_attributes',
            'quantity',
            'product_variants',
            'refundable',
            'full_description',
            'product_specification',
            'product_reviews'
        ]

    def get_product_images(self, obj):
        try:
            queryset = ProductImages.objects.filter(
                product=obj, is_active=True).distinct()
            serializer = ProductImageSerializer(instance=queryset, many=True, context={
                                                'request': self.context['request']})
            return serializer.data
        except:
            return []

    def get_avg_rating(self, ob):
        return ob.product_review_product.all().aggregate(Avg('rating_number'))['rating_number__avg']

    def get_review_count(self, obj):
        re_count = ProductReview.objects.filter(
            product=obj, is_active=True).count()
        return re_count

    def get_colors(self, obj):
        color_list = []
        try:
            selected_colors = ProductColor.objects.filter(
                product=obj, is_active=True).distinct()
            for s_c in selected_colors:
                color_title = s_c.color.title
                color_list.append(color_title)
            return color_list
        except:
            return color_list

    def get_product_attributes(self, product):
        queryset = ProductAttributes.objects.filter(product=product, is_active = True)
        serializer = ProductAttributesSerializer(instance=queryset, many=True)
        return serializer.data

    def get_product_variants(self, product):
        queryset = ProductVariation.objects.filter(product=product, is_active = True)
        serializer = ProductVariantsSerializer(instance=queryset, many=True)
        return serializer.data

    def get_product_specification(self, product):
        queryset = Specification.objects.filter(product=product, is_active = True)
        serializer = ProductSpecificationSerializer(instance=queryset, many=True)
        return serializer.data

    def get_product_reviews(self, obj):
        selected_product_reviews = ProductReview.objects.filter(
            product=obj, is_active=True).distinct()
        return ProductReviewSerializer(selected_product_reviews, many=True).data

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
        queryset = ProductMedia.objects.filter(
            product=obj, is_active=True).distinct()
        serializer = ProductMediaSerializer(instance=queryset, many=True, context={
                                            'request': self.context['request']})
        return serializer.data

    def get_product_combinations(self, obj):
        selected_product_combinations = ProductCombinations.objects.filter(
            product=obj, is_active=True).distinct()
        return ProductCombinationSerializerForVendorProductDetails(selected_product_combinations, many=True).data
    
class VendorProductUpdateSerializer(serializers.ModelSerializer):
    product_category_name = serializers.SerializerMethodField()
    product_sub_category_name = serializers.SerializerMethodField()
    product_sub_sub_category_name = serializers.SerializerMethodField()
    product_brand_name = serializers.SerializerMethodField()
    existing_product_tags = serializers.SerializerMethodField()
    product_tags = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False)
    existing_product_images = serializers.SerializerMethodField()
    product_images = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False)
    existing_colors = serializers.SerializerMethodField()
    product_colors = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False)
    existing_product_attributes =serializers.SerializerMethodField('get_product_attributes')
    product_attributes = ProductAttributesSerializer(
        many=True, required=False)
    existing_product_variants = serializers.SerializerMethodField('get_product_variants')
    product_variants = ProductVariantsSerializer(
        many=True, required=False)
    existing_product_specification = serializers.SerializerMethodField('get_product_specification')
    product_specification = ProductSpecificationSerializer(
        many=True, required=False)
    flash_deal = FlashDealSerializer(
        many=False, required=False)
    quantity = serializers.IntegerField(required=False, write_only=True)
    vat_type = VatTypeSerializer(
        many=False, required=False)
    existing_flash_deal = serializers.SerializerMethodField('get_flash_deal')
    class Meta:
        model = Product
        fields =[
                    'id',
                    'title',
                    'product_category_name',
                    'category',
                    'product_sub_category_name',
                    'sub_category',
                    'product_sub_sub_category_name',
                    'sub_sub_category',
                    'product_brand_name',
                    'brand',
                    'vendor',
                    'unit',
                    'minimum_purchase_quantity',
                    'existing_product_tags',
                    'product_tags',
                    'bar_code',
                    'refundable',
                    'existing_product_images',
                    'product_images',
                    'thumbnail',
                    'video_provider',
                    'video_link',
                    'existing_colors',
                    'product_colors',
                    'existing_product_attributes',
                    'product_attributes',
                    'price',
                    'pre_payment_amount',
                    'discount_start_date',
                    'discount_end_date',
                    'discount_amount',
                    'discount_type',
                    'quantity',
                    'sku',
                    'external_link',
                    'external_link_button_text',
                    'existing_product_variants',
                    'product_variants',
                    'full_description',
                    'active_short_description',
                    'short_description',
                    'existing_product_specification',
                    'product_specification',
                    'low_stock_quantity_warning',
                    'show_stock_quantity',
                    'cash_on_delivery',
                    'is_featured',
                    'todays_deal',
                    'existing_flash_deal',
                    'flash_deal',
                    'shipping_time',
                    'shipping_class',
                    'vat',
                    'vat_type'
                ]

    def get_product_category_name(self, obj):
        try:
            get_cat=Category.objects.get(id= obj.category.id)
            return get_cat.title
        except:
            return ''

    def get_product_sub_category_name(self, obj):
        try:
            get_sub_cat=SubCategory.objects.get(id= obj.sub_category.id)
            return get_sub_cat.title
        except:
            return ''

    def get_product_sub_sub_category_name(self, obj):
        try:
            get_sub_sub_cat=SubSubCategory.objects.get(id= obj.sub_sub_category.id)
            return get_sub_sub_cat.title
        except:
            return ''

    def get_product_brand_name(self, obj):
        try:
            get_brand=Brand.objects.get(id= obj.brand.id)
            return get_brand.title
        except:
            return ''

    def get_existing_product_tags(self, obj):
        tags_list = []
        try:
            selected_product_tags = ProductTags.objects.filter(
                product=obj, is_active=True).distinct()
            for s_p_t in selected_product_tags:
                tag_title = s_p_t.tag.title
                tags_list.append(tag_title)
            return tags_list
        except:
            return tags_list

    def get_existing_product_images(self, obj):
        try:
            queryset = ProductImages.objects.filter(
                product=obj, is_active=True).distinct()
            serializer = ProductImageSerializer(instance=queryset, many=True, context={
                                                'request': self.context['request']})
            return serializer.data
        except:
            return []

    def get_existing_colors(self, obj):
        color_list = []
        try:
            selected_colors = ProductColor.objects.filter(
                product=obj, is_active=True).distinct()
            for s_c in selected_colors:
                color_title = s_c.color.title
                color_list.append(color_title)
            return color_list
        except:
            return color_list

    def get_product_attributes(self, product):
        queryset = ProductAttributes.objects.filter(product=product, is_active = True)
        serializer = ProductAttributesSerializer(instance=queryset, many=True)
        return serializer.data

    def get_product_variants(self, product):
        queryset = ProductVariation.objects.filter(product=product, is_active = True)
        serializer = ProductVariantsSerializer(instance=queryset, many=True)
        return serializer.data

    def get_product_specification(self, product):
        queryset = Specification.objects.filter(product=product, is_active = True)
        serializer = ProductSpecificationSerializer(instance=queryset, many=True)
        return serializer.data

    def get_flash_deal(self, product):
        queryset = FlashDealProduct.objects.filter(product=product, is_active = True)
        serializer = FlashDealSerializer(instance=queryset, many=True)
        return serializer.data


    def update(self, instance, validated_data):
        # validation for sku start
        try:
            sku = validated_data["sku"]
        except:
            sku = ''

        if sku:
            product_check_sku = Product.objects.filter(sku=sku)
            if product_check_sku:
                raise ValidationError('This SKU already exist in product.')
            variation_check_sku = ProductVariation.objects.filter(sku=sku)
            if variation_check_sku:
                raise ValidationError('This SKU already exist in product variation.')
        # validation for sku end

        # validation for category sub category and sub sub category start
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
        # validation for category sub category and sub sub category end

        # product_tags
        try:
            product_tags = validated_data.pop('product_tags')
        except:
            product_tags = ''

        # product_images
        try:
            product_images = validated_data.pop('product_images')
        except:
            product_images = ''

        # product_colors
        try:
            product_colors = validated_data.pop('product_colors')
        except:
            product_colors = ''

        # product_attributes
        try:
            product_attributes = validated_data.pop('product_attributes')
        except:
            product_attributes = ''

        # product_variants
        try:
            product_variants = validated_data.pop('product_variants')
        except:
            product_variants = ''

        # product_specification
        try:
            product_specification = validated_data.pop('product_specification')
        except:
            product_specification = ''

        # flash_deal
        try:
            flash_deal = validated_data.pop('flash_deal')
        except:
            flash_deal = ''


        try:
            # tags
            if product_tags:
                ProductTags.objects.filter(product=instance).delete()
                for tag in product_tags:
                    tag_s = tag.lower()
                    if Tags.objects.filter(title=tag_s).exists():
                        tag_obj = Tags.objects.get(title=tag_s)
                        try:
                            ProductTags.objects.create(
                                tag=tag_obj, product=instance)
                        except:
                            pass
                    else:
                        tag_instance = Tags.objects.create(title=tag_s)
                        try:
                            ProductTags.objects.create(
                                tag=tag_instance, product=instance)
                        except:
                            pass
            else:
                ProductTags.objects.filter(product=instance).delete()

            # product_images
            if product_images:
                for image in product_images:
                    ProductImages.objects.create(
                        product=instance, image=image, status="COMPLETE")

            # product_colors
            if product_colors:
                ProductColor.objects.filter(product=instance).delete()
                for color in product_colors:
                    if Color.objects.filter(title=color).exists():
                        color_obj = Color.objects.get(title=color)
                        if color_obj:
                            ProductColor.objects.create(
                                color=color_obj, product=instance)
                        else:
                            pass
                    else:
                        pass
            else:
                ProductColor.objects.filter(product=instance).delete()

            # product_attributes
            if product_attributes:
                p_a = ProductAttributes.objects.filter(
                    product=instance).exists()
                if p_a:
                    ProductAttributes.objects.filter(
                        product=instance).delete()
                p_a_v = ProductAttributeValues.objects.filter(
                    product=instance).exists()
                if p_a_v:
                    ProductAttributeValues.objects.filter(
                        product=instance).delete()

                for product_attribute in product_attributes:
                    attribute_title = product_attribute['title']
                    attribute_attribute = product_attribute['attribute']
                    if instance and attribute_title and attribute_attribute:
                        product_attributes_instance = ProductAttributes.objects.create(
                        title=attribute_title, attribute=attribute_attribute, product=instance)
                    product_attribute_values = product_attribute['product_attribute_values']
                    for product_attribute_value in product_attribute_values:
                        attribute_value_value = product_attribute_value['value']
                        product_combination_instance = ProductAttributeValues.objects.create(product_attribute = product_attributes_instance, value= attribute_value_value)

            # # inventory update start
            # single_quantity = validated_data["quantity"]
            # total_quan = Product.objects.get(id=instance.id).total_quantity
            # if single_quantity:
            #     total_quan += single_quantity
            #     Product.objects.filter(id=instance.id).update(total_quantity=total_quan)

            # product with out variants
            single_quantity = validated_data["quantity"]
            quan = Product.objects.get(id=instance.id).quantity
            total_quan = Product.objects.get(id=instance.id).total_quantity
            if single_quantity:
                quan += single_quantity
                total_quan += single_quantity
                # inventory update
                Inventory.objects.create(product=instance, initial_quantity=single_quantity, current_quantity=single_quantity)

                Product.objects.filter(id=instance.id).update(quantity=quan, total_quantity=total_quan)


            # product with variants
            if product_variants:
                variation_total_quan = Product.objects.get(id=instance.id).total_quantity
                for product_variant in product_variants:
                    attribute = product_variant['attribute']
                    variation = product_variant['variation']
                    variation_price = product_variant['variation_price']
                    sku = product_variant['sku']
                    if sku:
                        product_check_sku = Product.objects.filter(sku=sku)
                        if product_check_sku:
                            raise ValidationError('This SKU already exist in product.')
                        variation_check_sku = ProductVariation.objects.filter(sku=sku)
                        if variation_check_sku:
                            raise ValidationError('This SKU already exist in product variation.')

                    variant_quantity = product_variant['quantity']
                    if variant_quantity:
                        variation_total_quan += variant_quantity
                        Product.objects.filter(id=instance.id).update(total_quantity=variation_total_quan)


                    v_image = product_variant['image']

                    if attribute and variation and variation_price and sku and variant_quantity and v_image:
                        total_price = float(variation_price) * float(variant_quantity)
                        product_variation_instance = ProductVariation.objects.create(product=instance, attribute=attribute,
                        variation=variation, variation_price=variation_price, sku=sku, quantity=variant_quantity, image=v_image, total_price=total_price)

                        # inventory update
                        if variation_total_quan:
                            if variation_total_quan != 0:
                                inventory_instance = Inventory.objects.create(product=instance)
                                inventory_variation_instance = InventoryVariation.objects.create(inventory=inventory_instance, variation_initial_quantity=variation_total_quan, variation_current_quantity=variation_total_quan)

            # product_specification
            if product_specification:
                s = Specification.objects.filter(
                    product=instance).exists()
                if s:
                    Specification.objects.filter(
                        product=instance).delete()
                s_v= SpecificationValue.objects.filter(
                    product=instance).exists()
                if s_v:
                    SpecificationValue.objects.filter(
                        product=instance).delete()

                for p_specification in product_specification:
                    s_title = p_specification['title']
                    if s_title:
                        specification_instance = Specification.objects.create(
                        title=s_title, product=instance)
                    specification_values = p_specification['specification_values']
                    for specification_value in specification_values:
                        key = specification_value['key']
                        value = specification_value['value']
                        product_combination_instance = SpecificationValue.objects.create(specification = specification_instance, key=key, value= value)

            # flash_deal
            if flash_deal:
                f_p = FlashDealProduct.objects.filter(
                    product=instance).exists()
                if f_p:
                    FlashDealProduct.objects.filter(
                        product=instance).delete()

                for f_deal in flash_deal:
                    flashDealInfo = f_deal['flashDealInfo']
                    discount_type = f_deal['discount_type']
                    discount_amount = f_deal['discount_amount']
                    if s_title:
                        flash_deal_product_instance = FlashDealProduct.objects.create(product=instance, flashDealInfo=flashDealInfo, discount_type=discount_type, discount_amount=discount_amount)

            validated_data.update(
                {"updated_at": timezone.now()})
            return super().update(instance, validated_data)
        except:
            validated_data.update({"updated_at": timezone.now()})
            return super().update(instance, validated_data)

class ProductVideoProviderSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "product video provider serializer"
        model = ProductVideoProvider
        fields = ['id', 'title']

class ProductVatProviderSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "product vat provider serializer"
        model = VatType
        fields = ['id', 'title']



# class VendorProductCreateSerializer(serializers.ModelSerializer):
#     product_tags = serializers.ListField(
#         child=serializers.CharField(), write_only=True, required=False)
#     product_media = serializers.ListField(
#         child=serializers.FileField(), write_only=True, required=False)
#     product_combinations = ProductCombinationSerializer(
#         many=True, required=False)

#     class Meta:
#         model = Product
#         fields = [
#             'id',
#             'title',
#             'sku',
#             'warranty',
#             'short_description',
#             'full_description',
#             'category',
#             'sub_category',
#             'sub_sub_category',
#             'brand',
#             'unit',
#             'price',
#             'purchase_price',
#             'tax_in_percent',
#             'discount_type',
#             'discount_amount',
#             'total_quantity',
#             'shipping_cost',
#             'shipping_cost_multiply',
#             'shipping_time',
#             'thumbnail',
#             'youtube_link',
#             'product_media',
#             'product_tags',
#             'product_combinations'
#         ]

#         read_only_fields = ('slug', 'is_featured', 'old_price',
#                             'total_shipping_cost', 'sell_count')

#     def create(self, validated_data):
#         # validation for sku start
#         try:
#             sku = validated_data["sku"]
#         except:
#             sku = ''

#         if sku:
#             check_sku = Product.objects.filter(sku=sku)
#             if check_sku:
#                 raise ValidationError('This SKU already exist.')
#         # validation for sku end

#         # validation for sub category and sub sub category start
#         try:
#             category_id = validated_data["category"].id
#         except:
#             category_id = ''

#         try:
#             sub_category = validated_data["sub_category"].id
#         except:
#             sub_category = ''

#         if sub_category:
#             check_sub_category = SubCategory.objects.filter(
#                 id=sub_category, category=category_id)
#             if not check_sub_category:
#                 raise ValidationError(
#                     'This Sub category is not under your selected parent category.')

#         try:
#             sub_sub_category = validated_data["sub_sub_category"].id
#         except:
#             sub_sub_category = ''

#         if sub_sub_category:
#             check_sub_sub_category = SubSubCategory.objects.filter(
#                 id=sub_sub_category, sub_category=sub_category, category=category_id)
#             if not check_sub_sub_category:
#                 raise ValidationError(
#                     'This Sub Sub category is not under your selected parent category.')
#         # validation for sub category and sub sub category end

#         try:
#             product_media = validated_data.pop('product_media')
#         except:
#             product_media = ''

#         try:
#             product_tags = validated_data.pop('product_tags')
#         except:
#             product_tags = ''

#         try:
#             product_combinations = validated_data.pop('product_combinations')
#         except:
#             product_combinations = ''

#         product_instance = Product.objects.create(**validated_data, vendor=Vendor.objects.get(vendor_admin=User.objects.get(
#             id=self.context['request'].user.id)))

#         try:
#             if product_media:
#                 for media_file in product_media:
#                     ProductMedia.objects.create(
#                         product=product_instance, file=media_file, status="COMPLETE")

#             if product_tags:
#                 for tag in product_tags:
#                     tag_s = tag.lower()
#                     if Tags.objects.filter(title=tag_s).exists():
#                         tag_obj = Tags.objects.get(title=tag_s)
#                         try:
#                             ProductTags.objects.create(
#                                 tag=tag_obj, product=product_instance)
#                         except:
#                             pass
#                     else:
#                         tag_instance = Tags.objects.create(title=tag_s)
#                         try:
#                             ProductTags.objects.create(
#                                 tag=tag_instance, product=product_instance)
#                         except:
#                             pass

#             if product_combinations:
#                 for product_combination in product_combinations:
#                     product_attribute = product_combination['product_attribute']
#                     product_attribute_value = product_combination['product_attribute_value']
#                     product_attribute_color_code = product_combination['product_attribute_color_code']
#                     product_combination_instance = ProductCombinations.objects.create(
#                         product_attribute=product_attribute, product_attribute_value=product_attribute_value, product_attribute_color_code=product_attribute_color_code, product=product_instance)

#                     variant_type = product_combination['variant_type']
#                     variant_value = product_combination['variant_value']
#                     variant_price = product_combination['variant_price']
#                     quantity = product_combination['quantity']
#                     try:
#                         discount_type = product_combination['discount_type']
#                     except:
#                         discount_type = ''

#                     try:
#                         discount_amount = product_combination['discount_amount']
#                     except:
#                         discount_amount = ''
#                     ProductCombinationsVariants.objects.create(
#                         variant_type=variant_type,  variant_value=variant_value, variant_price=variant_price, quantity=quantity, discount_type=discount_type, discount_amount=discount_amount, product=product_instance, product_combination=product_combination_instance)
#             return product_instance
#         except:
#             return product_instance


# class VendorProductListSerializer(serializers.ModelSerializer):
#     product_media = ProductMediaSerializer(many=True, read_only=True)
#     category = CategorySerializer(read_only=True)
#     brand_name = serializers.SerializerMethodField()
#     avg_rating = serializers.SerializerMethodField()
#     review_count = serializers.SerializerMethodField()
#     discount_type = serializers.CharField()

#     class Meta:
#         model = Product
#         fields = [
#             'id',
#             'title',
#             'slug',
#             'sku',
#             'price',
#             'old_price',
#             'short_description',
#             'total_quantity',
#             'status',
#             'is_featured',
#             'category',
#             'brand_name',
#             'thumbnail',
#             'product_media',
#             'avg_rating',
#             'review_count',
#             'discount_type',
#             'discount_amount'
#         ]

#     def get_avg_rating(self, obj):
#         return obj.product_review_product.all().aggregate(Avg('rating_number'))['rating_number__avg']

#     def get_brand_name(self, obj):
#         if obj.brand:
#             get_brand = Brand.objects.get(id=obj.brand.id)
#             return get_brand.title
#         else:
#             return obj.brand

#     def get_review_count(self, obj):
#         re_count = ProductReview.objects.filter(
#             product=obj, is_active=True).count()
#         return re_count


# class VendorProductUpdateSerializer(serializers.ModelSerializer):
#     tags = serializers.SerializerMethodField()
#     product_tags = serializers.ListField(
#         child=serializers.CharField(), write_only=True, required=False)
#     media = serializers.SerializerMethodField()
#     product_media = serializers.ListField(
#         child=serializers.FileField(), write_only=True, required=False)
#     combinations = serializers.SerializerMethodField()
#     product_combinations = ProductCombinationSerializer(
#         many=True, required=False)

#     class Meta:
#         model = Product
#         fields = ['id',
#                   'title',
#                   'sku',
#                   'warranty',
#                   'short_description',
#                   'full_description',
#                   'category',
#                   'sub_category',
#                   'sub_sub_category',
#                   'brand',
#                   'unit',
#                   'price',
#                   'purchase_price',
#                   'tax_in_percent',
#                   'discount_type',
#                   'discount_amount',
#                   'total_quantity',
#                   'shipping_cost',
#                   'shipping_cost_multiply',
#                   'shipping_time',
#                   'thumbnail',
#                   'youtube_link',
#                   'tags',
#                   'product_tags',
#                   'media',
#                   'product_media',
#                   'combinations',
#                   'product_combinations'
#                   ]

#     def get_tags(self, obj):
#         tags_list = []
#         try:
#             selected_product_tags = ProductTags.objects.filter(
#                 product=obj, is_active=True).distinct()
#             for s_p_t in selected_product_tags:
#                 tag_title = s_p_t.tag.title
#                 tags_list.append(tag_title)
#             return tags_list
#         except:
#             return tags_list

#     def get_media(self, obj):
#         queryset = ProductMedia.objects.filter(
#             product=obj, is_active=True).distinct()
#         serializer = ProductMediaSerializer(instance=queryset, many=True, context={
#                                             'request': self.context['request']})
#         return serializer.data

#     def get_combinations(self, obj):
#         selected_product_combinations = ProductCombinations.objects.filter(
#             product=obj, is_active=True).distinct()
#         return ProductCombinationSerializerForVendorProductUpdate(selected_product_combinations, many=True).data

#     def update(self, instance, validated_data):
#         # validation for sku start
#         try:
#             sku = validated_data["sku"]
#         except:
#             sku = ''

#         if sku:
#             check_sku = Product.objects.filter(sku=sku)
#             if check_sku:
#                 if int(check_sku[0].id) == int(instance.id):
#                     pass
#                 elif int(check_sku[0].id) != int(instance.id):
#                     raise ValidationError('This SKU already exist.')
#                 else:
#                     pass
#         # validation for sku end

#         # validation for sub category and sub sub category start
#         try:
#             category_id = validated_data["category"].id
#         except:
#             category_id = ''

#         try:
#             sub_category = validated_data["sub_category"].id
#         except:
#             sub_category = ''

#         if sub_category:
#             check_sub_category = SubCategory.objects.filter(
#                 id=sub_category, category=category_id)
#             if not check_sub_category:
#                 raise ValidationError(
#                     'This Sub category is not under your selected parent category.')

#         try:
#             sub_sub_category = validated_data["sub_sub_category"].id
#         except:
#             sub_sub_category = ''

#         if sub_sub_category:
#             check_sub_sub_category = SubSubCategory.objects.filter(
#                 id=sub_sub_category, sub_category=sub_category, category=category_id)
#             if not check_sub_sub_category:
#                 raise ValidationError(
#                     'This Sub Sub category is not under your selected parent category.')
#         # validation for sub category and sub sub category end

#         try:
#             product_tags = validated_data.pop('product_tags')
#         except:
#             product_tags = ''

#         try:
#             product_media = validated_data.pop('product_media')
#         except:
#             product_media = ''

#         try:
#             product_combinations = validated_data.pop('product_combinations')
#         except:
#             product_combinations = ''

#         try:
#             if product_tags:
#                 ProductTags.objects.filter(product=instance).delete()
#                 for tag in product_tags:
#                     tag_s = tag.lower()
#                     if Tags.objects.filter(title=tag_s).exists():
#                         tag_obj = Tags.objects.get(title=tag_s)
#                         try:
#                             ProductTags.objects.create(
#                                 tag=tag_obj, product=instance)
#                         except:
#                             pass
#                     else:
#                         tag_instance = Tags.objects.create(title=tag_s)
#                         try:
#                             ProductTags.objects.create(
#                                 tag=tag_instance, product=instance)
#                         except:
#                             pass
#             else:
#                 ProductTags.objects.filter(product=instance).delete()

#             if product_media:
#                 for media_file in product_media:
#                     ProductMedia.objects.create(
#                         product=instance, file=media_file, status="COMPLETE")

#             if product_combinations:
#                 p_c_v = ProductCombinationsVariants.objects.filter(
#                     product=instance).exists()
#                 if p_c_v:
#                     ProductCombinationsVariants.objects.filter(
#                         product=instance).delete()
#                 p_c = ProductCombinations.objects.filter(
#                     product=instance).exists()
#                 if p_c:
#                     ProductCombinations.objects.filter(
#                         product=instance).delete()

#                 for product_combination in product_combinations:
#                     product_attribute = product_combination['product_attribute']
#                     product_attribute_value = product_combination['product_attribute_value']
#                     product_attribute_color_code = product_combination['product_attribute_color_code']
#                     product_combination_instance = ProductCombinations.objects.create(
#                         product_attribute=product_attribute, product_attribute_value=product_attribute_value, product_attribute_color_code=product_attribute_color_code, product=instance)

#                     variant_type = product_combination['variant_type']
#                     variant_value = product_combination['variant_value']
#                     variant_price = product_combination['variant_price']
#                     quantity = product_combination['quantity']
#                     try:
#                         discount_type = product_combination['discount_type']
#                     except:
#                         discount_type = ''

#                     try:
#                         discount_amount = product_combination['discount_amount']
#                     except:
#                         discount_amount = ''

#                     ProductCombinationsVariants.objects.create(
#                         variant_type=variant_type,  variant_value=variant_value, variant_price=variant_price, quantity=quantity, discount_type=discount_type, discount_amount=discount_amount, product=instance, product_combination=product_combination_instance)
#             else:
#                 p_c_v = ProductCombinationsVariants.objects.filter(
#                     product=instance).exists()
#                 if p_c_v:
#                     ProductCombinationsVariants.objects.filter(
#                         product=instance).delete()
#                 p_c = ProductCombinations.objects.filter(
#                     product=instance).exists()
#                 if p_c:
#                     ProductCombinations.objects.filter(
#                         product=instance).delete()

#             validated_data.update(
#                 {"updated_at": timezone.now()})
#             return super().update(instance, validated_data)
#         except:
#             validated_data.update(
#                 {"updated_at": timezone.now()})
#             return super().update(instance, validated_data)