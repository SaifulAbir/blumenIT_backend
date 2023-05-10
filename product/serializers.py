from rest_framework import serializers
from product.models import Category, ProductImages, SubCategory, SubSubCategory, Product, ProductTags, ProductReview, \
    Brand, DiscountTypes, Tags, Units, Specification, SpecificationValue, AttributeValues, Seller, FilterAttributes, \
    ProductWarranty, Offer, ProductReviewReply

from user.models import User
from vendor.models import StoreSettings
from django.db.models import Avg
from rest_framework.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone


class SellerDataSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(allow_null=True)

    class Meta:
        model = Seller
        fields = ['id', 'name', 'address',
                  'phone', 'email', 'logo', 'is_active']


class UserDataSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(
        source="user_customer_profile.avatar", read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'avatar'
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
            'icon',
            'sub_sub_category'
        ]

    def get_sub_sub_category(self, obj):
        selected_sub_sub_category = SubSubCategory.objects.filter(
            sub_category=obj).distinct()
        return SubSubCategorySerializer(selected_sub_sub_category, many=True).data


class StoreCategoryAPIViewListSerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'icon', 'banner', 'sub_category']

    def get_sub_category(self, obj):
        try:
            queryset = SubCategory.objects.filter(
                category=obj.id, is_active=True).distinct()
            serializer = SubCategorySerializerForMegaMenu(
                instance=queryset, many=True, context={'request': self.context['request']})
            return serializer.data
        except:
            return []


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

        brand_instance = Brand.objects.create(
            **validated_data, title=title_get_data)

        return brand_instance


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title', 'logo', 'meta_title',
                  'meta_description', 'is_gaming', 'rating_number', 'created_at']


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
        product_review_instance = ProductReview.objects.create(
            **validated_data, user=self.context['request'].user)
        return product_review_instance


class CommentsRepliesSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    created_at = serializers.DateTimeField(format="%d %B, %Y %I:%M %p")

    class Meta:
        model = ProductReviewReply
        fields = [
            'id',
            'review',
            'user',
            'user_name',
            'review_text',
            'created_at'
        ]


class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserDataSerializer()
    created_at = serializers.DateTimeField(format="%d %B, %Y %I:%M %p")
    replies = serializers.SerializerMethodField('get_replies')

    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'rating_number',
                  'review_text', 'replies', 'created_at']

    def get_replies(self, obj):
        replies = ProductReviewReply.objects.filter(review=obj, is_active=True)
        return CommentsRepliesSerializer(replies, many=True).data


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['id', 'file']


class SpecificationValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationValue
        fields = [
            'id',
            'key',
            'value'
        ]


class SpecificationSerializer(serializers.ModelSerializer):
    specification_values = serializers.SerializerMethodField(
        'get_existing_specification_values')
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
        queryset = SpecificationValue.objects.filter(
            specification=instense.id, is_active=True)
        serializer = SpecificationValuesSerializer(
            instance=queryset, many=True)
        return serializer.data


