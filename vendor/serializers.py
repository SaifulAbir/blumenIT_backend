from blog.models import Blog
from cart.serializers import OrderItemSerializer
from home.serializers import AdvertisementDataSerializer, SliderAdvertisementDataSerializer
from product.serializers import ProductImageSerializer, ProductReviewSerializer, BrandSerializer, UnitSerializer
from cart.serializers import OrderItemSerializer, DeliveryAddressSerializer
from product.serializers import ProductImageSerializer, ProductReviewSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from product.models import Brand, Category, DiscountTypes, FlashDealInfo, FlashDealProduct, Inventory, \
    Product, ProductImages, ProductReview, ProductTags, ProductVariation, ProductVideoProvider, \
    ShippingClass, Specification, SpecificationValue, SubCategory, SubSubCategory, Tags, Units, \
    VatType, Attribute, FilterAttributes, ProductFilterAttributes, AttributeValues, ProductWarranty, Warranty, \
    SpecificationTitle, \
    Offer, OfferProduct, ShippingCountry, ShippingState, ShippingCity, OfferCategory
from user.models import User, Subscription
from cart.models import Order, Coupon, OrderItem, DeliveryAddress, PaymentType
from user.serializers import CustomerProfileSerializer
from vendor.models import Seller
from django.db.models import Avg
from django.utils import timezone
from support_ticket.models import Ticket, TicketConversation
from stuff.models import Role, RolePermissions
from home.models import CorporateDeal, Advertisement, HomeSingleRowData, SliderImage, RequestQuote, ContactUs
from django.db.models import Q
from django.db.models import Sum


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
    total_product = serializers.SerializerMethodField('get_total_product')

    class Meta:
        model = Seller
        fields = ['id', 'name', 'address', 'phone', 'email', 'logo', 'is_active', 'total_product']

    def get_total_product(self, obj):
        total_product_count = Product.objects.filter(status='PUBLISH', seller=obj).count()
        return total_product_count


class SellerDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = ['id', 'name', 'email', 'address', 'phone', 'logo']


class FilteringAttributesSerializer(serializers.ModelSerializer):
    attribute_title = serializers.CharField(source='attribute.title',read_only=True)
    class Meta:
        model = FilterAttributes
        fields = ['id', 'attribute', 'attribute_title']
        read_only_fields = ['category', 'sub_category', 'sub_sub_category']


class AdminCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "admin category list serializer"
        model = Category
        fields = ['id', 'title', 'ordering_number', 'type', 'banner', 'icon', 'is_featured', 'pc_builder']


class AddNewCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= True)
    ordering_number = serializers.CharField(required= False)
    category_filter_attributes = FilteringAttributesSerializer(many=True, required=False)

    class Meta:
        model = Category
        fields = ['id', 'title', 'ordering_number', 'type', 'icon', 'banner', 'category_filter_attributes']

    def create(self, validated_data):
        # filtering_attributes
        try:
            category_filter_attributes = validated_data.pop('category_filter_attributes')
        except:
            category_filter_attributes = ''

        # work with category title 
        # title_get = validated_data.pop('title')
        # title_get_data = title_get.lower()
        # if title_get:
        #     title_get_for_check = Category.objects.filter(title=title_get.lower())
        #     if title_get_for_check:
        #         raise ValidationError('This category title already exist in Category.')

        # work with order number
        # ordering_number_get = validated_data.pop('ordering_number')
        # ordering_number_get_data = ordering_number_get.lower()
        # if ordering_number_get:
        #     ordering_number_get_for_check = Category.objects.filter(ordering_number=ordering_number_get)
        #     if ordering_number_get_for_check:
        #         raise ValidationError('This category ordering number already exist in Category.')

        category_instance = Category.objects.create(**validated_data)

        if category_filter_attributes:
            for f_attr in category_filter_attributes:
                attribute = f_attr['attribute']
                if attribute:
                    filtering_attribute_create_instance = FilterAttributes.objects.create(attribute=attribute, category=category_instance)

        return category_instance


class UpdateCategoryDetailsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= False)
    ordering_number = serializers.CharField(required= False)
    filtering_attributes = serializers.SerializerMethodField('get_existing_filtering_attributes')
    class Meta:
        model = Category
        fields = ['id', 'title', 'ordering_number', 'type', 'icon', 'banner', 'subtitle', 'is_active', 'filtering_attributes']

    def get_existing_filtering_attributes(self, obj):
        try:
            queryset = FilterAttributes.objects.filter(category=obj.id, is_active=True).distinct()
            serializer = FilteringAttributesSerializer(instance=queryset, many=True, context={
                                                'request': self.context['request']})
            return serializer.data
        except:
            return []

class UpdateCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= False)
    ordering_number = serializers.CharField(required= False)
    filtering_attributes = FilteringAttributesSerializer(many=True, required=False)
    class Meta:
        model = Category
        fields = ['id', 'title', 'ordering_number', 'type', 'icon', 'banner', 'subtitle', 'is_active', 'filtering_attributes']

    def update(self, instance, validated_data):
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
        fields = ['id', 'title', 'ordering_number', 'category', 'is_featured', 'pc_builder']


class AddNewSubCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= True)
    ordering_number = serializers.CharField(required= False)
    sub_category_filtering_attributes = FilteringAttributesSerializer(many=True, required=False)
    class Meta:
        model = SubCategory
        fields = ['id', 'title', 'ordering_number', 'category', 'sub_category_filtering_attributes', 'icon']

    def create(self, validated_data):
        try:
            sub_category_filtering_attributes = validated_data.pop('sub_category_filtering_attributes')
        except:
            sub_category_filtering_attributes = ''

        # work with category title 
        # title_get = validated_data.pop('title')
        # title_get_data = title_get.lower()
        # if title_get:
        #     title_get_for_check = SubCategory.objects.filter(title=title_get.lower())
        #     if title_get_for_check:
        #         raise ValidationError('This Sub category title already exist in Sub Category.')

        # work with order number
        # ordering_number_get = validated_data.pop('ordering_number')
        # ordering_number_get_data = ordering_number_get.lower()
        # if ordering_number_get:
        #     ordering_number_get_for_check = SubCategory.objects.filter(ordering_number=ordering_number_get)
        #     if ordering_number_get_for_check:
        #         raise ValidationError('This Sub category ordering number already exist in SubCategory.')


        sub_category_instance = SubCategory.objects.create(**validated_data)

        # filtering_attributes
        if sub_category_filtering_attributes:
            for f_attr in sub_category_filtering_attributes:
                attribute = f_attr['attribute']
                if attribute:
                    filtering_attribute_create_instance = FilterAttributes.objects.create(attribute=attribute, sub_category=sub_category_instance)
        return sub_category_instance


class UpdateSubCategoryDetailsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= False)
    ordering_number = serializers.CharField(required= False)
    filtering_attributes = serializers.SerializerMethodField('get_existing_filtering_attributes')
    class Meta:
        model = SubCategory
        fields = ['id', 'title', 'ordering_number', 'category', 'is_active','filtering_attributes', 'icon']

    def get_existing_filtering_attributes(self, obj):
        try:
            queryset = FilterAttributes.objects.filter(sub_category=obj.id, is_active=True).distinct()
            serializer = FilteringAttributesSerializer(instance=queryset, many=True, context={
                                                'request': self.context['request']})
            return serializer.data
        except:
            return []

class UpdateSubCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= False)
    ordering_number = serializers.CharField(required= False)
    filtering_attributes = FilteringAttributesSerializer(many=True, required=False)
    class Meta:
        model = SubCategory
        fields = ['id', 'title', 'ordering_number', 'category', 'is_active', 'filtering_attributes', 'icon']

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
    ordering_number = serializers.CharField(required= False)
    sub_sub_category_filtering_attributes = FilteringAttributesSerializer(many=True, required=False)
    class Meta:
        model = SubSubCategory
        fields = ['id', 'title', 'ordering_number', 'category', 'sub_category', 'sub_sub_category_filtering_attributes', 'icon']

    def create(self, validated_data):
        try:
            sub_sub_category_filtering_attributes = validated_data.pop('sub_sub_category_filtering_attributes')
        except:
            sub_sub_category_filtering_attributes = ''

        # work with category title
        # title_get = validated_data.pop('title')
        # title_get_data = title_get.lower()
        # if title_get:
        #     title_get_for_check = SubSubCategory.objects.filter(title=title_get.lower())
        #     if title_get_for_check:
        #         raise ValidationError('This Sub Sub category title already exist in Sub Sub Category.')

        # work with order number
        # ordering_number_get = validated_data.pop('ordering_number')
        # ordering_number_get_data = ordering_number_get.lower()
        # if ordering_number_get:
        #     ordering_number_get_for_check = SubSubCategory.objects.filter(ordering_number=ordering_number_get)
        #     if ordering_number_get_for_check:
        #         raise ValidationError('This Sub Sub category ordering number already exist in Sub Sub Category.')

        sub_sub_category_instance = SubSubCategory.objects.create(**validated_data)

        # filtering_attributes
        if sub_sub_category_filtering_attributes:
            for f_attr in sub_sub_category_filtering_attributes:
                attribute = f_attr['attribute']
                if attribute:
                    filtering_attribute_create_instance = FilterAttributes.objects.create(attribute=attribute, sub_sub_category=sub_sub_category_instance)

        return sub_sub_category_instance


class UpdateSubSubCategoryDetailsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= False)
    ordering_number = serializers.CharField(required= False)
    filtering_attributes = serializers.SerializerMethodField('get_existing_filtering_attributes')
    class Meta:
        model = SubSubCategory
        fields = ['id', 'title', 'ordering_number', 'category', 'sub_category', 'is_active', 'filtering_attributes', 'icon']

    def get_existing_filtering_attributes(self, obj):
        try:
            queryset = FilterAttributes.objects.filter(sub_sub_category=obj.id, is_active=True).distinct()
            serializer = FilteringAttributesSerializer(instance=queryset, many=True, context={
                                                'request': self.context['request']})
            return serializer.data
        except:
            return []

class UpdateSubSubCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= False)
    ordering_number = serializers.CharField(required= False)
    filtering_attributes = FilteringAttributesSerializer(many=True, required=False)
    class Meta:
        model = SubSubCategory
        fields = ['id', 'title', 'ordering_number', 'category', 'sub_category', 'is_active', 'filtering_attributes', 'icon']

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
        fields = ['id', 'title', 'logo', 'meta_title', 'meta_description', 'is_gaming']


class VendorUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = ['id', 'title']


class VendorProductListSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    vendor_organization_name = serializers.CharField(source="vendor.organization_name",read_only=True)
    seller_title = serializers.CharField(source="seller.name",read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'slug',
            'thumbnail',
            'title',
            'vendor_organization_name',
            'seller',
            'seller_title',
            'sell_count',
            'price',
            'avg_rating',
            'quantity',
            'low_stock_quantity_warning',
            'todays_deal',
            'is_featured',
            'is_active',
            'in_house_product',
            'status'
        ]

    def get_avg_rating(self, obj):
        return obj.product_review_product.all().aggregate(Avg('rating_number'))['rating_number__avg']


class ProductSpecificationValuesSerializer(serializers.ModelSerializer):
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
    specification_values = ProductSpecificationValuesSerializer(
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
        serializer = ProductSpecificationValuesSerializer(instance=queryset, many=True)
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
    filter_attribute = serializers.PrimaryKeyRelatedField(queryset=FilterAttributes.objects.all(), many=False, required= True)
    attribute_value = serializers.PrimaryKeyRelatedField(queryset=AttributeValues.objects.all(), many=False, required= True)
    class Meta:
        model = ProductFilterAttributes
        fields = [
            'id',
            'filter_attribute',
            'attribute_value',
        ]


class ProductWarrantiesSerializer(serializers.ModelSerializer):
    warranty = serializers.PrimaryKeyRelatedField(queryset=Warranty.objects.filter(is_active=True), many=False, required= True)
    class Meta:
        model = ProductWarranty
        fields = [
            'id',
            'warranty',
            'warranty_value',
            'warranty_value_type'
        ]


class OfferProductSerializer(serializers.ModelSerializer):
    offer = serializers.PrimaryKeyRelatedField(queryset=Offer.objects.all(), many=False, required= False)
    class Meta:
        model = OfferProduct
        fields = [
            'id',
            'offer'
        ]

# class FlashDealSerializer(serializers.ModelSerializer):
#     flash_deal_info = serializers.PrimaryKeyRelatedField(queryset=FlashDealInfo.objects.all(), many=False, write_only=True, required= False)
#     discount_type = serializers.PrimaryKeyRelatedField(queryset=DiscountTypes.objects.all(), many=False, write_only=True, required= False)
#     class Meta:
#         model = FlashDealProduct
#         fields = [
#             'id',
#             'flash_deal_info',
#             'discount_amount',
#             'discount_type'
#         ]

# product create serializer start
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
    product_tags = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=True)
    product_images = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False)
    product_specification = ProductSpecificationSerializer(
        many=True, required=False)
    # flash_deal = FlashDealSerializer(many=True, required=False)
    offers = OfferProductSerializer(many=True, required=False)
    product_filter_attributes = ProductFilterAttributesSerializer(many=True, required=False)
    product_warranties = ProductWarrantiesSerializer(many=True, required=False)
    video_provider = serializers.PrimaryKeyRelatedField(queryset=ProductVideoProvider.objects.all(), many=False, write_only=True, required= False)

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
            'price',
            'pre_payment_amount',
            'quantity',
            'sku',
            'external_link',
            'external_link_button_text',
            'full_description',
            'active_short_description',
            'short_description',
            'meta_title',
            'meta_description',
            'product_specification',
            'show_stock_quantity',
            'in_house_product',
            'whole_sale_product',
            'cash_on_delivery',
            'is_featured',
            'todays_deal',
            'offers',
            'vat',
            'vat_type',
            'product_filter_attributes',
            'product_warranties'
        ]

        read_only_fields = ['slug', 'sell_count']

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

        # product_specification
        try:
            product_specification = validated_data.pop('product_specification')
        except:
            product_specification = ''

        # flash_deal
        # try:
        #     flash_deal = validated_data.pop('flash_deal')
        # except:
        #     flash_deal = ''

        # offers
        try:
            offers = validated_data.pop('offers')
        except:
            offers = ''

        # product_filter_attributes
        try:
            product_filter_attributes = validated_data.pop('product_filter_attributes')
        except:
            product_filter_attributes = ''


        # product_warranties
        try:
            product_warranties = validated_data.pop('product_warranties')
        except:
            product_warranties = ''

        product_instance = Product.objects.create(**validated_data)

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

        # product_specification
        try:
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
        except:
            raise ValidationError('Problem of Product Specification info insert.')

        # flash_deal
        # try:
        #     flash_deal_add_count = 0
        #     if flash_deal:
        #         for f_deal in flash_deal:
        #             flash_deal_info = f_deal['flash_deal_info']
        #             discount_type = f_deal['discount_type']
        #             discount_amount = f_deal['discount_amount']
        #             if flash_deal_info:
        #                 if flash_deal_add_count <= 0:
        #                     flash_deal_product_instance = FlashDealProduct.objects.create(product=product_instance, flash_deal_info=flash_deal_info, discount_type=discount_type, discount_amount=discount_amount)
        #                     flash_deal_add_count += 1
        #                 else:
        #                     pass
        # except:
        #     raise ValidationError('Problem of Flash Deal info insert.')

        # offers
        try:
            if offers:
                for offer in offers:
                    offer = offer['offer']
                    if offer:
                        OfferProduct.objects.create(product=product_instance, offer=offer)
        except:
            raise ValidationError('Problem of Offer product info insert.')

        # product_filter_attributes
        try:
            if product_filter_attributes:
                for product_filter_attribute in product_filter_attributes:
                    filter_attribute = product_filter_attribute['filter_attribute']
                    attribute_value = product_filter_attribute['attribute_value']
                    ProductFilterAttributes.objects.create(filter_attribute=filter_attribute, attribute_value=attribute_value, product=product_instance)
        except:
            raise ValidationError('Problem of Product Filter Attributes info insert.')

        # product_warranties
        try:
            if product_warranties:
                for product_warranty in product_warranties:
                    warranty = product_warranty['warranty']
                    warranty_value = product_warranty['warranty_value']
                    warranty_value_type = product_warranty['warranty_value_type']
                    product_warranty_instance = ProductWarranty.objects.create(product=product_instance, warranty=warranty, warranty_value=warranty_value, warranty_value_type=warranty_value_type)
        except:
            raise ValidationError('Problem of Product Product Warranties info insert.')

        return product_instance
