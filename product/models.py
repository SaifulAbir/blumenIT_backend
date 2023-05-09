from django.db import models
from ecommerce.models import AbstractTimeStamp
from vendor.models import Seller
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
from user.models import User
from django.utils import timezone

from django.db.models import Avg

class Attribute(AbstractTimeStamp):
    title = models.CharField(
        max_length=100, null=False, blank=False, default="", help_text="name")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'Attribute'
        verbose_name_plural = 'Attributes'
        db_table = 'attribute'

    def __str__(self):
        return self.title


class AttributeValues(AbstractTimeStamp):
    attribute = models.ForeignKey(Attribute, on_delete=models.PROTECT,
                               related_name='attribute_values_attribute', blank=False, null=False)
    value = models.CharField(
        max_length=255, null=False, blank=False, default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'AttributeValues'
        verbose_name_plural = 'AttributeValues'
        db_table = 'attribute_attribute'

    def __str__(self):
        return 'attribute: ' + self.attribute.title + ' value: '+ self.value + ' ' + str(self.id)


class Category(AbstractTimeStamp):
    title = models.CharField(
        max_length=100, null=False, blank=False, default="", help_text="name")
    ordering_number = models.IntegerField(null=False, blank=False, default=0)
    type = models.CharField(max_length=100, null=True, blank=True, default="")
    banner = models.ImageField(
        upload_to='product_category', blank=True, null=True)
    icon = models.ImageField(
        upload_to='product_category', blank=True, null=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)
    pc_builder = models.BooleanField(null=False, blank=False, default=False)
    is_featured = models.BooleanField(null=False, blank=False, default=False)
    is_gaming = models.BooleanField(null=False, blank=False, default=False)

    subtitle = models.TextField(null=True, blank=True, default="")

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'category'

    def __str__(self):
        return 'id: ' + str(self.id) + ' Title: ' + self.title + ' pc_builder:' + str(self.pc_builder)


class SubCategory(AbstractTimeStamp):
    title = models.CharField(
        max_length=100, null=False, blank=False, default="", help_text="name")
    ordering_number = models.IntegerField(null=False, blank=False, default=0)
    icon = models.ImageField(
        upload_to='product_sub_category', blank=True, null=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)
    pc_builder = models.BooleanField(null=False, blank=False, default=False)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='sub_category_category')
    is_featured = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'
        db_table = 'sub_category'

    def __str__(self):
        return 'id: ' + str(self.id) + ' title: ' + self.title + ' pc_builder:' + str(self.pc_builder)


class SubSubCategory(AbstractTimeStamp):
    title = models.CharField(
        max_length=100, null=False, blank=False, default="", help_text="name")
    ordering_number = models.IntegerField(null=False, blank=False, default=0)
    icon = models.ImageField(
        upload_to='product_sub_sub_category', blank=True, null=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)
    pc_builder = models.BooleanField(null=False, blank=False, default=False)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='sub_sub_category_category')
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.PROTECT, related_name='sub_sub_category_sub_category')

    class Meta:
        verbose_name = 'SubSubCategory'
        verbose_name_plural = 'SubSubCategories'
        db_table = 'sub_sub_category'

    def __str__(self):
        return 'id: ' + str(self.id) + ' title: ' + self.title + ' Ordering Number:' + str(self.ordering_number)


