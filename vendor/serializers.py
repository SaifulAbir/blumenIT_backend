from cart.serializers import OrderItemSerializer
from product.serializers import ProductImageSerializer, ProductReviewSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from product.models import Brand, Category, DiscountTypes, FlashDealInfo, FlashDealProduct, Inventory, \
    Product, ProductImages, ProductReview, ProductTags, ProductVariation, ProductVideoProvider, \
    ShippingClass, Specification, SpecificationValue, SubCategory, SubSubCategory, Tags, Units,\
    VatType, Attribute, FilterAttributes, ProductFilterAttributes, AttributeValues, ProductWarranty, Warranty
from user.models import User
from cart.models import Order, SubOrder, OrderItem
from user.serializers import CustomerProfileSerializer
from vendor.models import Seller
from django.db.models import Avg
from django.utils import timezone
from support_ticket.models import Ticket, TicketConversation


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
        fields = ['id', 'attribute', 'attribute_title', 'category', 'sub_category', 'sub_sub_category']


class AdminCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "admin category list serializer"
        model = Category
        fields = ['id', 'title', 'ordering_number', 'type', 'banner', 'icon']


class AddNewCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required= True)
    ordering_number = serializers.CharField(required= True)
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

        if category_filter_attributes:
            for f_attr in category_filter_attributes:
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
    sub_category_filtering_attributes = FilteringAttributesSerializer(many=True, required=False)
    class Meta:
        model = SubCategory
        fields = ['id', 'title', 'ordering_number', 'category', 'sub_category_filtering_attributes']

    def create(self, validated_data):
        try:
            sub_category_filtering_attributes = validated_data.pop('sub_category_filtering_attributes')
        except:
            sub_category_filtering_attributes = ''

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
        if sub_category_filtering_attributes:
            for f_attr in sub_category_filtering_attributes:
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
    sub_sub_category_filtering_attributes = FilteringAttributesSerializer(many=True, required=False)
    class Meta:
        model = SubSubCategory
        fields = ['id', 'title', 'ordering_number', 'category', 'sub_category', 'sub_sub_category_filtering_attributes']

    def create(self, validated_data):
        try:
            sub_sub_category_filtering_attributes = validated_data.pop('sub_sub_category_filtering_attributes')
        except:
            sub_sub_category_filtering_attributes = ''

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
        if sub_sub_category_filtering_attributes:
            for f_attr in sub_sub_category_filtering_attributes:
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
        fields = ['id', 'title', 'logo', 'meta_title', 'meta_description']


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
            'is_featured'
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
    class Meta:
        model = ProductFilterAttributes
        fields = [
            'id',
            'attribute_value'
        ]