# product create serializer end


class VendorProductViewSerializer(serializers.ModelSerializer):
    product_images = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
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
            'quantity',
            'refundable',
            'full_description',
            'product_specification',
            'product_reviews',
            'in_house_product'
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

    def get_product_specification(self, product):
        queryset = Specification.objects.filter(product=product, is_active = True)
        serializer = ProductSpecificationSerializer(instance=queryset, many=True)
        return serializer.data

    def get_product_reviews(self, obj):
        selected_product_reviews = ProductReview.objects.filter(
            product=obj, is_active=True).distinct()
        return ProductReviewSerializer(selected_product_reviews, many=True).data


# product update serializer start
class ProductUpdateSerializer(serializers.ModelSerializer):
    sub_category = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), many=False, write_only=True, required= False)
    sub_sub_category = serializers.PrimaryKeyRelatedField(queryset=SubSubCategory.objects.all(), many=False, write_only=True, required= False)
    product_tags = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    product_images = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)
    product_specification = ProductSpecificationSerializer(many=True, required=False)
    # flash_deal = FlashDealSerializer(many=True, required=False)
    offers = OfferProductSerializer(many=True, required=False)
    quantity = serializers.IntegerField(required=False, write_only=True)
    product_filter_attributes = ProductFilterAttributesSerializer(many=True, required=False)
    product_warranties = ProductWarrantiesSerializer(many=True, required=False)
    video_provider = serializers.PrimaryKeyRelatedField(queryset=ProductVideoProvider.objects.all(), many=False, write_only=True, required= False)

    class Meta:
        model = Product
        fields =[
                    'id',
                    'title',
                    'category',
                    'sub_category',
                    'sub_sub_category',
                    'brand',
                    'unit',
                    'seller',
                    'minimum_purchase_quantity',
                    'product_tags',
                    'bar_code',
                    'refundable',
                    'video_provider',
                    'video_link',
                    'price',
                    'pre_payment_amount',
                    'quantity',
                    'sku',
                    'external_link',
                    'external_link_button_text',
                    'vat',
                    'vat_type',
                    'active_short_description',
                    'show_stock_quantity',
                    'in_house_product',
                    'whole_sale_product',
                    'cash_on_delivery',
                    'is_featured',
                    'todays_deal',
                    'full_description',
                    'short_description',
                    'meta_title',
                    'meta_description',
                    'thumbnail',
                    'product_images',
                    'product_filter_attributes',
                    'offers',
                    'product_warranties',
                    'product_specification',
                ]

    def update(self, instance, validated_data):
        # validation for sku start
        try:
            sku = validated_data["sku"]
        except:
            sku = ''

        if sku:
            product_check_sku = Product.objects.filter(Q(sku=sku), ~Q(id = instance.id))
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

        # product_specification
        try:
            product_specification = validated_data.pop('product_specification')
        except:
            product_specification = ''

        # offers
        try:
            offers = validated_data.pop('offers')
        except:
            offers = ''

        # product_filter_attributes
        try:
            product_filter_attributes = validated_data.pop('product_filter_attributes')
        except:
            product_filter_attributes = ''

        # product_warranties
        try:
            product_warranties = validated_data.pop('product_warranties')
        except:
            product_warranties = ''

        # price
        try:
            price = validated_data.pop('price')
        except:
            price = ''


        # tags
        try:
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
        except:
            raise ValidationError('Problem of Product Tags update.')

        # product_images
        try:
            if product_images:
                for image in product_images:
                    ProductImages.objects.create(
                        product=instance, file=image, status="COMPLETE")
        except:
            raise ValidationError('Problem of Product Image update.')

        # product with out variants
        try:
            single_quantity = validated_data["quantity"]
        except:
            single_quantity = ''

        try:
            single_quantity = int(single_quantity)
            if single_quantity >= 0:
                latest_inventory_obj = Inventory.objects.filter(product=instance).latest('created_at')
                latest_current_quantity = latest_inventory_obj.current_quantity

                if single_quantity == 0 and latest_current_quantity == 0:
                    pass
                else:
                    initial_quantity =  single_quantity - latest_current_quantity
                    Inventory.objects.create(product=instance, initial_quantity=initial_quantity, current_quantity=single_quantity)
                    total_initial_quantity= Inventory.objects.filter(product=instance).order_by('created_at').aggregate(Sum('initial_quantity'))
                    validated_data.update({"quantity" : single_quantity, "total_quantity": total_initial_quantity['initial_quantity__sum']})
            else:
                raise ValidationError("We can't accept Minus quantity value.")
        except:
            raise ValidationError('Problem of Product Quantity update.')

        # product_specification
        try:
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
        except:
            raise ValidationError('Problem of Product specification update.')

        # offers
        try:
            if offers:
                offer_ids = [offer['offer'].id for offer in offers]
                OfferProduct.objects.filter(Q(product=instance), ~Q(offer__in=offer_ids)).update(is_active=False)
                for offer in offers:
                    offer = offer['offer']
                    offer_product_exist = OfferProduct.objects.filter(product=instance, offer=offer).exists()
                    if not offer_product_exist:
                        OfferProduct.objects.create(product=instance, offer=offer)
                    else:
                        OfferProduct.objects.filter(product=instance, offer=offer).update(is_active=True)

        except:
            raise ValidationError('Problem of Product Offer product update.')

        # product_filter_attributes
        try:
            if product_filter_attributes:
                p_f_a = ProductFilterAttributes.objects.filter(
                    product=instance).exists()
                if p_f_a == True:
                    ProductFilterAttributes.objects.filter(
                        product=instance).delete()

                for product_filter_attribute in product_filter_attributes:
                    filter_attribute = product_filter_attribute['filter_attribute']
                    attribute_value = product_filter_attribute['attribute_value']
                    ProductFilterAttributes.objects.create(filter_attribute=filter_attribute, attribute_value=attribute_value, product=instance)
            else:
                p_f_a = ProductFilterAttributes.objects.filter(
                    product=instance).exists()
                if p_f_a == True:
                    ProductFilterAttributes.objects.filter(
                        product=instance).delete()
        except:
            raise ValidationError('Problem of Product attributes update.')

        # product_warranties
        try:
            if product_warranties:
                product_warranties_ids = [warranty['warranty'].id for warranty in product_warranties]
                ProductWarranty.objects.filter(Q(product=instance), ~Q(warranty__in=product_warranties_ids)).update(is_active=False)

                for product_warranty in product_warranties:
                    warranty = product_warranty['warranty']
                    warranty_value = product_warranty['warranty_value']
                    warranty_value_type = product_warranty['warranty_value_type']

                    warranty_exist = ProductWarranty.objects.filter(product=instance, warranty=warranty).exists()
                    if not warranty_exist:
                            ProductWarranty.objects.create(product=instance, warranty=warranty, warranty_value=warranty_value, warranty_value_type=warranty_value_type)
                    else:
                        ProductWarranty.objects.filter(product=instance, warranty=warranty).update(is_active=True)
        except:
            raise ValidationError('Problem of Product warranties update.')

        # work with price
        try:
            if price:
                existing_price = Product.objects.get(id=instance.id).price
                if price != existing_price:
                    validated_data.update({"price" : price, "old_price" : existing_price})
        except:
            raise ValidationError('Problem of Product price update.')

        validated_data.update({"updated_at": timezone.now()})
        return super().update(instance, validated_data)

