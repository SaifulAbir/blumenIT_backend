from django.template.loader import render_to_string
from product.serializers import BrandSerializer, CategorySerializer, DiscountTypeSerializer, ProductMediaSerializer, ProductReviewSerializer, ProductTagsSerializer, SubCategorySerializer, SubSubCategorySerializer, UnitSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ecommerce.common.emails import send_email_without_delay
from product.models import Brand, Category, DiscountTypes, Product, ProductCombinations, ProductCombinationsVariants, ProductMedia, ProductReview, ProductTags, SubCategory, SubSubCategory, Tags, Units, VariantType
from user.models import User
from user.serializers import UserRegisterSerializer
from vendor.models import VendorRequest, Vendor, StoreSettings,Seller
from django.db.models import Avg
from django.utils import timezone


#Seller Create serializer
class SellerSerializer(serializers.ModelSerializer):


    class Meta:
        model = Seller
        fields = ['id', 'name', 'address', 'phone', 'email', 'logo']


# Seller Detail serializer
class SellerDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = ['id', 'name', 'email', 'address', 'phone','logo']


# Vendor Request serializer
class VendorRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorRequest
        fields = ['id', 'first_name', 'last_name', 'organization_name',
                  'email', 'vendor_type', 'nid', 'trade_license']
        read_only_field =['first_name', 'last_name', 'organization_name',
                  'email', 'vendor_type', 'nid', 'trade_license']
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


class VendorProductCreateSerializer(serializers.ModelSerializer):
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
                    try:
                        discount_type = product_combination['discount_type']
                    except:
                        discount_type = ''

                    try:
                        discount_amount = product_combination['discount_amount']
                    except:
                        discount_amount = ''
                    ProductCombinationsVariants.objects.create(
                        variant_type=variant_type,  variant_value=variant_value, variant_price=variant_price, quantity=quantity, discount_type=discount_type, discount_amount=discount_amount, product=product_instance, product_combination=product_combination_instance)
            return product_instance
        except:
            return product_instance


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
    tags = serializers.SerializerMethodField()
    product_tags = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False)
    media = serializers.SerializerMethodField()
    product_media = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False)
    combinations = serializers.SerializerMethodField()
    product_combinations = ProductCombinationSerializer(
        many=True, required=False)

    class Meta:
        model = Product
        fields = ['id',
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
                  'tags',
                  'product_tags',
                  'media',
                  'product_media',
                  'combinations',
                  'product_combinations'
                  ]

    # def get_tags(self, obj):
    #     selected_product_tags = ProductTags.objects.filter(
    #         product=obj, is_active=True).distinct()
    #     return ProductTagsSerializer(selected_product_tags, many=True).data

    def get_tags(self, obj):
        tags_list = []
        try:
            selected_product_tags = ProductTags.objects.filter(
                product=obj, is_active=True).distinct()
            for s_p_t in selected_product_tags:
                # tag_title = s_p_t.title
                tag_title = s_p_t.tag.title
                tags_list.append(tag_title)
            return tags_list
        except:
            return tags_list

    def get_media(self, obj):
        queryset = ProductMedia.objects.filter(
            product=obj, is_active=True).distinct()
        serializer = ProductMediaSerializer(instance=queryset, many=True, context={
                                            'request': self.context['request']})
        return serializer.data

    # def get_media(self, obj):
    #     medias_list = []
    #     try:
    #         selected_product_medias = ProductMedia.objects.filter(
    #             product=obj).distinct()
    #         for s_p_m in selected_product_medias:
    #             request = self.context.get('request')
    #             media_url = request.build_absolute_uri(s_p_m.file.url)
    #             medias_list.append(media_url)
    #         return medias_list
    #     except:
    #         return medias_list

    def get_combinations(self, obj):
        selected_product_combinations = ProductCombinations.objects.filter(
            product=obj, is_active=True).distinct()
        return ProductCombinationSerializerForVendorProductUpdate(selected_product_combinations, many=True).data
        # return ProductCombinationSerializerForVendorProductDetails(selected_product_combinations, many=True).data

    def update(self, instance, validated_data):
        # validation for sku start
        try:
            sku = validated_data["sku"]
        except:
            sku = ''

        if sku:
            check_sku = Product.objects.filter(sku=sku)
            if check_sku:
                if int(check_sku[0].id) == int(instance.id):
                    pass
                elif int(check_sku[0].id) != int(instance.id):
                    raise ValidationError('This SKU already exist.')
                else:
                    pass
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
            product_tags = validated_data.pop('product_tags')
        except:
            product_tags = ''

        try:
            product_media = validated_data.pop('product_media')
        except:
            product_media = ''

        try:
            product_combinations = validated_data.pop('product_combinations')
        except:
            product_combinations = ''

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

            if product_media:
                for media_file in product_media:
                    ProductMedia.objects.create(
                        product=instance, file=media_file, status="COMPLETE")

            if product_combinations:
                p_c_v = ProductCombinationsVariants.objects.filter(
                    product=instance).exists()
                if p_c_v:
                    ProductCombinationsVariants.objects.filter(
                        product=instance).delete()
                p_c = ProductCombinations.objects.filter(
                    product=instance).exists()
                if p_c:
                    ProductCombinations.objects.filter(
                        product=instance).delete()

                for product_combination in product_combinations:
                    product_attribute = product_combination['product_attribute']
                    product_attribute_value = product_combination['product_attribute_value']
                    product_attribute_color_code = product_combination['product_attribute_color_code']
                    product_combination_instance = ProductCombinations.objects.create(
                        product_attribute=product_attribute, product_attribute_value=product_attribute_value, product_attribute_color_code=product_attribute_color_code, product=instance)

                    variant_type = product_combination['variant_type']
                    variant_value = product_combination['variant_value']
                    variant_price = product_combination['variant_price']
                    quantity = product_combination['quantity']
                    try:
                        discount_type = product_combination['discount_type']
                    except:
                        discount_type = ''

                    try:
                        discount_amount = product_combination['discount_amount']
                    except:
                        discount_amount = ''

                    ProductCombinationsVariants.objects.create(
                        variant_type=variant_type,  variant_value=variant_value, variant_price=variant_price, quantity=quantity, discount_type=discount_type, discount_amount=discount_amount, product=instance, product_combination=product_combination_instance)
            else:
                p_c_v = ProductCombinationsVariants.objects.filter(
                    product=instance).exists()
                if p_c_v:
                    ProductCombinationsVariants.objects.filter(
                        product=instance).delete()
                p_c = ProductCombinations.objects.filter(
                    product=instance).exists()
                if p_c:
                    ProductCombinations.objects.filter(
                        product=instance).delete()

            validated_data.update(
                {"updated_at": timezone.now()})
            return super().update(instance, validated_data)
        except:
            validated_data.update(
                {"updated_at": timezone.now()})
            return super().update(instance, validated_data)