class ProductListBySerializer(serializers.ModelSerializer):
    product_specification = serializers.SerializerMethodField(
        'get_product_specification')
    product_tags = serializers.SerializerMethodField()
    discount_type = DiscountTypeSerializer()
    avg_rating = serializers.SerializerMethodField()
    brand_title = serializers.CharField(source="brand.title", read_only=True)
    product_condition_title = serializers.CharField(
        source="product_condition.title", read_only=True)
    review_count = serializers.SerializerMethodField('get_review_count')
    product_reviews = serializers.SerializerMethodField()
    seller = SellerDataSerializer()
    category = CategorySerializer()
    sub_category = SubCategorySerializer()
    sub_sub_category = SubSubCategorySerializer()
    brand = BrandSerializer()
    unit = UnitSerializer()
    total_quantity = serializers.SerializerMethodField()
    is_new = serializers.SerializerMethodField('get_is_new')

    offer_discount_id = serializers.SerializerMethodField(
        'get_offer_discount_id')
    offer_discount_price = serializers.SerializerMethodField(
        'get_offer_discount_price')
    offer_discount_price_type = serializers.SerializerMethodField(
        'get_offer_discount_price_type')
    price_after_offer_discount = serializers.SerializerMethodField(
        'get_price_after_offer_discount')

    # def to_representation(self, instance):
    #     # get the serialized data as a dictionary
    #     data = super().to_representation(instance)
    #     # update the price field with the discounted price
    #     if data['offer_discount_price']:
    #         data['price'] = data['offer_discount_price']
    # return the updated data
    # return data
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
            'vat',
            'vat_type',
            'brand_title',
            'product_condition',
            'product_condition_title',
            'short_description',
            'review_count',
            'product_reviews',
            'warranty',
            'short_description',
            'full_description',
            'in_house_product',
            'is_new',
            'offer_discount_id',
            'offer_discount_price',
            'offer_discount_price_type',
            'price_after_offer_discount'
        ]
        # ordering_fields = ('price', 'price_after_offer_discount')
        # ordering = ('-price_after_offer_discount',)

    def get_offer_discount_id(self, obj):
        today_date = timezone.now().date()
        offers = Offer.objects.filter(
            offer_product_offer__product=obj.id, is_active=True, end_date__gte=today_date)
        if offers:
            offer_id = offers[0].id
        else:
            offer_id = None
        return offer_id

    def get_offer_discount_price_type(self, obj):
        today_date = timezone.now().date()
        offers = Offer.objects.filter(
            offer_product_offer__product=obj.id, is_active=True, end_date__gte=today_date)
        if offers:
            price_type = offers[0].discount_price_type.title
        else:
            price_type = None
        return price_type

    def get_offer_discount_price(self, obj):
        today_date = timezone.now().date()
        offers = Offer.objects.filter(
            offer_product_offer__product=obj.id, is_active=True, end_date__gte=today_date)
        if offers:
            price = offers[0].discount_price
        else:
            price = None
        return price

    def get_is_new(self, obj):
        create_date = obj.created_at
        created_month_number = create_date.month
        created_year_number = create_date.year

        today = timezone.now().date()
        today_month = today.month
        today_year = today.year

        if created_month_number == today_month and created_year_number == today_year:
            return True
        else:
            return False

    def get_avg_rating(self, obj):
        return obj.product_review_product.all().aggregate(Avg('rating_number'))['rating_number__avg']

    def get_product_tags(self, obj):
        selected_product_tags = ProductTags.objects.filter(
            product=obj).distinct()
        return ProductTagsSerializer(selected_product_tags, many=True).data

    def get_product_specification(self, product):
        queryset = Specification.objects.filter(
            product=product, is_active=True)
        serializer = SpecificationSerializer(instance=queryset, many=True)
        return serializer.data

    def get_review_count(self, product):
        review_count = ProductReview.objects.filter(
            product=product, is_active=True).count()
        return review_count

    def get_product_reviews(self, obj):
        selected_product_reviews = ProductReview.objects.filter(
            product=obj, is_active=True).distinct()
        return ProductReviewSerializer(selected_product_reviews, many=True).data

    def get_total_quantity(self, obj):
        quantity = Product.objects.get(id=obj.id).quantity
        return quantity

    def get_price_after_offer_discount(self, obj):
        today_date = timezone.now().date()
        offers = Offer.objects.filter(
            offer_product_offer__product=obj.id, is_active=True, end_date__gte=today_date)
        if offers:
            offer_price = offers[0].discount_price
        else:
            offer_price = 0
        price_after_offer_discount = float(obj.price) - float(offer_price)
        return price_after_offer_discount


class ProductListBySerializerForHomeData(serializers.ModelSerializer):
    discount_type = DiscountTypeSerializer()
    total_quantity = serializers.SerializerMethodField()
    is_new = serializers.SerializerMethodField('get_is_new')
    offer_discount_id = serializers.SerializerMethodField(
        'get_offer_discount_id')
    offer_discount_price = serializers.SerializerMethodField(
        'get_offer_discount_price')
    offer_discount_price_type = serializers.SerializerMethodField(
        'get_offer_discount_price_type')

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'slug',
            'total_quantity',
            'price',
            'old_price',
            'vat',
            'vat_type',
            'discount_type',
            'discount_amount',
            'thumbnail',
            'warranty',
            'in_house_product',
            'is_new',
            'offer_discount_id',
            'offer_discount_price',
            'offer_discount_price_type',
        ]

    def get_offer_discount_id(self, obj):
        today_date = timezone.now().date()
        offers = Offer.objects.filter(
            offer_product_offer__product=obj.id, is_active=True, end_date__gte=today_date)
        if offers:
            offer_id = offers[0].id
        else:
            offer_id = None
        return offer_id

    def get_offer_discount_price_type(self, obj):
        today_date = timezone.now().date()
        offers = Offer.objects.filter(
            offer_product_offer__product=obj.id, is_active=True, end_date__gte=today_date)
        if offers:
            price_type = offers[0].discount_price_type.title
        else:
            price_type = None
        return price_type

    def get_offer_discount_price(self, obj):
        today_date = timezone.now().date()
        offers = Offer.objects.filter(
            offer_product_offer__product=obj.id, is_active=True, end_date__gte=today_date)
        if offers:
            price = offers[0].discount_price
        else:
            price = None
        return price

    def get_is_new(self, obj):
        create_date = obj.created_at
        created_month_number = create_date.month
        created_year_number = create_date.year

        today = timezone.now()
        today_month = today.month
        today_year = today.year

        if created_month_number == today_month and created_year_number == today_year:
            return True
        else:
            return False

    def get_total_quantity(self, obj):
        quantity = Product.objects.get(id=obj.id).quantity
        return quantity