# product update serializer end



# product update details serializer start
class ProductUpdateDetailsSerializer(serializers.ModelSerializer):
    product_tags = serializers.SerializerMethodField()
    product_images = serializers.SerializerMethodField()
    product_specification = serializers.SerializerMethodField('get_product_specification')
    # flash_deal = serializers.SerializerMethodField('get_flash_deal')
    offers = serializers.SerializerMethodField('get_offers')
    product_filter_attributes = serializers.SerializerMethodField('get_product_filter_attributes')
    product_warranties = serializers.SerializerMethodField('get_product_warranties')


    class Meta:
        model = Product
        fields =[
                    'id',
                    'title',
                    'category',
                    'sub_category',
                    'sub_sub_category',
                    'brand',
                    'unit',
                    'seller',
                    'minimum_purchase_quantity',
                    'product_tags',
                    'bar_code',
                    'refundable',
                    'video_provider',
                    'video_link',
                    'price',
                    'pre_payment_amount',
                    'quantity',
                    'total_quantity',
                    'sku',
                    'external_link',
                    'external_link_button_text',
                    'vat',
                    'vat_type',
                    'meta_title',
                    'meta_description',
                    'active_short_description',
                    'show_stock_quantity',
                    'in_house_product',
                    'whole_sale_product',
                    'cash_on_delivery',
                    'is_featured',
                    'todays_deal',
                    'full_description',
                    'short_description',
                    'thumbnail',
                    'product_images',
                    'product_filter_attributes',
                    'offers',
                    'product_warranties',
                    'product_specification',
                ]
    def get_product_tags(self, obj):
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

    def get_product_images(self, obj):
        try:
            queryset = ProductImages.objects.filter(
                product=obj, is_active=True).distinct()
            serializer = ProductImageSerializer(instance=queryset, many=True, context={
                                                'request': self.context['request']})
            return serializer.data
        except:
            return []

    def get_product_specification(self, product):
        queryset = Specification.objects.filter(product=product, is_active = True)
        serializer = ProductExistingSpecificationSerializer(instance=queryset, many=True)
        return serializer.data

    def get_offers(self, product):
        queryset = OfferProduct.objects.filter(product=product, is_active=True)
        serializer = OfferProductSerializer(instance=queryset, many=True)
        return serializer.data

    def get_product_filter_attributes(self, product):
        queryset = ProductFilterAttributes.objects.filter(product=product, is_active = True)
        serializer = ProductFilterAttributesSerializer(instance=queryset, many=True)
        return serializer.data

    def get_product_warranties(self, product):
        queryset = ProductWarranty.objects.filter(product=product, is_active = True)
        serializer = ProductWarrantiesSerializer(instance=queryset, many=True)
        return serializer.data
# product update details serializer end

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


class FlashDealProductSerializer(serializers.ModelSerializer):
    discount_type = serializers.PrimaryKeyRelatedField(queryset=DiscountTypes.objects.all(), many=False, write_only=True, required= True)
    discount_amount = serializers.FloatField(required= True)
    class Meta:
        model = FlashDealProduct
        fields = [
                    'id',
                    'product',
                    'discount_type',
                    'discount_amount',
                ]


class FlashDealInfoSerializer(serializers.ModelSerializer):
    flash_deal_products = FlashDealProductSerializer(many=True, required=False)
    existing_flash_deal_products = serializers.SerializerMethodField('get_flash_deal_products')
    class Meta:
        model = FlashDealInfo
        fields = [
                    'id',
                    'title',
                    'background_color',
                    'text_color',
                    'banner',
                    'start_date',
                    'end_date',
                    'is_active',
                    'is_featured',
                    'flash_deal_products',
                    'existing_flash_deal_products'
                ]

    def get_flash_deal_products(self, obj):
        queryset = FlashDealProduct.objects.filter(flash_deal_info=obj, is_active = True)
        serializer = FlashDealProductSerializer(instance=queryset, many=True)
        return serializer.data

    def create(self, validated_data):
        # product_warranties
        try:
            flash_deal_products = validated_data.pop('flash_deal_products')
        except:
            flash_deal_products = ''

        flash_deal_instance = FlashDealInfo.objects.create(**validated_data)

        try:
            # product_warranties
            if flash_deal_products:
                for flash_deal_product in flash_deal_products:
                    product = flash_deal_product['product']
                    discount_type = flash_deal_product['discount_type']
                    discount_amount = flash_deal_product['discount_amount']
                    FlashDealProduct.objects.create(flash_deal_info=flash_deal_instance, product=product, discount_type=discount_type, discount_amount=discount_amount)

            return flash_deal_instance
        except:
            return flash_deal_instance

    def update(self, instance, validated_data):
        # flash_deal_products
        try:
            flash_deal_products = validated_data.pop('flash_deal_products')
        except:
            flash_deal_products = ''

        try:
            # product_warranties
            if flash_deal_products:
                f_d_p = FlashDealProduct.objects.filter(flash_deal_info=instance).exists()
                if f_d_p == True:
                    FlashDealProduct.objects.filter(flash_deal_info=instance).delete()

                for flash_deal_product in flash_deal_products:
                    product = flash_deal_product['product']
                    discount_type = flash_deal_product['discount_type']
                    discount_amount = flash_deal_product['discount_amount']
                    FlashDealProduct.objects.create(flash_deal_info=instance, product=product, discount_type=discount_type, discount_amount=discount_amount)
            else:
                f_d_p = FlashDealProduct.objects.filter(flash_deal_info=instance).exists()
                if f_d_p == True:
                    FlashDealProduct.objects.filter(flash_deal_info=instance).delete()

            validated_data.update({"updated_at": timezone.now()})
            return super().update(instance, validated_data)
        except:
            validated_data.update({"updated_at": timezone.now()})
            return super().update(instance, validated_data)


class RolePermissionsDataSerializer(serializers.ModelSerializer):
    permission_module_title = serializers.CharField(source='permission_module.title',read_only=True)
    class Meta:
        model = RolePermissions
        fields = ['id', 'permission_module', 'permission_module_title']

class RoleDataSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField('get_permissions')
    class Meta:
        model = Role
        fields = ['id', 'title', 'permissions']

    def get_permissions(self, obj):
        queryset = RolePermissions.objects.filter(role=obj, is_active = True)
        serializer = RolePermissionsDataSerializer(instance=queryset, many=True)
        return serializer.data

class AdminProfileSerializer(serializers.ModelSerializer):
    staff_role = serializers.SerializerMethodField('get_staff_role')
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'username', 'phone', 'date_joined', 'staff_role']

    def get_staff_role(self, obj):
        try:
            queryset = Role.objects.filter(id=obj.role.id, is_active = True)
            serializer = RoleDataSerializer(instance=queryset, many=True)
            return serializer.data
        except:
            return []


class ReviewListSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title',read_only=True)
    customer_name = serializers.CharField(source='user.username',read_only=True)
    class Meta:
        model = ProductReview
        fields = ['id', 'product', 'product_title', 'user', 'customer_name', 'rating_number', 'review_text',
                  'is_active']


