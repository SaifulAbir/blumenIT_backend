from enum import unique
from django.template.loader import render_to_string
from product.serializers import ProductImageSerializer, ProductReviewSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ecommerce.common.emails import send_email_without_delay
from product.models import Brand, Category, Color, DiscountTypes, FlashDealInfo, FlashDealProduct, Inventory, InventoryVariation, Product, ProductAttributeValues, ProductAttributes, ProductColor, ProductCombinations, ProductCombinationsVariants, ProductImages, ProductReview, ProductTags, ProductVariation, ProductVideoProvider, ShippingClass, Specification, SpecificationValue, SubCategory, SubSubCategory, Tags, Units, VariantType, VatType, Attribute, FilterAttributes, ProductFilterAttributes
from user.models import User
# from user.serializers import UserRegisterSerializer
from vendor.models import VendorRequest, Vendor, StoreSettings, Seller
from django.db.models import Avg
from django.utils import timezone


class SellerCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)

    class Meta:
        model = Seller
        fields = ['id', 'name', 'address', 'phone', 'email', 'logo', 'is_active']

    def create(self, validated_data):
        email_get = validated_data.pop('email')
        email_get_data = email_get.lower()
        if email_get:
            email_get_for_check = Seller.objects.filter(email=email_get.lower())
            if email_get_for_check:
                raise ValidationError('Email already exists')
        phone_get = validated_data.pop('phone')
        phone_get_data = phone_get.lower()
        if phone_get:
            phone_get_for_check = Seller.objects.filter(phone=phone_get.lower())
            if phone_get_for_check:
                raise ValidationError('Phone already exists')
        seller_instance = Seller.objects.create(**validated_data, phone=phone_get_data,
                                                email=email_get_data)
        return seller_instance

class SellerUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)

    class Meta:
        model = Seller
        fields = ['id', 'name', 'address', 'phone', 'email', 'logo', 'is_active']

    def update(self, instance, validated_data):
        email_get = validated_data.pop('email')
        email_get_data = email_get.lower()
        if email_get:
            email_get_for_check = Seller.objects.filter(email=email_get.lower())
            if email_get_for_check:
                raise ValidationError('Email already exists')
        phone_get = validated_data.pop('phone')
        phone_get_data = phone_get.lower()
        if phone_get:
            phone_get_for_check = Seller.objects.filter(phone=phone_get.lower())
            if phone_get_for_check:
                raise ValidationError('Phone already exists')
        validated_data.update({ "email": email_get_data, "phone": phone_get_data})
        return super().update(instance, validated_data)

class SellerSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(allow_null=True)

    class Meta:
        model = Seller
        fields = ['id', 'name', 'address', 'phone', 'email', 'logo', 'is_active']

class SellerDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = ['id', 'name', 'email', 'address', 'phone', 'logo']



class FilteringAttributesSerializer(serializers.ModelSerializer):
    attribute_title = serializers.CharField(source='attribute.title',read_only=True)
    class Meta:
        model = FilterAttributes
        fields = ['id', 'attribute', 'attribute_title', 'category', 'sub_category', 'sub_sub_category']

class AdminCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "admin category list serializer"
        model = Category
        fields = ['id', 'title', 'ordering_number', 'type']

class AddNewCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= True)
    ordering_number = serializers.CharField(required= True)

    filtering_attributes = FilteringAttributesSerializer(many=True, required=False)

    class Meta:
        model = Category
        fields = ['id', 'title', 'ordering_number', 'type', 'icon', 'banner', 'filtering_attributes']

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

        # filtering_attributes
        try:
            filtering_attributes = validated_data.pop('filtering_attributes')
        except:
            filtering_attributes = ''

        if filtering_attributes:
            for f_attr in filtering_attributes:
                attribute = f_attr['attribute']
                if attribute:
                    filtering_attribute_create_instance = FilterAttributes.objects.create(attribute=attribute, category=category_instance)

        return category_instance

class UpdateCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= False)
    ordering_number = serializers.CharField(required= False)
    existing_filtering_attributes = serializers.SerializerMethodField()
    filtering_attributes = FilteringAttributesSerializer(many=True, required=False)
    class Meta:
        model = Category
        fields = ['id', 'title', 'ordering_number', 'type', 'icon', 'banner', 'subtitle', 'is_active', 'existing_filtering_attributes', 'filtering_attributes']

    def get_existing_filtering_attributes(self, obj):
        try:
            queryset = FilterAttributes.objects.filter(category=obj.id, is_active=True).distinct()
            serializer = FilteringAttributesSerializer(instance=queryset, many=True, context={
                                                'request': self.context['request']})
            return serializer.data
        except:
            return []

    def update(self, instance, validated_data):
        # work with category title
        # try:
        #     title_get = validated_data.pop('title')
        # except:
        #     title_get = ''

        # if title_get:
            # title_get_for_check = Category.objects.filter(title=title_get.lower()).exists()
        #     instance_title = instance.title.lower()

        #     if instance_title == title_get_for_check:
        #         pass
        #     else:
                # if title_get_for_check == True:
                #     raise ValidationError('This category title already exist in Category.')
                # else:
                #     pass


        # filtering_attributes
        try:
            filtering_attributes = validated_data.pop('filtering_attributes')
        except:
            filtering_attributes = ''
        if filtering_attributes:
            f_a = FilterAttributes.objects.filter(
                category=instance).exists()
            if f_a == True:
                FilterAttributes.objects.filter(
                    category=instance).delete()

            for f_attr in filtering_attributes:
                attribute = f_attr['attribute']
                if attribute:
                    filter_attr_create_instance = FilterAttributes.objects.create(attribute=attribute, category=instance)
        else:
            f_a = FilterAttributes.objects.filter(
                category=instance).exists()
            if f_a == True:
                FilterAttributes.objects.filter(category=instance).delete()

        validated_data.update({"updated_at": timezone.now()})
        return super().update(instance, validated_data)

class AdminSubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'title', 'ordering_number', 'category']

class AddNewSubCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= True)
    ordering_number = serializers.CharField(required= True)
    filtering_attributes = FilteringAttributesSerializer(many=True, required=False)
    class Meta:
        model = SubCategory
        fields = ['id', 'title', 'ordering_number', 'category', 'filtering_attributes']

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

        # filtering_attributes
        try:
            filtering_attributes = validated_data.pop('filtering_attributes')
        except:
            filtering_attributes = ''
        if filtering_attributes:
            for f_attr in filtering_attributes:
                attribute = f_attr['attribute']
                if attribute:
                    filtering_attribute_create_instance = FilterAttributes.objects.create(attribute=attribute, sub_category=sub_category_instance)
        return sub_category_instance

class UpdateSubCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= False)
    ordering_number = serializers.CharField(required= False)
    existing_filtering_attributes = serializers.SerializerMethodField()
    filtering_attributes = FilteringAttributesSerializer(many=True, required=False)
    class Meta:
        model = SubCategory
        fields = ['id', 'title', 'ordering_number', 'category', 'is_active', 'existing_filtering_attributes', 'filtering_attributes']

    def get_existing_filtering_attributes(self, obj):
        try:
            queryset = FilterAttributes.objects.filter(sub_category=obj.id, is_active=True).distinct()
            serializer = FilteringAttributesSerializer(instance=queryset, many=True, context={
                                                'request': self.context['request']})
            return serializer.data
        except:
            return []

    def update(self, instance, validated_data):
        # filtering_attributes
        try:
            filtering_attributes = validated_data.pop('filtering_attributes')
        except:
            filtering_attributes = ''
        if filtering_attributes:
            f_a = FilterAttributes.objects.filter(
                sub_category=instance).exists()
            if f_a == True:
                FilterAttributes.objects.filter(
                    sub_category=instance).delete()

            for f_attr in filtering_attributes:
                attribute = f_attr['attribute']
                if attribute:
                    filter_attr_create_instance = FilterAttributes.objects.create(attribute=attribute, sub_category=instance)
        else:
            f_a = FilterAttributes.objects.filter(
                sub_category=instance).exists()
            if f_a == True:
                FilterAttributes.objects.filter(sub_category=instance).delete()

        validated_data.update({"updated_at": timezone.now()})
        return super().update(instance, validated_data)

class AdminSubSubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSubCategory
        fields = ['id', 'title', 'ordering_number', 'category', 'sub_category', 'is_active']

class AddNewSubSubCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= True)
    ordering_number = serializers.CharField(required= True)
    filtering_attributes = FilteringAttributesSerializer(many=True, required=False)
    class Meta:
        model = SubSubCategory
        fields = ['id', 'title', 'ordering_number', 'category', 'sub_category', 'filtering_attributes']

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

        sub_sub_category_instance = SubSubCategory.objects.create(**validated_data, title=title_get_data, ordering_number=ordering_number_get_data )

        # filtering_attributes
        try:
            filtering_attributes = validated_data.pop('filtering_attributes')
        except:
            filtering_attributes = ''
        if filtering_attributes:
            for f_attr in filtering_attributes:
                attribute = f_attr['attribute']
                if attribute:
                    filtering_attribute_create_instance = FilterAttributes.objects.create(attribute=attribute, sub_sub_category=sub_sub_category_instance)

        return sub_sub_category_instance

class UpdateSubSubCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= False)
    ordering_number = serializers.CharField(required= False)
    existing_filtering_attributes = serializers.SerializerMethodField()
    filtering_attributes = FilteringAttributesSerializer(many=True, required=False)
    class Meta:
        model = SubSubCategory
        fields = ['id', 'title', 'ordering_number', 'category', 'sub_category', 'is_active', 'existing_filtering_attributes', 'filtering_attributes']

    def get_existing_filtering_attributes(self, obj):
        try:
            queryset = FilterAttributes.objects.filter(sub_sub_category=obj.id, is_active=True).distinct()
            serializer = FilteringAttributesSerializer(instance=queryset, many=True, context={
                                                'request': self.context['request']})
            return serializer.data
        except:
            return []

    def update(self, instance, validated_data):
        # filtering_attributes
        try:
            filtering_attributes = validated_data.pop('filtering_attributes')
        except:
            filtering_attributes = ''
        if filtering_attributes:
            f_a = FilterAttributes.objects.filter(
                sub_sub_category=instance).exists()
            if f_a == True:
                FilterAttributes.objects.filter(
                    sub_sub_category=instance).delete()

            for f_attr in filtering_attributes:
                attribute = f_attr['attribute']
                if attribute:
                    filter_attr_create_instance = FilterAttributes.objects.create(attribute=attribute, sub_sub_category=instance)
        else:
            f_a = FilterAttributes.objects.filter(sub_sub_category=instance).exists()
            if f_a == True:
                FilterAttributes.objects.filter(sub_sub_category=instance).delete()


        validated_data.update({"updated_at": timezone.now()})
        return super().update(instance, validated_data)










class VendorBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title']

class VendorUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = ['id', 'title']

class VendorProductListSerializer(serializers.ModelSerializer):
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
    attribute_value_title = serializers.CharField(source="value.value",read_only=True)
    class Meta:
        model = ProductAttributeValues
        fields = [
            'id',
            'value',
            'attribute_value_title'
        ]

class ProductAttributesSerializer(serializers.ModelSerializer):
    attribute_title = serializers.CharField(source="attribute.title",read_only=True)
    product_attribute_values = ProductAttributeValuesSerializer(
        many=True, required=False)
    class Meta:
        model = ProductAttributes
        fields = [
            'id',
            'attribute',
            'attribute_title',
            'product_attribute_values'
        ]

class ProductExistingAttributesSerializer(serializers.ModelSerializer):
    attribute_title = serializers.CharField(source="attribute.title",read_only=True)
    product_attribute_values = serializers.SerializerMethodField('get_existing_product_attribute_values')

    class Meta:
        model = ProductAttributes
        fields = [
            'id',
            'attribute',
            'attribute_title',
            'product_attribute_values'
        ]

    def get_existing_product_attribute_values(self, instense):
        queryset = ProductAttributeValues.objects.filter(product_attribute=instense.id, is_active = True)
        serializer = ProductAttributeValuesSerializer(instance=queryset, many=True)
        return serializer.data

class ProductVariantsSerializer(serializers.ModelSerializer):
    variation = serializers.CharField(required=True, write_only=True)
    variation_price = serializers.FloatField(required=True, write_only=True)
    sku = serializers.CharField(required=True, write_only=True)
    quantity = serializers.IntegerField(required=False, write_only=True)
    update_quantity = serializers.IntegerField(required=False, write_only=True)
    class Meta:
        model = ProductVariation
        fields = [
            'id',
            'variation',
            'variation_price',
            'sku',
            'quantity',
            'update_quantity',
            'image',
        ]

class ProductExistingVariantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = [
            'id',
            'variation',
            'variation_price',
            'sku',
            'quantity',
            'image',
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

class ProductExistingSpecificationSerializer(serializers.ModelSerializer):
    specification_values = serializers.SerializerMethodField('get_existing_specification_values')
    class Meta:
        model = Specification
        fields = [
            'id',
            'title',
            'specification_values'
        ]

    def get_existing_specification_values(self, instense):
        queryset = SpecificationValue.objects.filter(specification=instense.id, is_active = True)
        serializer = SpecificationValuesSerializer(instance=queryset, many=True)
        return serializer.data

class FlashDealSerializer(serializers.ModelSerializer):
    flash_deal_info = serializers.PrimaryKeyRelatedField(queryset=FlashDealInfo.objects.all(), many=False, write_only=True, required= False)
    discount_type = serializers.PrimaryKeyRelatedField(queryset=DiscountTypes.objects.all(), many=False, write_only=True, required= False)
    class Meta:
        model = FlashDealProduct
        fields = [
            'id',
            'flash_deal_info',
            'discount_amount',
            'discount_type'
        ]

class FlashDealExistingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashDealProduct
        fields = [
            'id',
            'flash_deal_info',
            'discount_amount',
            'discount_type'
        ]

class ProductFilterAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFilterAttributes
        fields = [
            'id',
            'filter_attribute'
        ]

class ProductCreateSerializer(serializers.ModelSerializer):
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
    # product_colors = serializers.ListField(
    #     child=serializers.PrimaryKeyRelatedField(queryset=Color.objects.all()), write_only=True, required=False)
    # product_attributes = ProductAttributesSerializer(
    #     many=True, required=False)
    # product_variants = ProductVariantsSerializer(many=True, required=False)
    product_specification = ProductSpecificationSerializer(
        many=True, required=False)
    flash_deal = FlashDealSerializer(many=True, required=False)
    product_filter_attributes = ProductFilterAttributesSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'category',
            'sub_category',
            'sub_sub_category',
            'brand',
            'seller',
            'unit',
            'minimum_purchase_quantity',
            'product_tags',
            'bar_code',
            'refundable',
            'product_images',
            'thumbnail',
            'video_provider',
            'video_link',
            # 'product_colors',
            # 'product_attributes',
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
            # 'product_variants',
            'full_description',
            'active_short_description',
            'short_description',
            'product_specification',
            'low_stock_quantity_warning',
            'show_stock_quantity',
            'in_house_product',
            'cash_on_delivery',
            'is_featured',
            'todays_deal',
            'flash_deal',
            'shipping_time',
            'shipping_class',
            'vat',
            'vat_type',
            'product_filter_attributes'
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
        # try:
        #     product_colors = validated_data.pop('product_colors')
        # except:
        #     product_colors = ''

        # product_attributes
        # try:
        #     product_attributes = validated_data.pop('product_attributes')
        # except:
        #     product_attributes = ''

        # product_variants
        # try:
        #     product_variants = validated_data.pop('product_variants')
        # except:
        #     product_variants = ''

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

        # product_filter_attributes
        try:
            product_filter_attributes = validated_data.pop('product_filter_attributes')
        except:
            product_filter_attributes = ''

        product_instance = Product.objects.create(**validated_data, seller= Seller.objects.get(phone =  User.objects.get(id=self.context['request'].user.id).phone))
        # product_instance = Product.objects.create(**validated_data)

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
                for image in product_images:
                    ProductImages.objects.create(
                        product=product_instance, file=image, status="COMPLETE")

            # product_colors
            # if product_colors:
            #     for color in product_colors:
            #         if Color.objects.filter(title=color).exists():
            #             color_obj = Color.objects.get(title=color)
            #             if color_obj:
            #                 ProductColor.objects.create(
            #                     color=color_obj, product=product_instance)
            #             else:
            #                 pass
            #         else:
            #             pass

            # product_attributes
            # if product_attributes:
            #     for product_attribute in product_attributes:
            #         attribute_attribute = product_attribute['attribute']
            #         if product_instance and attribute_attribute:
            #             product_attributes_instance = ProductAttributes.objects.create(attribute=attribute_attribute, product=product_instance)
            #         product_attribute_values = product_attribute['product_attribute_values']
            #         for product_attribute_value in product_attribute_values:
            #             attribute_value_value = product_attribute_value['value']
            #             product_attributes_value_instance = ProductAttributeValues.objects.create(product_attribute = product_attributes_instance, value= attribute_value_value, product=product_instance)

            # product with out variants
            try:
                single_quantity = validated_data["quantity"]
            except:
                single_quantity = ''
            if single_quantity:
                total_quan = 0
                total_quan += single_quantity
                Product.objects.filter(id=product_instance.id).update(total_quantity=total_quan)
                # inventory update
                Inventory.objects.create(product=product_instance, initial_quantity=single_quantity, current_quantity=single_quantity)

            # product with variants
            # if product_variants:
            #     variation_total_quan = 0
            #     for product_variant in product_variants:
            #         variation = product_variant['variation']
            #         variation_price = product_variant['variation_price']
            #         variation_sku = product_variant['sku']
            #         variant_quantity = product_variant['quantity']
            #         try:
            #             v_image = product_variant['image']
            #         except:
            #             v_image = ''

            #         if variation_sku:
            #             product_check_sku = Product.objects.filter(sku=variation_sku)
            #             if product_check_sku:
            #                 raise ValidationError('This SKU already exist in product.')
            #             variation_check_sku = ProductVariation.objects.filter(sku=variation_sku)
            #             if variation_check_sku:
            #                 raise ValidationError('This SKU already exist in product variation.')


            #         if variation and variation_price and variation_sku and variant_quantity:
            #             total_price = float(variation_price) * float(variant_quantity)
            #             product_variation_instance = ProductVariation.objects.create(product=product_instance,
            #             variation=variation, variation_price=variation_price, sku=variation_sku, quantity=variant_quantity, total_quantity=variant_quantity, image=v_image, total_price=total_price)

            #             inventory_variation_instance = InventoryVariation.objects.create(product=product_instance, product_variation=product_variation_instance, variation_initial_quantity=variant_quantity, variation_current_quantity=variant_quantity)


            #         if variant_quantity:
            #             variation_total_quan += variant_quantity
            #             Product.objects.filter(id=product_instance.id).update(quantity=variation_total_quan, total_quantity=variation_total_quan)


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
                        product_specification_instance = SpecificationValue.objects.create(specification = specification_instance, key=key, value=value, product=product_instance )

            # flash_deal
            flash_deal_add_count = 0
            if flash_deal:
                for f_deal in flash_deal:
                    flash_deal_info = f_deal['flash_deal_info']
                    discount_type = f_deal['discount_type']
                    discount_amount = f_deal['discount_amount']
                    if flash_deal_info:
                        if flash_deal_add_count <= 0:
                            flash_deal_product_instance = FlashDealProduct.objects.create(product=product_instance, flash_deal_info=flash_deal_info, discount_type=discount_type, discount_amount=discount_amount)
                            flash_deal_add_count += 1
                        else:
                            pass

            # product_filter_attributes
            if product_filter_attributes:
                for product_filter_attribute in product_filter_attributes:
                    filter_attribute = product_filter_attribute['filter_attribute']
                    if filter_attribute:
                        product_filter_attribute_instance = ProductFilterAttributes.objects.create(filter_attribute=filter_attribute,  product=product_instance)

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

class ProductUpdateSerializer(serializers.ModelSerializer):
    product_category_name = serializers.SerializerMethodField()
    product_sub_category_name = serializers.SerializerMethodField()
    product_sub_sub_category_name = serializers.SerializerMethodField()
    product_brand_name = serializers.SerializerMethodField()
    product_unit_name = serializers.SerializerMethodField()
    existing_product_tags = serializers.SerializerMethodField()
    product_tags = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    existing_product_images = serializers.SerializerMethodField()
    product_images = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False)
    # existing_colors = serializers.SerializerMethodField()
    # product_colors = serializers.ListField(
    #     child=serializers.IntegerField(), write_only=True, required=False)
    # existing_product_attributes =serializers.SerializerMethodField('get_existing_product_attributes')
    # product_attributes = ProductAttributesSerializer(many=True, required=False)
    # existing_product_variants = serializers.SerializerMethodField('get_existing_product_variants')
    # product_variants = ProductVariantsSerializer(
    #     many=True, required=False)
    existing_product_specification = serializers.SerializerMethodField('get_product_specification')
    product_specification = ProductSpecificationSerializer(
        many=True, required=False)
    existing_flash_deal = serializers.SerializerMethodField('get_flash_deal')
    flash_deal = FlashDealSerializer(
        many=True, required=False)
    update_quantity = serializers.IntegerField(required=False, write_only=True)
    vat_type = VatTypeSerializer(many=False, required=False)
    existing_product_filter_attributes = serializers.SerializerMethodField('get_product_filter_attributes')
    product_filter_attributes = ProductFilterAttributesSerializer(many=True, required=False)

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
                    'seller',
                    'product_unit_name',
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
                    # 'existing_colors',
                    # 'product_colors',
                    # 'existing_product_attributes',
                    # 'product_attributes',
                    'price',
                    'pre_payment_amount',
                    'discount_start_date',
                    'discount_end_date',
                    'discount_amount',
                    'discount_type',
                    'update_quantity',
                    'sku',
                    'external_link',
                    'external_link_button_text',
                    # 'existing_product_variants',
                    # 'product_variants',
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
                    'vat_type',
                    'warranty',
                    'existing_product_filter_attributes',
                    'product_filter_attributes'
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

    def get_product_unit_name(self, obj):
        try:
            get_unit=Units.objects.get(id= obj.unit.id)
            return get_unit.title
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

    # def get_existing_colors(self, obj):
    #     color_list_ids = []
    #     try:
    #         selected_colors = ProductColor.objects.filter(
    #             product=obj, is_active=True).distinct()
    #         for s_c in selected_colors:
    #             color_id = s_c.color.id
    #             color_list_ids.append(color_id)
    #         return color_list_ids
    #     except:
    #         return color_list_ids

    # def get_existing_product_attributes(self, product):
    #     queryset = ProductAttributes.objects.filter(product=product, is_active = True)
    #     serializer = ProductExistingAttributesSerializer(instance=queryset, many=True)
    #     return serializer.data

    # def get_existing_product_variants(self, product):
    #     queryset = ProductVariation.objects.filter(product=product, is_active = True)
    #     serializer = ProductExistingVariantsSerializer(instance=queryset, many=True , context={'request': self.context['request']} )
    #     return serializer.data

    def get_product_specification(self, product):
        queryset = Specification.objects.filter(product=product, is_active = True)
        serializer = ProductExistingSpecificationSerializer(instance=queryset, many=True)
        return serializer.data

    def get_flash_deal(self, product):
        queryset = FlashDealProduct.objects.filter(product=product, is_active = True)
        serializer = FlashDealExistingSerializer(instance=queryset, many=True)
        return serializer.data

    def get_product_filter_attributes(self, product):
        queryset = ProductFilterAttributes.objects.filter(product=product, is_active = True)
        serializer = ProductFilterAttributesSerializer(instance=queryset, many=True)
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
        # try:
        #     product_colors = validated_data.pop('product_colors')
        # except:
        #     product_colors = ''

        # product_attributes
        # try:
        #     product_attributes = validated_data.pop('product_attributes')
        # except:
        #     product_attributes = ''

        # product_variants
        # try:
        #     product_variants = validated_data.pop('product_variants')
        # except:
        #     product_variants = ''

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

        # product_filter_attributes
        try:
            product_filter_attributes = validated_data.pop('product_filter_attributes')
        except:
            product_filter_attributes = ''


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
                        product=instance, file=image, status="COMPLETE")

            # product_colors
            # if product_colors:
            #     ProductColor.objects.filter(product=instance).delete()
            #     for color in product_colors:
            #         if Color.objects.filter(id=color).exists():
            #             color_obj = Color.objects.get(id=color)
            #             if color_obj:
            #                 ProductColor.objects.create(
            #                     color=color_obj, product=instance)
            #             else:
            #                 pass
            #         else:
            #             pass
            # else:
            #     ProductColor.objects.filter(product=instance).delete()

            # product_attributes
            # if product_attributes:
            #     p_a_v = ProductAttributeValues.objects.filter(
            #         product=instance).exists()

            #     if p_a_v == True:
            #         ProductAttributeValues.objects.filter(
            #             product=instance).delete()

            #     p_a = ProductAttributes.objects.filter(
            #         product=instance).exists()
            #     if p_a == True:
            #         ProductAttributes.objects.filter(
            #             product=instance).delete()

            #     for product_attribute in product_attributes:
            #         attribute_attribute = product_attribute['attribute']
            #         if attribute_attribute:
            #             product_attributes_instance = ProductAttributes.objects.create(attribute=attribute_attribute, product=instance)
            #         try:
            #             product_attribute_values = product_attribute['product_attribute_values']
            #         except:
            #             product_attribute_values = ''

            #         if product_attribute_values:
            #             for product_attribute_value in product_attribute_values:
            #                 attribute_value_value = product_attribute_value['value']
            #                 product_combination_instance = ProductAttributeValues.objects.create(product_attribute = product_attributes_instance, value= attribute_value_value, product=instance)
            # else:
            #     p_a_v = ProductAttributeValues.objects.filter(
            #         product=instance).exists()
            #     if p_a_v == True:
            #         ProductAttributeValues.objects.filter(
            #             product=instance).delete()

            #     p_a = ProductAttributes.objects.filter(
            #         product=instance).exists()
            #     if p_a == True:
            #         ProductAttributes.objects.filter(
            #             product=instance).delete()

            # product with out variants
            try:
                single_quantity = validated_data["update_quantity"]
            except:
                single_quantity = ''


            if single_quantity:
                quan = Product.objects.get(id=instance.id).quantity
                total_quan = Product.objects.get(id=instance.id).total_quantity
                if single_quantity:
                    quan += single_quantity
                    total_quan += single_quantity

                    # inventory update
                    latest_inventory_obj= Inventory.objects.filter(product=instance).latest('created_at')
                    current_qun = int(latest_inventory_obj.current_quantity) + int(single_quantity)
                    Inventory.objects.create(product=instance, initial_quantity=single_quantity, current_quantity=current_qun)
                    validated_data.update({"quantity" : quan, "total_quantity": total_quan})


            # product with variants
            # if product_variants:
            #     for product_variant in product_variants:
            #         variation = product_variant['variation']
            #         variation_price = product_variant['variation_price']
            #         sku = product_variant['sku']
            #         try:
            #             variant_quantity = product_variant['quantity']
            #         except:
            #             variant_quantity = ''
            #         try:
            #             variant_update_quantity = product_variant['update_quantity']
            #         except:
            #             variant_update_quantity = ''
            #         try:
            #             v_image = product_variant['image']
            #         except:
            #             v_image = ''


            #         # quantity and total quantity from product table 
            #         quan = Product.objects.get(id=instance.id).quantity
            #         total_quan = Product.objects.get(id=instance.id).total_quantity

            #         if variation and variant_quantity:
            #             # update product table, create a new row in product variant table, create new row inventory variation table

            #             quan += variant_quantity
            #             total_quan += variant_quantity

            #             # new row create in product variation 
            #             total_price = float(variation_price) * float(total_quan)
            #             product_variation_instance = ProductVariation.objects.create(product=instance,
            #             variation=variation, variation_price=variation_price, sku=sku, quantity=variant_quantity, total_quantity=variant_quantity, image=v_image, total_price=total_price)

            #             # create new row inventory variation
            #             inventory_variation_instance = InventoryVariation.objects.create(product=instance, product_variation=product_variation_instance, variation_initial_quantity=variant_quantity, variation_current_quantity=variant_quantity)

            #             # Product table update
            #             validated_data.update({"quantity" : quan, "total_quantity": total_quan})

            #         elif variation and variant_update_quantity:
            #             # update product table, update product variation, create a new row in inventory variation table

            #             quan += variant_update_quantity
            #             total_quan += variant_update_quantity

            #             # inventory update
            #             product_variation_instance = ProductVariation.objects.filter(variation=variation, product=instance)
            #             for product_variation_in in product_variation_instance:
            #                 latest_inventory_variation_obj= InventoryVariation.objects.filter(product_variation=product_variation_in, product=instance).latest('created_at')
            #                 current_qun = int(latest_inventory_variation_obj.variation_current_quantity) + int(variant_update_quantity)
            #                 product_variation = latest_inventory_variation_obj.product_variation

            #                 # InventoryVariation table update
            #                 InventoryVariation.objects.create(product=instance, variation_initial_quantity=variant_update_quantity, variation_current_quantity=current_qun, product_variation=product_variation)

            #                 # ProductVariation table update
            #                 product_variation_quan = ProductVariation.objects.get(id=product_variation.id).quantity
            #                 product_variation_total_quan = ProductVariation.objects.get(id=product_variation.id).total_quantity
            #                 product_variation_quan += variant_update_quantity
            #                 product_variation_total_quan += variant_update_quantity
            #                 total_price = float(variation_price) * float(total_quan)
            #                 if v_image:
            #                     product_variation_instance.update(variation_price=variation_price, sku=sku ,quantity=product_variation_quan,  total_quantity=product_variation_total_quan, image=v_image, total_price=total_price)
            #                 else:
            #                     product_variation_instance.update(variation_price=variation_price, sku=sku ,quantity=product_variation_quan,  total_quantity=product_variation_total_quan, total_price=total_price)

            #                 # Product table update
            #                 validated_data.update({"quantity" : quan, "total_quantity": total_quan})

            #         else:
            #             # update only product variation table

            #             product_variation_instance = ProductVariation.objects.filter(variation=variation, product=instance)
            #             for product_variation_in in product_variation_instance:

            #                 if v_image:
            #                     product_variation_instance.update(variation_price=variation_price, sku=sku, image=v_image)
            #                 else:
            #                     product_variation_instance.update(variation_price=variation_price, sku=sku)


            # product_specification
            if product_specification:
                specification_value = SpecificationValue.objects.filter(
                    product=instance).exists()
                if specification_value == True:
                    SpecificationValue.objects.filter(
                        product=instance).delete()

                specification = Specification.objects.filter(
                    product=instance).exists()
                if specification == True:
                    Specification.objects.filter(
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
                        SpecificationValue.objects.create(specification = specification_instance, key=key, value= value, product=instance)
            else:
                specification_value = SpecificationValue.objects.filter(
                    product=instance).exists()
                if specification_value == True:
                    SpecificationValue.objects.filter(
                        product=instance).delete()

                specification = Specification.objects.filter(
                    product=instance).exists()
                if specification == True:
                    Specification.objects.filter(
                        product=instance).delete()

            # flash_deal
            if flash_deal:
                f_p = FlashDealProduct.objects.filter(
                    product=instance).exists()
                if f_p == True:
                    FlashDealProduct.objects.filter(
                        product=instance).delete()

                for f_deal in flash_deal:
                    flash_deal_info = f_deal['flash_deal_info']
                    discount_type = f_deal['discount_type']
                    discount_amount = f_deal['discount_amount']
                    if flash_deal_info:
                        flash_deal_product_instance = FlashDealProduct.objects.create(product=instance, flash_deal_info=flash_deal_info, discount_type=discount_type, discount_amount=discount_amount)
            else:
                f_p = FlashDealProduct.objects.filter(
                    product=instance).exists()
                if f_p == True:
                    FlashDealProduct.objects.filter(
                        product=instance).delete()

            # product_filter_attributes
            if product_filter_attributes:
                p_f_a = ProductFilterAttributes.objects.filter(
                    product=instance).exists()
                if p_f_a == True:
                    ProductFilterAttributes.objects.filter(
                        product=instance).delete()

                for product_filter_attribute in product_filter_attributes:
                    filter_attribute = product_filter_attribute['filter_attribute']
                    if filter_attribute:
                        product_filter_attr = ProductFilterAttributes.objects.create(filter_attribute=filter_attribute, product=instance)
            else:
                p_f_a = ProductFilterAttributes.objects.filter(
                    product=instance).exists()
                if p_f_a == True:
                    ProductFilterAttributes.objects.filter(
                        product=instance).delete()

            validated_data.update({"updated_at": timezone.now()})
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

class FlashDealCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlashDealInfo
        fields = [
                    'id',
                    'title',
                    'background_color',
                    'text_color',
                    'banner',
                    'start_date',
                    'end_date'
                ]