class ProductWarrantiesSerializer(serializers.ModelSerializer):
    warranty = serializers.PrimaryKeyRelatedField(queryset=Warranty.objects.filter(is_active=True), many=False, write_only=True, required= True)
    class Meta:
        model = ProductWarranty
        fields = [
            'id',
            'warranty',
            'warranty_value',
            'warranty_value_type'
        ]


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
    shipping_class = serializers.PrimaryKeyRelatedField(queryset=ShippingClass.objects.all(), many=False, write_only=True, required= False)

    product_tags = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=True)
    product_images = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False)
    product_specification = ProductSpecificationSerializer(
        many=True, required=False)
    flash_deal = FlashDealSerializer(many=True, required=False)
    product_filter_attributes = ProductFilterAttributesSerializer(many=True, required=False)
    product_warranties = ProductWarrantiesSerializer(many=True, required=False)

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
            'discount_start_date',
            'discount_end_date',
            'discount_amount',
            'discount_type',
            'quantity',
            'sku',
            'external_link',
            'external_link_button_text',
            'full_description',
            'active_short_description',
            'short_description',
            'product_specification',
            'low_stock_quantity_warning',
            'show_stock_quantity',
            'in_house_product',
            'whole_sale_product',
            'cash_on_delivery',
            'is_featured',
            'todays_deal',
            'flash_deal',
            'shipping_time',
            'shipping_class',
            'vat',
            'vat_type',
            'product_filter_attributes',
            'product_warranties'
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

        # product_warranties
        try:
            product_warranties = validated_data.pop('product_warranties')
        except:
            product_warranties = ''

        # print("product_warranties")
        # print(product_warranties)

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
                    attribute_value = product_filter_attribute['attribute_value']
                    if attribute_value:
                        product_filter_attribute_instance = ProductFilterAttributes.objects.create(attribute_value=attribute_value,  product=product_instance)

            # product_warranties
            if product_warranties:
                for product_warranty in product_warranties:
                    warranty = product_warranty['warranty']
                    warranty_value = product_warranty['warranty_value']
                    warranty_value_type = product_warranty['warranty_value_type']
                    product_warranty_instance = ProductWarranty.objects.create(product=product_instance, warranty=warranty, warranty_value=warranty_value, warranty_value_type=warranty_value_type)

            return product_instance
        except:
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
    existing_product_warranties = serializers.SerializerMethodField('get_product_warranties')
    product_warranties = ProductWarrantiesSerializer(many=True, required=False)
    old_price = serializers.FloatField(read_only=True)


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
                    'price',
                    'old_price',
                    'pre_payment_amount',
                    'discount_start_date',
                    'discount_end_date',
                    'discount_amount',
                    'discount_type',
                    'update_quantity',
                    'sku',
                    'external_link',
                    'external_link_button_text',
                    'full_description',
                    'active_short_description',
                    'short_description',
                    'existing_product_specification',
                    'product_specification',
                    'low_stock_quantity_warning',
                    'show_stock_quantity',
                    'in_house_product',
                    'whole_sale_product',
                    'cash_on_delivery',
                    'is_featured',
                    'todays_deal',
                    'existing_flash_deal',
                    'flash_deal',
                    'shipping_time',
                    'shipping_class',
                    'vat',
                    'vat_type',
                    'existing_product_filter_attributes',
                    'product_filter_attributes',
                    'existing_product_warranties',
                    'product_warranties'
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

    def get_product_warranties(self, product):
        queryset = ProductWarranty.objects.filter(product=product, is_active = True)
        serializer = ProductWarrantiesSerializer(instance=queryset, many=True)
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
                    attribute_value = product_filter_attribute['attribute_value']
                    if attribute_value:
                        product_filter_attr = ProductFilterAttributes.objects.create(attribute_value=attribute_value, product=instance)
            else:
                p_f_a = ProductFilterAttributes.objects.filter(
                    product=instance).exists()
                if p_f_a == True:
                    ProductFilterAttributes.objects.filter(
                        product=instance).delete()

            # product_warranties
            if product_warranties:
                p_w = ProductWarranty.objects.filter(
                    product=instance).exists()
                if p_w == True:
                    ProductWarranty.objects.filter(
                        product=instance).delete()

                for product_warranties in product_warranties:
                    warranty = product_filter_attribute['warranty']
                    warranty_value = product_filter_attribute['warranty_value']
                    warranty_value_type = product_filter_attribute['warranty_value_type']
                    product_warranty_instance = p_w.objects.create(product=instance, warranty=warranty, warranty_value=warranty_value, warranty_value_type=warranty_value_type)
            else:
                p_w = ProductWarranty.objects.filter(
                    product=instance).exists()
                if p_w == True:
                    ProductWarranty.objects.filter(
                        product=instance).delete()

            # work with price
            if price:
                existing_price = Product.objects.get(id=instance.id).price
                if price != existing_price:
                    validated_data.update({"price" : price, "old_price" : existing_price})

            validated_data.update({"updated_at": timezone.now()})
            return super().update(instance, validated_data)
        except:
            validated_data.update({"updated_at": timezone.now()})
            return super().update(instance, validated_data)
# product update serializer end


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
                    'flash_deal_products'
                ]

    def create(self, validated_data):
        # product_warranties
        try:
            flash_deal_products = validated_data.pop('flash_deal_products')
        except:
            flash_deal_products = ''

        flash_deal_instance = FlashDealInfo.objects.create(**validated_data)

        # product_warranties
        if flash_deal_products:
            for flash_deal_product in flash_deal_products:
                product = flash_deal_product['product']
                discount_type = flash_deal_product['discount_type']
                discount_amount = flash_deal_product['discount_amount']
                FlashDealProduct.objects.create(flash_deal_info=flash_deal_instance, product=product, discount_type=discount_type, discount_amount=discount_amount)

        return flash_deal_instance

        # try:

        #     return flash_deal_instance
        # except:
        #     return flash_deal_instance


class AdminProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'username', 'phone', 'date_joined']


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
    attribute_title = serializers.CharField(source='attribute.title',read_only=True)
    category_title = serializers.CharField(source='category.title',read_only=True)
    sub_category_title = serializers.CharField(source='sub_category.title',read_only=True)
    sub_sub_category_title = serializers.CharField(source='sub_sub_category.title',read_only=True)
    class Meta:
        model = FilterAttributes
        fields = ['id', 'attribute', 'attribute_title', 'category', 'category_title', 'sub_category',
                  'sub_category_title', 'sub_sub_category', 'sub_sub_category_title', 'is_active']


class AdminOrderListSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(source='order_id.order_id',read_only=True)
    product_count = serializers.CharField(source='order_id.product_count',read_only=True)
    order_date = serializers.CharField(source='order_id.order_date',read_only=True)
    order_status = serializers.CharField(source='order_id.order_status',read_only=True)
    total_price = serializers.SerializerMethodField('get_total_price')
    created_at = serializers.CharField(source='order_id.created_at',read_only=True)
    payment_status = serializers.CharField(source='order_id.payment_status',read_only=True)
    user_email = serializers.CharField(source='order_id.user.email',read_only=True)
    user_phone = serializers.CharField(source='order_id.user.phone',read_only=True)

    class Meta:
        model = SubOrder
        fields = ['id', 'order_id', 'sub_order_id', 'product_count', 'order_date', 'order_status', 'total_price', 'created_at', 'payment_status', 'user_email', 'user_phone', 'in_house_order']

    def get_total_price(self, obj):
        order_items = OrderItem.objects.filter(order=obj.order_id)
        prices = []
        total_price = 0
        for order_item in order_items:
            price = order_item.unit_price
            if order_item.unit_price_after_add_warranty != 0.0:
                price = order_item.unit_price_after_add_warranty
            quantity = order_item.quantity
            t_price = float(price) * float(quantity)
            prices.append(t_price)
        sub_total = sum(prices)
        if sub_total:
            total_price += sub_total

        shipping_cost = obj.order_id.shipping_cost
        if shipping_cost:
            total_price += shipping_cost

        coupon_discount_amount = obj.order_id.coupon_discount_amount
        if coupon_discount_amount:
            total_price -= coupon_discount_amount
        return total_price


class AdminOrderViewSerializer(serializers.ModelSerializer):
    order_item_order = OrderItemSerializer(many=True, read_only=True)
    user = CustomerProfileSerializer(many=False, read_only=True)
    class Meta:
        model = Order
        fields = ['user', 'order_id', 'product_count', 'order_date', 'order_status', 'total_price',
                  'payment_type', 'shipping_cost', 'coupon_discount_amount', 'order_item_order', 'user']


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
    last_reply = serializers.SerializerMethodField()
    class Meta:
        model = Ticket
        fields = ['id', 'ticket_id', 'created_at', 'ticket_subject', 'user_name', 'status', 'last_reply']

    def get_last_reply(self, obj):
        selected_last_ticket_conversation = TicketConversation.objects.filter(
            ticket=obj).order_by('-created_at').latest('id').created_at
        data = selected_last_ticket_conversation.strftime("%Y-%m-%d, %H:%M:%S")
        return data


class AdminTicketConversationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    user_name = serializers.CharField(source='ticket.user.username',read_only=True)
    class Meta:
        model = TicketConversation
        fields = ['id', 'conversation_text', 'conversation_photo', 'created_at', 'user_name' ]


class AdminTicketDataSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username',read_only=True)
    ticket_conversation = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['id', 'ticket_id', 'user_name', 'created_at', 'status', 'ticket_subject', 'ticket_conversation']

    def get_ticket_conversation(self, obj):
        selected_ticket_conversation = TicketConversation.objects.filter(
            ticket=obj, is_active=True).order_by('-created_at')
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
        products = Product.objects.filter(category = obj)
        total_quantity = 0
        for product in products:
            total_quantity += product.total_quantity
        return total_quantity


class AdminWarrantyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warranty
        fields = ['id', 'title']


class AdminAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValues
        fields = ['id', 'title']