class AttributeValuesSerializer(serializers.ModelSerializer):
    attribute_title = serializers.CharField(source='attribute.title',read_only=True)
    class Meta:
        model = AttributeValues
        fields = ['id', 'attribute', 'attribute_title', 'value', 'is_active']


class AttributeSerializer(serializers.ModelSerializer):
    attribute_values = serializers.SerializerMethodField('get_attribute_values')
    class Meta:
        model = Attribute
        fields = ['id', 'title', 'is_active', 'attribute_values']

    def get_attribute_values(self, obj):
        values = AttributeValues.objects.filter(attribute=obj, is_active=True)
        return AttributeValuesSerializer(values, many=True, context={'request': self.context['request']}).data


class AdminFilterAttributeSerializer(serializers.ModelSerializer):
    attribute_values = serializers.SerializerMethodField('get_attribute_values')
    attribute_title = serializers.CharField(source='attribute.title',read_only=True)
    category_title = serializers.CharField(source='category.title',read_only=True)
    sub_category_title = serializers.CharField(source='sub_category.title',read_only=True)
    sub_sub_category_title = serializers.CharField(source='sub_sub_category.title',read_only=True)
    class Meta:
        model = FilterAttributes
        fields = ['id', 'attribute', 'attribute_title', 'attribute_values', 'category', 'category_title', 'sub_category',
                  'sub_category_title', 'sub_sub_category', 'sub_sub_category_title', 'is_active']
    def get_attribute_values(self, obj):
        values = AttributeValues.objects.filter(attribute=obj.attribute, is_active=True)
        return AttributeValuesSerializer(values, many=True, context={'request': self.context['request']}).data


class AdminFilterAttributeValueSerializer(serializers.ModelSerializer):
    attribute_title = serializers.CharField(source='attribute.title',read_only=True)
    class Meta:
        model = AttributeValues
        fields = ['id', 'attribute', 'attribute_title', 'value']


class AdminOrderListSerializer(serializers.ModelSerializer):
    # total_price = serializers.SerializerMethodField('get_total_price')
    user_email = serializers.CharField(source='user.email',read_only=True)
    user_phone = serializers.CharField(source='user.phone',read_only=True)
    seller = serializers.CharField(source='vendor.name',read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'delivery_address', 'order_id', 'product_count', 'order_date', 'order_status', 'total_price', 'created_at', 'payment_status', 'user_email', 'user_phone', 'vendor', 'seller', 'delivery_agent', 'refund', 'discount_amount']

    # def get_total_price(self, obj):
    #     order_items = OrderItem.objects.filter(order=obj)
    #     prices = []
    #     total_price = 0.0
    #     for order_item in order_items:
    #         price = order_item.unit_price
    #         if order_item.unit_price_after_add_warranty != 0.0:
    #             price = order_item.unit_price_after_add_warranty
    #         quantity = order_item.quantity
    #         t_price = float(price) * float(quantity)
    #         prices.append(t_price)
    #     if obj.vat_amount:
    #         sub_total = float(sum(prices)) + float(obj.vat_amount)
    #     else:
    #         sub_total = float(sum(prices))
    #     if sub_total:
    #         total_price += sub_total

    #     shipping_cost = obj.shipping_cost
    #     if shipping_cost:
    #         total_price += shipping_cost

    #     coupon_discount_amount = obj.coupon_discount_amount
    #     if coupon_discount_amount:
    #         total_price -= coupon_discount_amount

    #     discount_amount = obj.discount_amount
    #     if discount_amount:
    #         total_price -= discount_amount
    #     return total_price


class AdminOrderViewSerializer(serializers.ModelSerializer):
    order_item_order = OrderItemSerializer(many=True, read_only=True)
    user = CustomerProfileSerializer(read_only=True)
    delivery_address = DeliveryAddressSerializer(read_only=True)
    # total_price = serializers.SerializerMethodField('get_total_price')
    payment_method = serializers.CharField(source='payment_type.type_name',read_only=True)
    # sub_total = serializers.SerializerMethodField('get_sub_total')
    vat_amount = serializers.FloatField(read_only=True)
    warranty_price = serializers.SerializerMethodField('get_warranty_price')

    class Meta:
        model = Order
        fields = ['user', 'delivery_address', 'order_id', 'product_count', 'order_date', 'order_status', 'order_date', 'total_price', 'payment_status', 'payment_method', 'order_item_order', 'sub_total', 'vat_amount', 'shipping_cost', 'coupon_discount_amount', 'comment', 'warranty_price', 'discount_amount']

    # def get_sub_total(self, obj):
    #     order_items = OrderItem.objects.filter(order=obj)
    #     prices = []
    #     for order_item in order_items:
    #         price = order_item.unit_price
    #         if order_item.unit_price_after_add_warranty != 0.0:
    #             price = order_item.unit_price_after_add_warranty
    #         quantity = order_item.quantity
    #         t_price = float(price) * float(quantity)
    #         prices.append(t_price)
    #         sub_total = float(sum(prices))
    #     return sub_total

    # def get_total_price(self, obj):
    #     order_items = OrderItem.objects.filter(order=obj)
    #     prices = []
    #     total_price = 0
    #     for order_item in order_items:
    #         price = order_item.unit_price
    #         if order_item.unit_price_after_add_warranty != 0.0:
    #             price = order_item.unit_price_after_add_warranty
    #         quantity = order_item.quantity
    #         t_price = float(price) * float(quantity)
    #         prices.append(t_price)
    #     if obj.vat_amount:
    #         sub_total = float(sum(prices)) + float(obj.vat_amount)
    #     else:
    #         sub_total = float(sum(prices))
    #     if sub_total:
    #         total_price += sub_total
    def get_warranty_price(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        prices = []
        for order_item in order_items:
            if order_item.unit_price_after_add_warranty != 0.0:
                price = order_item.unit_price
                w_prices = order_item.unit_price_after_add_warranty
                t_price = float(w_prices) - float(price)
                prices.append(t_price)
        warranty_price = sum(prices)
            # print(t_price)
        return warranty_price

    def get_total_price(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        prices = []
        total_price = 0
        for order_item in order_items:
            price = order_item.unit_price
            if order_item.unit_price_after_add_warranty != 0.0:
                price = order_item.unit_price_after_add_warranty
            quantity = order_item.quantity
            t_price = float(price) * float(quantity)
            prices.append(t_price)
        if obj.vat_amount:
            sub_total = float(sum(prices)) + float(obj.vat_amount)
        else:
            sub_total = float(sum(prices))
        if sub_total:
            total_price += sub_total

    #     shipping_cost = obj.shipping_cost
    #     if shipping_cost:
    #         total_price += shipping_cost

    #     coupon_discount_amount = obj.coupon_discount_amount
    #     if coupon_discount_amount:
    #         total_price -= coupon_discount_amount

    #     discount_amount = obj.discount_amount
    #     if discount_amount:
    #         total_price -= discount_amount
    #     return total_price


class AdminOrderUpdateSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(read_only=True)
    class Meta:
        model = Order
        fields = ['order_id', 'order_status', 'payment_status']


class AdminCustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'is_active']


class AdminTicketListSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    user_name = serializers.CharField(source='ticket.user.username',read_only=True)
    user_email = serializers.CharField(source='ticket.user.email',read_only=True)
    last_reply = serializers.SerializerMethodField()
    class Meta:
        model = Ticket
        fields = ['id', 'ticket_id', 'created_at', 'ticket_subject', 'user_name', 'user_email', 'status', 'last_reply']

    def get_last_reply(self, obj):
        try:
            selected_last_ticket_conversation = TicketConversation.objects.filter(
                ticket=obj).order_by('-created_at').latest('id').created_at
            data = selected_last_ticket_conversation.strftime("%Y-%m-%d, %H:%M:%S")
            return data
        except:
            return ''


class AdminTicketConversationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    creator_user_name = serializers.CharField(source='ticket.user.username',read_only=True)
    replier_user_name = serializers.CharField(source='replier_user.username',read_only=True)
    class Meta:
        model = TicketConversation
        fields = ['id', 'conversation_text', 'conversation_photo', 'created_at', 'creator_user_name', 'replier_user_name', 'ticket' ]

    def create(self, validated_data):
        ticket_conversation_instance = TicketConversation.objects.create(**validated_data, replier_user=self.context['request'].user)
        return ticket_conversation_instance


class AdminTicketDataSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username',read_only=True)
    ticket_conversation = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['id', 'ticket_id', 'user_name', 'created_at', 'status', 'ticket_subject', 'ticket_conversation']

    def get_ticket_conversation(self, obj):
        selected_ticket_conversation = TicketConversation.objects.filter(ticket=obj, is_active=True)
        return AdminTicketConversationSerializer(selected_ticket_conversation, many=True).data


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'status']