class FilterAttributes(AbstractTimeStamp):
    attribute = models.ForeignKey(
        Attribute, related_name='filter_attributes_attribute', blank=False, null=False, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, related_name='filter_attributes_category', blank=True, null=True, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(
        SubCategory, related_name='filter_attributes_sub_category', blank=True, null=True, on_delete=models.CASCADE)
    sub_sub_category = models.ForeignKey(
        SubSubCategory, related_name='filter_attributes_sub_sub_category', blank=True, null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'FilterAttribute'
        verbose_name_plural = 'FilterAttributes'
        db_table = 'filter_attributes'

    def __str__(self):
        return  'id: '+ str(self.id) + ' Attribute Title : '+ self.attribute.title + ' category: ' + str(self.category) + ' sub category: ' + str(self.sub_category) + ' sub sub category: ' + str(self.sub_sub_category)


class Brand(AbstractTimeStamp):
    title = models.CharField(
        max_length=100, null=False, blank=True)
    logo = models.ImageField(upload_to='brand', blank=True, null=True)
    meta_title = models.CharField(max_length=200, null=False, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    rating_number = models.FloatField(null=True, blank=True, default=0.0)
    is_active = models.BooleanField(null=False, blank=False, default=True)
    is_gaming = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        db_table = 'brand'

    def __str__(self):
        return self.title


class Units(AbstractTimeStamp):
    title = models.CharField(
        max_length=100, null=False, blank=False, default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'
        db_table = 'units'

    def __str__(self):
        return self.title


class DiscountTypes(AbstractTimeStamp):
    title = models.CharField(
        max_length=100, null=False, blank=False, default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'DiscountType'
        verbose_name_plural = 'DiscountTypes'
        db_table = 'discount_types'

    def __str__(self):
        return self.title


class ProductVideoProvider(AbstractTimeStamp):
    title = models.CharField(max_length=800, default='', help_text="name")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductVideoProvider'
        verbose_name_plural = 'ProductVideoProviders'
        db_table = 'product_video_provider'

    def __str__(self):
        return self.title


class VatType(AbstractTimeStamp):
    title = models.CharField(max_length=800, default='', help_text="name")
    is_active = models.BooleanField(null=False, blank=False, default=True)
    class Meta:
        verbose_name = 'VatType'
        verbose_name_plural = 'VatTypes'
        db_table = 'vat_type'

    def __str__(self):
        return self.title


class ShippingCountry(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False, default='')
    code = models.CharField(max_length=10, null=False, blank=False, default='')
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ShippingCountry'
        verbose_name_plural = 'ShippingCountries'
        db_table = 'shipping_country'

    def __str__(self):
        return self.title


class ShippingState(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False, default='')
    shipping_country = models.ForeignKey(ShippingCountry, on_delete=models.CASCADE, related_name='shipping_state_shipping_country', blank=True, null=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ShippingState'
        verbose_name_plural = 'ShippingStates'
        db_table = 'shipping_state'

    def __str__(self):
        return self.title


class ShippingCity(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False, default='')
    shipping_state = models.ForeignKey(ShippingState, on_delete=models.CASCADE, related_name='shipping_city_shipping_state', blank=True, null=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ShippingCity'
        verbose_name_plural = 'ShippingCities'
        db_table = 'shipping_city'

    def __str__(self):
        return self.title


class ShippingClass(AbstractTimeStamp):
    description = models.TextField(default='', null=False, blank=False)
    shipping_country = models.ForeignKey(ShippingCountry, on_delete=models.CASCADE, related_name='shipping_class_shipping_country', blank=False, null=False)
    shipping_state = models.ForeignKey(ShippingState, on_delete=models.CASCADE, related_name='shipping_class_shipping_state', blank=False, null=False)
    shipping_city = models.ForeignKey(ShippingCity, on_delete=models.CASCADE, related_name='shipping_class_shipping_city', blank=False, null=False)
    delivery_days = models.IntegerField(default=0, help_text="Minimum days to delivery")
    delivery_charge = models.FloatField(max_length=255, null=False, blank=False, default=0)
    is_active = models.BooleanField(null=False, blank=False, default=True)
    class Meta:
        verbose_name = 'ShippingClass'
        verbose_name_plural = 'ShippingClasses'
        db_table = 'shipping_class'

    def __str__(self):
        return f"{self.pk}"


class ProductCondition(AbstractTimeStamp):
    title = models.CharField(max_length=800, default='', help_text="name")
    class Meta:
        verbose_name = 'ProductCondition'
        verbose_name_plural = 'ProductConditions'
        db_table = 'product_condition'

    def __str__(self):
        return self.title


class Product(AbstractTimeStamp):
    PRODUCT_STATUSES = [
        ('DRAFT', 'Draft'),
        ('PUBLISH', 'Publish'),
        ('UNPUBLISH', 'UnPublish')]

    title = models.CharField(max_length=800, default='')
    slug = models.SlugField(
        null=False, allow_unicode=True, blank=True, max_length=255)
    category = models.ForeignKey(
        Category, related_name='product_category', blank=False, null=True, on_delete=models.PROTECT)
    sub_category = models.ForeignKey(
        SubCategory, related_name='product_sub_category', blank=True, null=True, on_delete=models.PROTECT)
    sub_sub_category = models.ForeignKey(
        SubSubCategory, related_name='product_sub_sub_category', blank=True, null=True, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, related_name='product_brand',
                              blank=True, null=True, on_delete=models.PROTECT)
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT,
                               related_name='product_seller', blank=True, null=True)
    unit = models.ForeignKey(Units, related_name="product_unit",
                             blank=True, null=True, on_delete=models.PROTECT)
    minimum_purchase_quantity = models.IntegerField(null=True, blank=True, default=0)
    bar_code = models.CharField(max_length=255, blank=True, null=True, default='')
    refundable = models.BooleanField(default=False)
    is_featured = models.BooleanField(null=False, blank=False, default=False)
    cash_on_delivery = models.BooleanField(default=False)
    todays_deal = models.BooleanField(default=False)
    full_description = models.TextField(default='', null=True, blank=True)
    short_description = models.CharField(max_length=800, default='', null=True, blank=True)
    active_short_description = models.BooleanField(default=True)
    price = models.FloatField(
        max_length=255, null=False, blank=False, default=0, help_text="Unit price")
    old_price = models.FloatField(
        max_length=255, null=False, blank=False, default=0, help_text="Old price")
    pre_payment_amount = models.FloatField(
        max_length=255, null=False, blank=False, default=0)
    discount_start_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    discount_end_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    discount_type = models.ForeignKey(
        DiscountTypes, related_name="product_discount_type", null=True, blank=True, on_delete=models.PROTECT)
    discount_amount = models.FloatField(
        max_length=255, null=True, blank=True, default=0)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    total_quantity = models.IntegerField(null=False, blank=False, default=0)
    sku = models.CharField(max_length=500, null=True,blank=True, default="")
    external_link = models.URLField(null=True, blank=True)
    external_link_button_text = models.CharField(max_length=500, null=True, blank=True)
    video_provider = models.ForeignKey(
        ProductVideoProvider, related_name="product_video_provider", null=True, blank=True, on_delete=models.PROTECT)
    video_link = models.URLField(null=True, blank=True)
    thumbnail = models.FileField(upload_to='products', blank=True, null=True)
    low_stock_quantity_warning = models.IntegerField(null=True, blank=True, default=0)
    show_stock_quantity = models.BooleanField(default=False)
    vat = models.FloatField(null=True, blank=True, default=0.0)
    vat_type = models.ForeignKey(
        VatType, related_name="product_vat_type", null=True, blank=True, on_delete=models.PROTECT)
    product_condition = models.ForeignKey(
        ProductCondition, related_name="product_product_condition", null=True, blank=True, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=20, choices=PRODUCT_STATUSES, default=PRODUCT_STATUSES[0][0])
    is_active = models.BooleanField(null=False, blank=False, default=True)
    digital = models.BooleanField(default=False)
    in_house_product = models.BooleanField(default=False)
    whole_sale_product = models.BooleanField(default=False)
    sell_count = models.BigIntegerField(null=True, blank=True, default=0)
    warranty = models.CharField(max_length=100, default='', null=True, blank=True)
    total_average_rating_number = models.FloatField(null=True, blank=True, default=0.0)
    meta_title = models.CharField(max_length=200, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'products'

    @property
    def average_rating(self):
        if hasattr(self, '_average_rating'):
            return self._average_rating
        return self.reviews.aggregate(Avg('rating'))

    def __str__(self):
        return self.title + ' ' + str(self.status) + ' ' + str(self.is_active) + ' ' + str(self.seller)

def pre_save_product(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_product, sender=Product)


class SpecificationTitle(AbstractTimeStamp):
    title = models.CharField(max_length=800, default='', help_text="name")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'SpecificationTitle'
        verbose_name_plural = 'SpecificationTitles'
        db_table = 'specification_title'

    def __str__(self):
        return 'title: ' + self.title


class Specification(AbstractTimeStamp):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='specification_product')
    title = models.ForeignKey(
        SpecificationTitle, on_delete=models.PROTECT, related_name='specification_specification_title', null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'Specification'
        verbose_name_plural = 'Specifications'
        db_table = 'specification'

    def __str__(self):
        return 'Product: ' + self.product.title + ' - title: ' + self.title.title


class SpecificationValue(AbstractTimeStamp):
    specification = models.ForeignKey(
        Specification, on_delete=models.PROTECT, related_name='specification_specification')
    key = models.CharField(max_length=800, default='')
    value = models.CharField(max_length=255, default='')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='specification_value_product', null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'SpecificationValue'
        verbose_name_plural = 'SpecificationValues'
        db_table = 'specification_value'

    def __str__(self):
        # return self.key
        return 'Product: ' + self.specification.product.title + '-specification title: ' + self.specification.title.title + '-key: ' + self.key


class ProductVariation(AbstractTimeStamp):
    def validate_file_extension(value):
        import os
        from django.core.exceptions import ValidationError
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.jpg', '.png', '.jpeg']
        if not ext.lower() in valid_extensions:
            raise ValidationError('Unsupported file extension.')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,
                            blank=True, related_name='Product_variation_product')
    variation = models.CharField(
        max_length=255, null=True, blank=True, default="")
    variation_price = models.FloatField(null=True, blank=True, default=0)
    sku = models.CharField(max_length=500, null=True,blank=True, default="")
    quantity = models.IntegerField(null=True, blank=True, default=0)
    total_quantity = models.IntegerField(null=True, blank=True, default=0)
    image = models.FileField(upload_to='product_variation', validators=[validate_file_extension], null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True, default=0)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductVariation'
        verbose_name_plural = 'ProductVariations'
        db_table = 'product_variation'

    def __str__(self):
        return self.product.title + '-variation: ' + self.variation


class Tags(AbstractTimeStamp):
    title = models.CharField(
        max_length=100, null=False, blank=False, default="", unique=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        db_table = 'tags'

    def __str__(self):
        return self.title


class ProductTags(AbstractTimeStamp):
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, null=True,
                            blank=True, related_name='product_tags_product', default="")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False,
                                blank=False, related_name='product_tags_product', default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductTag'
        verbose_name_plural = 'ProductTags'
        db_table = 'product_tags'

    def __str__(self):
        return self.product.title


class ProductImages(AbstractTimeStamp):
    CHOICES = [
        ('COMPLETE', 'Complete'),
        ('IN_QUEUE', 'In_Queue'),
        ('IN_PROCESSING', 'In_Processing'),
    ]

    def validate_file_extension(value):
        import os
        from django.core.exceptions import ValidationError
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.jpg', '.png', '.jpeg']
        if not ext.lower() in valid_extensions:
            raise ValidationError('Unsupported file extension.')

    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='product_image_product', null=True, blank=True)
    file = models.FileField(upload_to='products', validators=[
                            validate_file_extension])
    status = models.CharField(
        max_length=20, choices=CHOICES, default=CHOICES[0][0])
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductImage'
        verbose_name_plural = 'ProductImages'
        db_table = 'product_images'

    def __str__(self):
        return self.product.title


class ProductReview(AbstractTimeStamp):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,
                                blank=True, related_name='product_review_product')
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT,
                               related_name='product_review_seller', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             related_name='product_review_user', blank=True, null=True)
    rating_number = models.FloatField(null=True, blank=True, default=0.0)
    review_text = models.TextField(default='', blank=True, null=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductReview'
        verbose_name_plural = 'ProductReviews'
        db_table = 'product_review'

    def __str__(self):
        return 'Review Text: '+ str(self.review_text)

    def save(self, *args, **kwargs):
        super(ProductReview,self).save(*args, **kwargs)
        if self.product:
            average_rating = ProductReview.objects.filter(product=self.product).aggregate(Avg('rating_number'))['rating_number__avg']
            product_obj = Product.objects.filter(id=self.product.id)
            product_obj.update(total_average_rating_number=average_rating)


class ProductReviewReply(AbstractTimeStamp):
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE, null=True, blank=True, related_name='product_review_reply_review')
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             related_name='product_review_reply_user', blank=True, null=True)
    review_text = models.TextField(default='', blank=True, null=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductReviewReply'
        verbose_name_plural = 'ProductReviewsReply'
        db_table = 'product_review_reply'

    def __str__(self):
        return 'Review Reply Text: '+ str(self.review_text)


class ProductCombinationMedia(AbstractTimeStamp):
    CHOICES = [
        ('COMPLETE', 'Complete'),
        ('IN_QUEUE', 'In_Queue'),
        ('IN_PROCESSING', 'In_Processing'),
    ]

    def validate_file_extension(value):
        import os
        from django.core.exceptions import ValidationError
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.jpg', '.png', '.jpeg']
        if not ext.lower() in valid_extensions:
            raise ValidationError('Unsupported file extension.')

    file = models.FileField(upload_to='products', validators=[
                            validate_file_extension])
    status = models.CharField(
        max_length=20, choices=CHOICES, default=CHOICES[0][0])

    class Meta:
        verbose_name = 'ProductCombinationMedia'
        verbose_name_plural = 'ProductCombinationMedias'
        db_table = 'product_combination_medias'

    def __str__(self):
        return self.status


class VariantType(AbstractTimeStamp):
    title = models.CharField(
        max_length=500, null=False, blank=False, default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'VariantType'
        verbose_name_plural = 'VariantTypes'
        db_table = 'variant_types'

    def __str__(self):
        return self.title


class TextColor(AbstractTimeStamp):
    title = models.CharField(
        max_length=255, null=False, blank=False, default="")
    code = models.CharField(
        max_length=20, null=False, blank=False, default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'TextColor'
        verbose_name_plural = 'TextColors'
        db_table = 'text_color'

    def __str__(self):
        return self.title


class FlashDealInfo(AbstractTimeStamp):
    title = models.CharField(
        max_length=255, null=False, blank=False, default="")
    background_color = models.CharField(
        max_length=255, null=True, blank=True, default="")
    text_color = models.ForeignKey(
        TextColor, on_delete=models.PROTECT, related_name='flash_deal_info_text_color', null=True, blank=True)
    banner = models.ImageField(
        upload_to='flash_deal_info', blank=True, null=True)
    start_date = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    end_date = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)
    is_featured = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        verbose_name = 'FlashDealInfo'
        verbose_name_plural = 'FlashDealInfos'
        db_table = 'flash_deal_info'

    def __str__(self):
        return self.title


class FlashDealProduct(AbstractTimeStamp):
    flash_deal_info = models.ForeignKey(
        FlashDealInfo, on_delete=models.PROTECT, related_name='flash_deal_product_flash_deal_info', null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='flash_deal_product_product', null=False, blank=False)
    discount_type = models.ForeignKey(
        DiscountTypes, on_delete=models.PROTECT, related_name='flash_deal_product_discount_type', null=True, blank=True)
    discount_amount = models.FloatField(
        max_length=255, null=True, blank=True, default=0)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'FlashDealProduct'
        verbose_name_plural = 'FlashDealProducts'
        db_table = 'flash_deal_product'

    def __str__(self):
        return self.product.title


class Inventory(AbstractTimeStamp):
    initial_quantity = models.IntegerField(null=True, blank=True, default=0)
    current_quantity = models.IntegerField(null=True, blank=True, default=0)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='inventory_product')

    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'
        db_table = 'inventory'

    def __str__(self):
        return self.product.title


class ProductFilterAttributes(AbstractTimeStamp):
    filter_attribute = models.ForeignKey(
        FilterAttributes, related_name='product_filter_attributes_filter_attribute', blank=True, null=True, on_delete=models.CASCADE)
    attribute_value = models.ForeignKey(
        AttributeValues, related_name='product_filter_attributes_attribute_value', blank=True, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='product_filter_attributes_product', blank=True, null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductFilterAttribute'
        verbose_name_plural = 'ProductFilterAttributes'
        db_table = 'product_filter_attributes'

    def __str__(self):
        return  'Product: ' + self.product.title


class Warranty(AbstractTimeStamp):
    title = models.CharField(max_length=800, default='')
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'Warranty'
        verbose_name_plural = 'Warranties'
        db_table = 'warranty'

    def __str__(self):
        return  self.title


class ProductWarranty(AbstractTimeStamp):
    WARRANTY_VALUE_TYPE = [
        ('PERCENTAGE', '%'),
        ('FIX', 'Fix')]

    product = models.ForeignKey(Product, related_name='product_warranty_product', blank=True, null=True, on_delete=models.PROTECT)
    warranty = models.ForeignKey(Warranty, related_name='product_warranty_warranty', blank=True, null=True, on_delete=models.PROTECT)
    warranty_value = models.IntegerField()
    warranty_value_type = models.CharField(max_length=20, choices=WARRANTY_VALUE_TYPE, default=WARRANTY_VALUE_TYPE[0][0])
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductWarranty'
        verbose_name_plural = 'ProductWarranties'
        db_table = 'product_warranty'

    def __str__(self):
        return  'id: ' + str(self.id) + ' product: ' + self.product.title + ' warranty: ' + self.warranty.title


class SavePc(AbstractTimeStamp):
    title = models.CharField(max_length=300, default='')
    description = models.TextField(default='', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT,related_name='save_pc_user', blank=True, null=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'SavePc'
        verbose_name_plural = 'SavePcs'
        db_table = 'save_pc'

    def __str__(self):
        return  'id: ' + str(self.id) + ' title: ' + self.title + ' user: ' + self.user.email


class SavePcItems(AbstractTimeStamp):
    save_pc = models.ForeignKey(SavePc, on_delete=models.CASCADE, related_name='save_pc_items_save_pc', blank=False, null=False)
    sub_category = models.ForeignKey(SubCategory, related_name='save_pc_items_sub_category', blank=False, null=True, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, related_name='save_pc_items_product', blank=True, null=True, on_delete=models.PROTECT)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'SavePcItems'
        verbose_name_plural = 'SavePcItems'
        db_table = 'save_pc_items'

    def __str__(self):
        return  'id: ' + str(self.id) + ' sub_category: ' + self.sub_category.title + ' product: ' + self.product.title


class OfferCategory(AbstractTimeStamp):
    title = models.CharField(
        max_length=100, null=False, blank=False, default="", help_text="name")
    ordering_number = models.IntegerField(null=False, blank=False, default=0)

    class Meta:
        verbose_name = 'OfferCategory'
        verbose_name_plural = 'OfferCategories'
        db_table = 'offer_category'

    def __str__(self):
        return 'id: ' + str(self.id) + ' Title: ' + self.title


class Offer(AbstractTimeStamp):
    CHOICES = [
        ('per', 'Percentage'),
        ('flat', 'Flat'),]
    title = models.CharField(max_length=100, null=False, blank=False, default="", help_text="name")
    product_category = models.ForeignKey(
        Category, related_name='offer_product_category', blank=True, null=True, on_delete=models.PROTECT)
    offer_category = models.ForeignKey(
        OfferCategory, related_name='offer_offer_category', blank=True, null=True, on_delete=models.PROTECT)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    thumbnail = models.FileField(upload_to='offers', blank=True, null=True)
    short_description = models.CharField(max_length=800, default='', null=True, blank=True)
    full_description = models.TextField(default='', null=True, blank=True)
    discount_price = models.FloatField(max_length=255, null=True, blank=True, default=0)
    discount_price_type = models.ForeignKey(DiscountTypes, on_delete=models.PROTECT, related_name='offer_discount_type', null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'
        db_table = 'offer'

    def __str__(self):
        return f"{self.pk}"


class OfferProduct(AbstractTimeStamp):
    offer = models.ForeignKey(Offer, related_name='offer_product_offer', blank=True, null=True, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, related_name='offer_offer_product', blank=True, null=True, on_delete=models.PROTECT)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'OfferProduct'
        verbose_name_plural = 'OfferProducts'
        db_table = 'offer_products'

    def __str__(self):
        return f"{self.pk}"