class ProductWarrantySerializer(serializers.ModelSerializer):
    warranty_title = serializers.CharField(
        source="warranty.title", read_only=True)

    class Meta:
        model = ProductWarranty
        fields = [
            'id',
            'warranty_title',
            'warranty',
            'warranty_value',
            'warranty_value_type',
            'is_active'
        ]


class ProductDetailsSerializer(serializers.ModelSerializer):
    product_tags = serializers.SerializerMethodField()
    product_reviews = serializers.SerializerMethodField()
    seller = SellerDataSerializer()
    brand = BrandSerializer()
    unit = UnitSerializer()
    discount_type = DiscountTypeSerializer()
    avg_rating = serializers.SerializerMethodField()
    product_images = serializers.SerializerMethodField()
    product_specification = serializers.SerializerMethodField(
        'get_product_specification')
    vat_type_title = serializers.CharField(
        source="vat_type.title", read_only=True)
    related_products = serializers.SerializerMethodField()
    product_warranties = serializers.SerializerMethodField(
        'get_product_warranties')
    offer_discount_id = serializers.SerializerMethodField(
        'get_offer_discount_id')
    offer_discount_price = serializers.SerializerMethodField(
        'get_offer_discount_price')
    offer_discount_price_type = serializers.SerializerMethodField(
        'get_offer_discount_price_type')

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'slug',
            'sku',
            'avg_rating',
            'meta_title',
            'meta_description',
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
            'related_products',
            'product_warranties',
            'in_house_product',
            'offer_discount_id',
            'offer_discount_price',
            'offer_discount_price_type',
        ]

    def get_offer_discount_id(self, obj):
        today_date = timezone.now().date()
        offers = Offer.objects.filter(
            offer_product_offer__product=obj.id, is_active=True, end_date__gte=today_date)
        if offers:
            offer_id = offers[0].id
        else:
            offer_id = None
        return offer_id

    def get_offer_discount_price_type(self, obj):
        today_date = timezone.now().date()
        offers = Offer.objects.filter(
            offer_product_offer__product=obj.id, is_active=True, end_date__gte=today_date)
        if offers:
            price_type = offers[0].discount_price_type.title
        else:
            price_type = None
        return price_type

    def get_offer_discount_price(self, obj):
        today_date = timezone.now().date()
        offers = Offer.objects.filter(
            offer_product_offer__product=obj.id, is_active=True, end_date__gte=today_date)
        if offers:
            price = offers[0].discount_price
        else:
            price = None
        return price

    def get_avg_rating(self, obj):
        return obj.product_review_product.all().aggregate(Avg('rating_number'))['rating_number__avg']

    def get_product_tags(self, obj):
        selected_product_tags = ProductTags.objects.filter(
            product=obj).distinct()
        return ProductTagsSerializer(selected_product_tags, many=True).data

    def get_product_specification(self, product):
        queryset = Specification.objects.filter(
            product=product, is_active=True)
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
        return ProductListBySerializer(selected_related_products, many=True, context={'request': self.context['request']}).data

    def get_product_warranties(self, obj):
        selected_warranties = ProductWarranty.objects.filter(
            product=obj, is_active=True)
        return ProductWarrantySerializer(selected_warranties, many=True, context={'request': self.context['request']}).data


class PcBuilderSpecificationValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationValue
        fields = [
            'id',
            'key',
            'value'
        ]


class PcBuilderSpecificationSerializer(serializers.ModelSerializer):
    specification_values = serializers.SerializerMethodField(
        'get_existing_specification_values')
    title_name = serializers.CharField(source="title.title", read_only=True)

    class Meta:
        model = Specification
        fields = [
            'id',
            'title',
            'title_name',
            'specification_values'
        ]

    def get_existing_specification_values(self, instance):
        queryset = SpecificationValue.objects.filter(
            specification=instance.id, is_active=True)
        serializer = PcBuilderSpecificationValuesSerializer(
            instance=queryset, many=True)
        return serializer.data


class AttributeValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValues
        fields = [
            'id',
            'value',
        ]


class FilterAttributeSerializer(serializers.ModelSerializer):
    attribute_values = serializers.SerializerMethodField(
        'get_attribute_values')
    attribute_title = serializers.CharField(
        source="attribute.title", read_only=True)

    class Meta:
        model = FilterAttributes
        fields = [
            'id',
            'attribute',
            'attribute_title',
            'attribute_values'
        ]

    def get_attribute_values(self, instance):
        queryset = AttributeValues.objects.filter(
            attribute=instance.attribute.id, is_active=True)
        serializer = AttributeValuesSerializer(instance=queryset, many=True)
        return serializer.data

    def get_specification(self, obj):
        try:
            queryset = Specification.objects.filter(
                product=obj, is_active=True)
            serializer = PcBuilderSpecificationSerializer(
                instance=queryset, many=True)
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