class CategoryWiseProductSaleSerializer(serializers.ModelSerializer):
    sale_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'title', 'sale_count']

    def get_sale_count(self, obj):
        sell_count = Order.objects.filter(order_item_order__product__category = obj).count()
        return sell_count


class CategoryWiseProductStockSerializer(serializers.ModelSerializer):
    stock_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'title', 'stock_count']

    def get_stock_count(self, obj):
        products = Product.objects.filter(category = obj, status='PUBLISH')
        available_quantity = 0
        for product in products:
            available_quantity += product.quantity
        return available_quantity


class AdminWarrantyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warranty
        fields = ['id', 'title']


class AdminShippingCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingCountry
        fields = [
            'id',
            'title',
            'code',
        ]


class AdminShippingCitySerializer(serializers.ModelSerializer):
    shipping_state_title = serializers.CharField(source='shipping_state.title',read_only=True)
    class Meta:
        model = ShippingCity
        fields = [
            'id',
            'title',
            'shipping_state',
            'shipping_state_title'
        ]


class AdminShippingStateSerializer(serializers.ModelSerializer):
    shipping_country_title = serializers.CharField(source='shipping_country.title',read_only=True)
    class Meta:
        model = ShippingState
        fields = [
            'id',
            'title',
            'shipping_country',
            'shipping_country_title'
        ]


class AdminShippingClassSerializer(serializers.ModelSerializer):
    shipping_country_title = serializers.CharField(source='shipping_country.title', read_only=True)
    shipping_state_title = serializers.CharField(source='shipping_state.title', read_only=True)
    shipping_city_title = serializers.CharField(source='shipping_city.title', read_only=True)
    class Meta:
        model = ShippingClass
        fields = ['id', 'description', 'shipping_country', 'shipping_state', 'shipping_city', 'delivery_days',
                  'delivery_charge', 'shipping_country_title', 'shipping_state_title', 'shipping_city_title']


class AdminSpecificationTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationTitle
        fields = ['id', 'title']


class AdminSubscribersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'email']


class AdminCorporateDealSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorporateDeal
        fields = ['id', 'first_name', 'last_name', 'email', 'company_name', 'phone', 'region', 'details_text', 'attached_file']


class AdminRequestQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestQuote
        fields = ['id', 'name', 'email', 'phone', 'company_name', 'website', 'address', 'services', 'overview']


class AdminContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['id', 'name', 'email', 'phone', 'message']


class AdminCouponSerializer(serializers.ModelSerializer):
    amount = serializers.FloatField(required=True)

    class Meta:
        model = Coupon
        fields = [  'id',
                    'code',
                    'amount',
                    'quantity',
                    'start_time',
                    'end_time',
                    'min_shopping_amount',
                    'is_active'
                ]
        read_only_fields = ['id', 'number_of_uses']


class AdminOfferProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferProduct
        fields = [  'id',
                    'product',
        ]

class AdminOfferCategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferCategory
        fields = [
            'id', 'title'
        ]



class AdminOfferSerializer(serializers.ModelSerializer):
    # offer_category_title = serializers.CharField(source='offer_category.title',read_only=True)
    product_category_title = serializers.CharField(source='product_category.title',read_only=True)
    offer_products = AdminOfferProductsSerializer(many=True, required=False)
    existing_offer_products = serializers.SerializerMethodField('get_existing_offer_products')
    start_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    end_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    discount_price_title = serializers.CharField(source='discount_price_type.title', read_only=True)

    class Meta:
        model = Offer
        read_only_field = ['id']
        fields = [  'id',
                    'title',
                    'product_category',
                    'product_category_title',
                    # 'offer_category',
                    # 'offer_category_title',
                    'start_date',
                    'end_date',
                    'thumbnail',
                    'short_description',
                    'full_description',
                    'discount_price',
                    'discount_price_type',
                    'offer_products',
                    'existing_offer_products',
                    'discount_price_title'
                ]

    def get_existing_offer_products(self, obj):
        queryset = OfferProduct.objects.filter(offer=obj, is_active = True)
        serializer = AdminOfferProductsSerializer(instance=queryset, many=True)
        return serializer.data


    def create(self, validated_data):
        # offer_products
        try:
            offer_products = validated_data.pop('offer_products')
        except:
            offer_products = ''

        offer_instance = Offer.objects.create(**validated_data)

        try:
            # offer_products
            if offer_products:
                for offer_product in offer_products:
                    product = offer_product['product']
                    OfferProduct.objects.create(offer=offer_instance, product=product)
            return offer_instance
        except:
            return offer_instance

    def update(self, instance, validated_data):
        # offer_products
        try:
            offer_products = validated_data.pop('offer_products')
        except:
            offer_products = ''

        try:
            # offer_products
            if offer_products:
                o_p = OfferProduct.objects.filter(offer=instance).exists()
                if o_p == True:
                    OfferProduct.objects.filter(offer=instance).delete()

                for offer_product in offer_products:
                    product = offer_product['product']
                    OfferProduct.objects.create(offer=instance, product=product)
            else:
                o_p = OfferProduct.objects.filter(offer=instance).exists()
                if o_p == True:
                    OfferProduct.objects.filter(offer=instance).delete()

            validated_data.update({"updated_at": timezone.now()})
            return super().update(instance, validated_data)
        except:
            validated_data.update({"updated_at": timezone.now()})
            return super().update(instance, validated_data)


class AdminOfferDetailsSerializer(serializers.ModelSerializer):
    offer_category_title = serializers.CharField(source='offer_category.title',read_only=True)
    product_category_title = serializers.CharField(source='product_category.title',read_only=True)
    offer_products = serializers.SerializerMethodField('get_offer_products')
    start_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    end_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = Offer
        read_only_field = ['id']
        fields = [  'id',
                    'title',
                    'product_category',
                    'product_category_title',
                    'offer_category',
                    'offer_category_title',
                    'start_date',
                    'end_date',
                    'thumbnail',
                    'short_description',
                    'full_description',
                    'discount_price',
                    'discount_price_type',
                    'offer_products'
                ]

    def get_offer_products(self, obj):
        queryset = OfferProduct.objects.filter(offer=obj, is_active = True)
        serializer = AdminOfferProductsSerializer(instance=queryset, many=True)
        return serializer.data


class AdminPosCustomerCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username', 'email', 'phone', 'is_customer'
        ]

    # def create(self, validated_data):
    #     username = validated_data.pop('username')
    #     phone = validated_data.pop('phone')
    #     email = validated_data.pop('email')
    #     is_customer = validated_data.pop('is_customer')
    #
    #     query = User.objects.all()
    #
    #     query.username = username
    #     query.phone =
class AdminPosProductListSerializer(serializers.ModelSerializer):
    brand_title = serializers.CharField(source="brand.title", read_only=True)
    brand = BrandSerializer()
    unit = UnitSerializer()

    class Meta:
        model = Product
        fields = [
            'id',
            'slug',
            'thumbnail',
            'title',
            'price',
            'quantity',
            'low_stock_quantity_warning',
            'brand_title',
            'brand',
            'unit',
            'vat',
            'vat_type'
        ]

class AdminPosOrderItemSerializer(serializers.ModelSerializer):
    product_warranty = serializers.PrimaryKeyRelatedField(queryset=ProductWarranty.objects.all(), many=False,
                                                          write_only=True, required=False)

    class Meta:
        model = OrderItem
        fields = ['id',
                  'product',
                  'quantity',
                  'unit_price',
                  'product_warranty',
                  ]

class AdminPosOrderSerializer(serializers.ModelSerializer):
    order_items = AdminPosOrderItemSerializer(many=True, required=False)
    order_id = serializers.CharField(read_only=True)
    vat_amount =  serializers.FloatField()
    product_count = serializers.IntegerField(required=True)

    class Meta:
        model = Order
        fields = ['id', 'order_id', 'product_count', 'vat_amount', 'discount_amount',
                  'payment_type', 'shipping_class', 'shipping_cost', 'order_items', 'delivery_address', 'comment',
                  'customer', 'in_house_order', 'total_price',]

    def create(self, validated_data):
        order_items = validated_data.pop('order_items')
        payment_type = validated_data.get('payment_type')
        order_status = "PENDING"
        payment_status = "UN-PAID"

        if payment_type:
            type_name_org = PaymentType.objects.get(id=payment_type.id).type_name
            type_name = type_name_org.lower()
            if type_name != 'cash on delivery':
                order_status = "CONFIRMED"
                payment_status = "PAID"

        # stop take order process if any product out of stock
        if order_items:
            for order_item in order_items:
                product = order_item['product']
                quantity = order_item['quantity']
                inventory_obj = Inventory.objects.filter(product=product).latest('created_at')
                new_update_quantity = int(inventory_obj.current_quantity) - int(quantity)
                if int(new_update_quantity) < 0:
                    raise ValidationError("Order didn't create. One of product out of stock.")

        order_instance = Order.objects.create(**validated_data, order_status=order_status,payment_status=payment_status, user=validated_data.get('customer'))


        if order_items:
            count = 0
            for order_item in order_items:
                product = order_item['product']
                quantity = order_item['quantity']
                unit_price = order_item['unit_price']

                total_price = float(unit_price) * float(quantity)

                try:
                    product_warranty = order_item['product_warranty']
                except:
                    product_warranty = None

                if product_warranty:
                    warranty_value = product_warranty.warranty_value
                    warranty_value_type = product_warranty.warranty_value_type

                    if warranty_value_type == 'PERCENTAGE':
                        unit_price_after_add_warranty = float((float(unit_price) / 100) * float(warranty_value))
                        unit_price_after_add_warranty = unit_price + unit_price_after_add_warranty
                    elif warranty_value_type == 'FIX':
                        unit_price_after_add_warranty = float(float(unit_price) + float(warranty_value))
                        unit_price_after_add_warranty = unit_price + unit_price_after_add_warranty

                    total_price = float(unit_price_after_add_warranty) * float(quantity)

                    OrderItem.objects.create(order=order_instance, product=product, quantity=int(quantity),
                                                unit_price=unit_price, total_price=total_price,
                                                product_warranty=product_warranty,
                                                unit_price_after_add_warranty=unit_price_after_add_warranty)
                else:
                    OrderItem.objects.create(order=order_instance, product=product, quantity=int(quantity),
                                                unit_price=unit_price, total_price=total_price)


                # update inventory
                inventory_obj = Inventory.objects.filter(product=product).latest('created_at')
                new_update_quantity = int(inventory_obj.current_quantity) - int(quantity)
                Product.objects.filter(id=product.id).update(quantity=new_update_quantity)
                inventory_obj.current_quantity = new_update_quantity
                inventory_obj.save()

                # product sell count update
                count += 1
                product_sell_quan = Product.objects.filter(
                    slug=product.slug)[0].sell_count
                product_sell_quan += 1
                Product.objects.filter(slug=product.slug).update(
                    sell_count=product_sell_quan)

        return order_instance

class AdminCategoryToggleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'is_featured']


class AdminSubCategoryToggleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'title', 'is_featured', 'pc_builder']


class AdminProductToggleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'slug', 'title', 'status', 'is_featured']


class AdminBlogToggleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ['id', 'is_active','status']


class AdvertisementPosterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advertisement
        fields = ['id', 'image', 'bold_text', 'small_text', 'is_gaming', 'work_for']


class AdminProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ['id', 'is_active']


class AdminBrandIsGamingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'is_gaming']


class AdminCategoryIsPcBuilderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'pc_builder']


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderImage
        fields = [
            'id',
            'image',
            'bold_text',
            'small_text',
        ]


class WebsiteConfigurationSerializer(serializers.ModelSerializer):
    home_slider_images = SliderSerializer(many=True, required=False)
    gaming_slider_images = SliderSerializer(many=True, required=False)
    small_banners_carousel = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)
    small_banners_static = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)
    popular_products_banners = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)
    feature_products_banners = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)

    class Meta:
        model = HomeSingleRowData
        fields = [
            'id',
            'phone',
            'whats_app_number',
            'email',
            'bottom_banner',
            'shop_address',

            'home_slider_images',
            'small_banners_carousel',
            'small_banners_static',
            'popular_products_banners',
            'feature_products_banners',

            'gaming_slider_images'
        ]

    def create(self, validated_data):
        # home_slider_images
        try:
            home_slider_images = validated_data.pop('home_slider_images')
        except:
            home_slider_images = ''

        # gaming_slider_images
        try:
            gaming_slider_images = validated_data.pop('gaming_slider_images')
        except:
            gaming_slider_images = ''

        # small_banners_carousel
        try:
            small_banners_carousel = validated_data.pop('small_banners_carousel')
        except:
            small_banners_carousel = ''

        # small_banners_static
        try:
            small_banners_static = validated_data.pop('small_banners_static')
        except:
            small_banners_static = ''


        # popular_products_banners
        try:
            popular_products_banners = validated_data.pop('popular_products_banners')
        except:
            popular_products_banners = ''

        # feature_products_banners
        try:
            feature_products_banners = validated_data.pop('feature_products_banners')
        except:
            feature_products_banners = ''

        home_single_row_data_instance = HomeSingleRowData.objects.create(**validated_data)

        # home_slider_images
        try:
            if home_slider_images:
                for home_slider_image in home_slider_images:
                    try:
                        image = home_slider_image['image']
                    except:
                        raise ValidationError('Home Slider Image field required.')
                    try:
                        bold_text = home_slider_image['bold_text']
                    except:
                        bold_text = ''
                    try:
                        small_text = home_slider_image['small_text']
                    except:
                        small_text = ''
                    Advertisement.objects.create(image=image, bold_text=bold_text, small_text=small_text, is_gaming=False, work_for='SLIDER')
        except:
            raise ValidationError('Problem of Home Slider Images insert.')

        # gaming_slider_images
        try:
            if gaming_slider_images:
                for gaming_slider_image in gaming_slider_images:
                    try:
                        image = gaming_slider_image['image']
                    except:
                        raise ValidationError('Gaming Slider Image field required.')
                    try:
                        bold_text = gaming_slider_image['bold_text']
                    except:
                        bold_text = ''
                    try:
                        small_text = gaming_slider_image['small_text']
                    except:
                        small_text = ''
                    Advertisement.objects.create(image=image, bold_text=bold_text, small_text=small_text, is_gaming=True, work_for='SLIDER')
        except:
            raise ValidationError('Problem of Home Gaming Images insert.')

        # small_banners_carousel
        if small_banners_carousel:
            for small_banner in small_banners_carousel:
                Advertisement.objects.create(image=small_banner, work_for='SLIDER_SMALL_CAROUSEL', is_gaming=False)

        # small_banners_static
        if small_banners_static:
            for small_banner in small_banners_static:
                Advertisement.objects.create(image=small_banner, work_for='SLIDER_SMALL_STATIC', is_gaming=False)

        # popular_products_banners
        if popular_products_banners:
            for popular_products_banner in popular_products_banners:
                Advertisement.objects.create(image=popular_products_banner, work_for='POPULAR_PRODUCT_POSTER', is_gaming=False)

        # feature_products_banners
        if feature_products_banners:
            for feature_products_banner in feature_products_banners:
                Advertisement.objects.create(image=feature_products_banner, work_for='FEATURED_PRODUCT_POSTER', is_gaming=False)

        return home_single_row_data_instance


class WebsiteConfigurationUpdateSerializer(serializers.ModelSerializer):
    home_slider_images = SliderSerializer(many=True, required=False)
    gaming_slider_images = SliderSerializer(many=True, required=False)
    small_banners_carousel = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)
    small_banners_static = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)
    popular_products_banners = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)
    feature_products_banners = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)

    class Meta:
        model = HomeSingleRowData
        fields = [
            'id',
            'phone',
            'whats_app_number',
            'email',
            'bottom_banner',
            'shop_address',

            'home_slider_images',
            'small_banners_carousel',
            'small_banners_static',
            'popular_products_banners',
            'feature_products_banners',

            'gaming_slider_images'
        ]


    def update(self, instance, validated_data):
        # home_slider_images
        try:
            home_slider_images = validated_data.pop('home_slider_images')
        except:
            home_slider_images = ''

        # gaming_slider_images
        try:
            gaming_slider_images = validated_data.pop('gaming_slider_images')
        except:
            gaming_slider_images = ''

        # small_banners_carousel
        try:
            small_banners_carousel = validated_data.pop('small_banners_carousel')
        except:
            small_banners_carousel = ''

        # small_banners_static
        try:
            small_banners_static = validated_data.pop('small_banners_static')
        except:
            small_banners_static = ''

        # popular_products_banners
        try:
            popular_products_banners = validated_data.pop('popular_products_banners')
        except:
            popular_products_banners = ''

        # feature_products_banners
        try:
            feature_products_banners = validated_data.pop('feature_products_banners')
        except:
            feature_products_banners = ''


        # home_slider_images
        try:
            if home_slider_images:
                for home_slider_image in home_slider_images:
                    try:
                        image = home_slider_image['image']
                    except:
                        raise ValidationError('Home Slider Image field required.')
                    try:
                        bold_text = home_slider_image['bold_text']
                    except:
                        bold_text = ''
                    try:
                        small_text = home_slider_image['small_text']
                    except:
                        small_text = ''
                    Advertisement.objects.create(image=image, bold_text=bold_text, small_text=small_text, is_gaming=False, work_for='SLIDER')
        except:
            raise ValidationError('Problem of Home Slider Images update.')

        # gaming_slider_images
        try:
            if gaming_slider_images:
                for gaming_slider_image in gaming_slider_images:
                    try:
                        image = gaming_slider_image['image']
                    except:
                        raise ValidationError('Gaming Slider Image field required.')
                    try:
                        bold_text = gaming_slider_image['bold_text']
                    except:
                        bold_text = ''
                    try:
                        small_text = gaming_slider_image['small_text']
                    except:
                        small_text = ''
                    Advertisement.objects.create(image=image, bold_text=bold_text, small_text=small_text, is_gaming=True, work_for='SLIDER')
        except:
            raise ValidationError('Problem of Home Gaming Images insert.')

        # small_banners_carousel
        if small_banners_carousel:
            for small_banner in small_banners_carousel:
                Advertisement.objects.create(image=small_banner, work_for='SLIDER_SMALL_CAROUSEL', is_gaming=False)

        # small_banners_static
        if small_banners_static:
            for small_banner in small_banners_static:
                Advertisement.objects.create(image=small_banner, work_for='SLIDER_SMALL_STATIC', is_gaming=False)

        # popular_products_banners
        if popular_products_banners:
            for popular_products_banner in popular_products_banners:
                Advertisement.objects.create(image=popular_products_banner, work_for='POPULAR_PRODUCT_POSTER', is_gaming=False)

        # feature_products_banners
        if feature_products_banners:
            for feature_products_banner in feature_products_banners:
                Advertisement.objects.create(image=feature_products_banner, work_for='FEATURED_PRODUCT_POSTER', is_gaming=False)

        validated_data.update({"updated_at": timezone.now()})
        return super().update(instance, validated_data)

class WebsiteConfigurationViewSerializer(serializers.ModelSerializer):
    home_slider_images = serializers.SerializerMethodField('get_home_slider_images')
    gaming_slider_images = serializers.SerializerMethodField('get_gaming_slider_images')
    popular_products_banners = serializers.SerializerMethodField('get_popular_products_banners')
    small_banners_carousel = serializers.SerializerMethodField('get_small_banners_carousel')
    small_banners_static = serializers.SerializerMethodField('get_small_banners_static')
    feature_products_banners = serializers.SerializerMethodField('get_feature_products_banners')
    class Meta:
        model = HomeSingleRowData
        fields = [
            'id',
            'phone',
            'whats_app_number',
            'email',
            'bottom_banner',
            'shop_address',

            'home_slider_images',
            'small_banners_carousel',
            'small_banners_static',
            'popular_products_banners',
            'feature_products_banners',

            'gaming_slider_images'
        ]

    def get_home_slider_images(self, obj):
        try:
            queryset = SliderImage.objects.filter(is_active=True, is_gaming=False)
            serializer = SliderSerializer(instance=queryset, many=True, context={'request': self.context['request']})
            return serializer.data
        except:
            return []

    def get_gaming_slider_images(self, obj):
        try:
            queryset = SliderImage.objects.filter(is_active=True, is_gaming=True)
            serializer = SliderSerializer(instance=queryset, many=True, context={'request': self.context['request']})
            return serializer.data
        except:
            return []

    def get_popular_products_banners(self, obj):
        try:
            queryset = Advertisement.objects.filter(Q(work_for='POPULAR_PRODUCT_POSTER'),
                                                                              Q(is_active=True),
                                                                              Q(is_gaming=False)).order_by(
                '-created_at')[:3]
            serializer = AdvertisementDataSerializer(instance=queryset, many=True, context={'request': self.context['request']})
            return serializer.data
        except:
            return []

    def get_small_banners_carousel(self, obj):
        try:
            queryset = Advertisement.objects.filter(Q(work_for='SLIDER_SMALL_CAROUSEL'),
                                                                  Q(is_active=True), Q(is_gaming=False)).order_by(
            '-created_at')
            serializer = SliderAdvertisementDataSerializer(instance=queryset, many=True, context={'request': self.context['request']})
            return serializer.data
        except:
            return []

    def get_small_banners_static(self, obj):
        try:
            queryset = Advertisement.objects.filter(Q(work_for='SLIDER_SMALL_STATIC'), Q(is_active=True),
                                                                Q(is_gaming=False)).order_by('-created_at')[:2]
            serializer = SliderAdvertisementDataSerializer(instance=queryset, many=True, context={'request': self.context['request']})
            return serializer.data
        except:
            return []

    def get_feature_products_banners(self,obj):
        try:
            queryset = Advertisement.objects.filter(Q(work_for='FEATURED_PRODUCT_POSTER'),
                                                    Q(is_active=True), Q(is_gaming=False)).order_by('-created_at')[:3]
            serializer = AdvertisementDataSerializer(instance=queryset, many=True, context={'request': self.context['request']})
            return serializer.data
        except:
            return []




