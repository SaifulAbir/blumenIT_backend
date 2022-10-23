from email.policy import default
from hashlib import blake2b
from itertools import product
from statistics import mode
from turtle import back
from django.db import models
from ecommerce.models import AbstractTimeStamp
from vendor.models import Vendor
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
from user.models import User, CustomerProfile
import string
import random

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
        return self.title

class Category(AbstractTimeStamp):
    title = models.CharField(
        max_length=100, null=False, blank=False, default="", help_text="name")
    ordering_number = models.IntegerField(null=True, blank=True, default=0)
    type = models.CharField(max_length=100, null=True, blank=True, default="")
    subtitle = models.TextField(null=False, blank=False, default="")
    logo = models.ImageField(
        upload_to='product_category', blank=True, null=True)
    cover = models.ImageField(
        upload_to='product_category', blank=True, null=True)
    banner = models.ImageField(
        upload_to='product_category', blank=True, null=True)
    icon = models.ImageField(
        upload_to='product_category', blank=True, null=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)
    filtering_attributes = models.ForeignKey(Attribute, on_delete=models.PROTECT,
                               related_name='category_filtering_attributes', blank=True, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'category'

    def __str__(self):
        return self.title


class SubCategory(AbstractTimeStamp):
    title = models.CharField(
        max_length=100, null=False, blank=False, default="", help_text="name")
    is_active = models.BooleanField(null=False, blank=False, default=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='sub_category_category')

    class Meta:
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'
        db_table = 'sub_category'

    def __str__(self):
        return self.title


class SubSubCategory(AbstractTimeStamp):
    title = models.CharField(
        max_length=100, null=False, blank=False, default="", help_text="name")
    is_active = models.BooleanField(null=False, blank=False, default=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='sub_sub_category_category')
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.PROTECT, related_name='sub_sub_category_sub_category')

    class Meta:
        verbose_name = 'SubSubCategory'
        verbose_name_plural = 'SubSubCategories'
        db_table = 'sub_sub_category'

    def __str__(self):
        return self.title


class Brand(AbstractTimeStamp):
    title = models.CharField(
        max_length=100, null=False, blank=False, default="")
    logo = models.ImageField(upload_to='brand', blank=True, null=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

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

class ShippingClass(AbstractTimeStamp):
    title = models.CharField(max_length=800, default='', help_text="name")
    description = models.TextField(default='', null=False, blank=False)
    delivery_charge = models.FloatField(max_length=255, null=False, blank=False, default=0)
    class Meta:
        verbose_name = 'ShippingClass'
        verbose_name_plural = 'ShippingClasses'
        db_table = 'shipping_class'

    def __str__(self):
        return self.title

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
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('REMOVE', 'Remove')]

    title = models.CharField(max_length=800, default='')
    slug = models.SlugField(
        null=False, allow_unicode=True, blank=True, max_length=255)
    sku = models.CharField(max_length=500, null=True,
                           blank=True, default="")
    warranty = models.CharField(
        max_length=255, blank=True, null=True, help_text="eg: 1 year or 6 months")
    full_description = models.TextField(default='', null=False, blank=False)
    short_description = models.CharField(max_length=800, default='', null=False, blank=False)
    active_short_description = models.BooleanField(default=True)
    status = models.CharField(
        max_length=20, choices=PRODUCT_STATUSES, default=PRODUCT_STATUSES[0][0])
    is_featured = models.BooleanField(null=False, blank=False, default=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT,
                               related_name='product_vendor', blank=True, null=True)
    category = models.ForeignKey(
        Category, related_name='product_category', blank=False, null=True, on_delete=models.PROTECT)
    sub_category = models.ForeignKey(
        SubCategory, related_name='product_sub_category', blank=True, null=True, on_delete=models.PROTECT)
    sub_sub_category = models.ForeignKey(
        SubSubCategory, related_name='product_sub_sub_category', blank=True, null=True, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, related_name='product_brand',
                              blank=True, null=True, on_delete=models.PROTECT)
    unit = models.ForeignKey(Units, related_name="product_unit",
                             blank=True, null=True, on_delete=models.PROTECT)
    price = models.FloatField(
        max_length=255, null=False, blank=False, default=0, help_text="Unit price")
    old_price = models.FloatField(
        max_length=255, null=False, blank=False, default=0)
    purchase_price = models.FloatField(
        max_length=255, null=False, blank=False, default=0)
    pre_payment_amount = models.FloatField(
        max_length=255, null=False, blank=False, default=0)
    tax_in_percent = models.IntegerField(null=True, blank=True, default=0)
    vat = models.IntegerField(null=True, blank=True, default=0)
    discount_type = models.ForeignKey(
        DiscountTypes, related_name="product_discount_type", null=True, blank=True, on_delete=models.PROTECT)
    discount_amount = models.FloatField(
        max_length=255, null=True, blank=True, default=0)
    discount_start_date = models.DateTimeField(null=True, blank=True)
    discount_end_date = models.DateTimeField(null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    total_quantity = models.IntegerField(null=False, blank=False, default=0)
    shipping_cost = models.FloatField(
        max_length=255, null=True, blank=True, default=0)
    shipping_cost_multiply = models.BooleanField(
        null=True, blank=True, default=False)
    total_shipping_cost = models.FloatField(
        max_length=255, null=True, blank=True, default=0)
    shipping_time = models.IntegerField(
        null=False, blank=False, default=0, help_text="eg: Days in count.")
    shipping_class = models.ForeignKey(
        ShippingClass, related_name="product_shipping_class", null=True, blank=True, on_delete=models.PROTECT)
    thumbnail = models.FileField(upload_to='products', blank=True, null=True)
    youtube_link = models.URLField(null=True, blank=True)
    video_link = models.URLField(null=True, blank=True)
    external_link = models.URLField(null=True, blank=True)
    external_link_button_text = models.CharField(max_length=500, null=True, blank=True)
    sell_count = models.BigIntegerField(null=True, blank=True, default=0)
    minimum_purchase_quantity = models.IntegerField(null=True, blank=True, default=0)
    bar_code = models.CharField(max_length=255, blank=False, null=False, default='')
    refundable = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    in_house_product = models.BooleanField(default=False)
    cash_on_delivery = models.BooleanField(default=False)
    todays_deal = models.BooleanField(default=False)
    show_stock_quantity = models.BooleanField(default=False)
    low_stock_quantity_warning = models.IntegerField(null=True, blank=True, default=0)
    video_provider = models.ForeignKey(
        ProductVideoProvider, related_name="product_video_provider", null=True, blank=True, on_delete=models.PROTECT)
    vat_type = models.ForeignKey(
        VatType, related_name="product_vat_type", null=True, blank=True, on_delete=models.PROTECT)
    product_condition = models.ForeignKey(
        ProductCondition, related_name="product_product_condition", null=True, blank=True, on_delete=models.PROTECT)
    is_published = models.BooleanField(null=False, blank=False, default=True)

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
        return self.title + '-' + self.vendor.vendor_admin.email

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        try:
            if self.shipping_cost_multiply == True:
                self.total_shipping_cost = self.shipping_cost * self.shipping_cost
                # product.save()
                super(Product, self).save(*args, **kwargs)
            elif self.shipping_cost_multiply == False:
                self.total_shipping_cost = self.shipping_cost
                super(Product, self).save(*args, **kwargs)
            else:
                super(Product, self).save(*args, **kwargs)
        except:
            print("Error in product combination save.")


def pre_save_product(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        # chars = string.ascii_lowercase + string.digits
        # size = 10
        # instance.sku = ''.join(random.choice(chars) for _ in range(size))


pre_save.connect(pre_save_product, sender=Product)

class Specification(AbstractTimeStamp):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='specification_product')
    title = models.CharField(max_length=800, default='', help_text="name")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'Specification'
        verbose_name_plural = 'Specifications'
        db_table = 'specification'

    def __str__(self):
        return self.title

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
        return self.key

class ProductAttributes(AbstractTimeStamp):
    title = models.CharField(
        max_length=100, null=False, blank=False, default="")
    attribute = models.ForeignKey(
        Attribute, related_name='product_attributes_attribute', blank=True, null=True, on_delete=models.PROTECT)
    product = models.ForeignKey(
        Product, related_name='product_attributes_product', blank=True, null=True, on_delete=models.PROTECT)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductAttribute'
        verbose_name_plural = 'ProductAttributes'
        db_table = 'product_attributes'

    def __str__(self):
        return self.product.title + ' ' + self.title

class ProductAttributeValues(AbstractTimeStamp):
    product_attribute = models.ForeignKey(ProductAttributes, on_delete=models.PROTECT,
                               related_name='product_attribute_values_product_attribute', blank=False, null=False)
    value = models.CharField(
        max_length=255, null=False, blank=False, default="")
    product = models.ForeignKey(
        Product, related_name='product_attributes_values_product', blank=True, null=True, on_delete=models.PROTECT)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductAttributeValue'
        verbose_name_plural = 'ProductAttributeValues'
        db_table = 'product_attribute_value'

    def __str__(self):
        return self.product_attribute.product.title + ' ' + self.product_attribute.title + ' ' + self.value

class Color(AbstractTimeStamp):
    title = models.CharField(
        max_length=255, null=False, blank=False, default="")
    color_code = models.CharField(
        max_length=20, null=False, blank=False, default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'
        db_table = 'color'

    def __str__(self):
        return self.title

class ProductColor(AbstractTimeStamp):
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True,
                            blank=True, related_name='product_color_color', default="")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False,
                                blank=False, related_name='product_color_product', default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductColor'
        verbose_name_plural = 'ProductColors'
        db_table = 'product_color'

    def __str__(self):
        return self.product.title + ' ' + self.color.title
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
    attribute = models.ForeignKey(ProductAttributes, on_delete=models.CASCADE, null=True,
                            blank=True, related_name='Product_variation_product_attribute')
    variation = models.CharField(
        max_length=255, null=False, blank=False, default="")
    variation_price = models.FloatField(null=False, blank=False, default=0)
    sku = models.CharField(max_length=500, null=True,blank=True, default="")
    quantity = models.IntegerField(null=False, blank=False, default=0)
    image = models.FileField(upload_to='product_variation', validators=[validate_file_extension])
    product_color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, null=True,
                            blank=True, related_name='Product_variation_color')
    total_price = models.FloatField(null=False, blank=False, default=0)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductVariation'
        verbose_name_plural = 'ProductVariations'
        db_table = 'product_variation'

    def __str__(self):
        return self.title


class ProductCombinations(AbstractTimeStamp):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='product_combinations_product')
    product_attribute = models.ForeignKey(
        ProductAttributes, related_name="product_combinations_product_attributes", null=True, blank=True, on_delete=models.PROTECT)
    product_attribute_value = models.CharField(
        max_length=500, null=False, blank=False, default="")
    product_attribute_price = models.FloatField(
        max_length=255, null=True, blank=True, default=0)
    product_attribute_color_code = models.CharField(
        max_length=100, null=True, blank=True, default="")

    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductCombination'
        verbose_name_plural = 'ProductCombinations'
        db_table = 'product_combinations'

    def __str__(self):
        return str(self.id) + '-'+self.product.title+'-'+self.product_attribute_value

    # def __str__(self):
    #     # title = self.product.title
    #     # combine = title + ' ' + self.product_attribute.title + \
    #     #     ' ' + self.product_attribute_value

    #     combine = self.product_attribute_value
    #     return combine


class Tags(AbstractTimeStamp):
    title = models.CharField(
        max_length=100, null=False, blank=False, default="", unique=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='tags_product', null=True, blank=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        db_table = 'tags'

    def __str__(self):
        return self.title

    # def save(self, force_insert=False, force_update=False):
    #     self.title = self.title.upper()
    #     super(Tags, self).save(force_insert, force_update)


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
        # return self.product.title + ' ' + self.tag.title


class ProductMedia(AbstractTimeStamp):
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
        Product, on_delete=models.PROTECT, related_name='product_media_product', null=True, blank=True)
    file = models.FileField(upload_to='products', validators=[
                            validate_file_extension])
    status = models.CharField(
        max_length=20, choices=CHOICES, default=CHOICES[0][0])
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductMedia'
        verbose_name_plural = 'ProductMedias'
        db_table = 'product_medias'

    def __str__(self):
        return self.product.title

class ProductImages(AbstractTimeStamp):
    def validate_file_extension(value):
        import os
        from django.core.exceptions import ValidationError
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.jpg', '.png', '.jpeg']
        if not ext.lower() in valid_extensions:
            raise ValidationError('Unsupported file extension.')

    image = models.FileField(upload_to='products', validators=[validate_file_extension])
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='product_images_product', null=True, blank=True)

    class Meta:
        verbose_name = 'ProductImage'
        verbose_name_plural = 'ProductImages'
        db_table = 'product_images'

    def __str__(self):
        return self.product.title
class ProductReview(AbstractTimeStamp):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,
                                blank=True, related_name='product_review_product')
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT,
                               related_name='product_review_vendor', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             related_name='product_review_user', blank=True, null=True)
    rating_number = models.IntegerField(default=0)
    review_text = models.TextField(default='', blank=True, null=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductReview'
        verbose_name_plural = 'ProductReviews'
        db_table = 'product_review'

    def __str__(self):
        return str(self.pk)


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

    product_combination = models.ForeignKey(
        ProductCombinations, on_delete=models.PROTECT, related_name='product_media_product_combination')
    file = models.FileField(upload_to='products', validators=[
                            validate_file_extension])
    status = models.CharField(
        max_length=20, choices=CHOICES, default=CHOICES[0][0])

    class Meta:
        verbose_name = 'ProductCombinationMedia'
        verbose_name_plural = 'ProductCombinationMedias'
        db_table = 'product_combination_medias'

    def __str__(self):
        # return self.pk
        return self.product_combination.product.title


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


class ProductCombinationsVariants(AbstractTimeStamp):
    product_combination = models.ForeignKey(
        ProductCombinations, related_name="product_combinations_variant_product_combination", null=True, blank=True, on_delete=models.PROTECT)
    product = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.PROTECT, related_name='product_combinations_variant_product')
    variant_type = models.ForeignKey(
        VariantType, related_name="product_combinations_variant_variant_type", null=True, blank=True, on_delete=models.PROTECT)
    variant_value = models.CharField(max_length=500, null=True, blank=True)
    variant_price = models.FloatField(
        max_length=255, null=True, blank=True, default=0)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    discount_type = models.ForeignKey(
        DiscountTypes, related_name="product_combinations_variant_discount_type", null=True, blank=True, on_delete=models.PROTECT)
    discount_amount = models.FloatField(
        max_length=255, null=True, blank=True, default=0)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductCombinationsVariant'
        verbose_name_plural = 'ProductCombinationsVariants'
        db_table = 'product_combinations_variant'

    def __str__(self):
        # return self.variant_type.title + ' ' + self.variant_value
        return str(self.id)+'-'+self.product_combination.product.title+'-'+self.variant_type.title+'-'+self.variant_value

    def save(self, *args, **kwargs):
        super(ProductCombinationsVariants, self).save(*args, **kwargs)
        try:
            product = Product.objects.get(id=self.product.id)
            p_cs = ProductCombinationsVariants.objects.filter(
                product=self.product)
            total = 0
            for p_c in p_cs:
                total += p_c.quantity
            product.total_quantity = total
            product.save()
        except:
            print("Error in product combination save.")


class TextColor(AbstractTimeStamp):
    title = models.CharField(
        max_length=255, null=False, blank=False, default="")
    code = models.CharField(
        max_length=20, null=False, blank=False, default="")

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
        max_length=255, null=False, blank=False, default="")
    text_color = models.ForeignKey(
        TextColor, on_delete=models.PROTECT, related_name='flash_deal_info_text_color')
    banner = models.ImageField(
        upload_to='flash_deal_info', blank=True, null=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'FlashDealInfo'
        verbose_name_plural = 'FlashDealInfos'
        db_table = 'flash_deal_info'

    def __str__(self):
        return self.title

class FlashDealProduct(AbstractTimeStamp):
    flashDealInfo = models.ForeignKey(
        FlashDealInfo, on_delete=models.PROTECT, related_name='flash_deal_product_flash_deal_info')
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='flash_deal_product_product')
    discount_type = models.ForeignKey(
        DiscountTypes, on_delete=models.PROTECT, related_name='flash_deal_product_discount_type')
    discount_amount = models.FloatField(
        max_length=255, null=True, blank=True, default=0)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'FlashDealProduct'
        verbose_name_plural = 'FlashDealProducts'
        db_table = 'flash_deal_product'

    def __str__(self):
        return self.title


class Inventory(AbstractTimeStamp):
    initial_quantity = models.IntegerField(null=False, blank=False, default=0)
    current_quantity = models.IntegerField(null=False, blank=False, default=0)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='inventory_product')

    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'
        db_table = 'inventory'

    def __str__(self):
        return self.product.title + ' ' + self.initial_quantity + ' ' + self.current_quantity

class InventoryVariation(AbstractTimeStamp):
    inventory = models.ForeignKey(
        Inventory, on_delete=models.PROTECT, related_name='inventory_variation_inventory')
    variation_initial_quantity = models.IntegerField(null=True, blank=True, default=0)
    variation_current_quantity = models.IntegerField(null=True, blank=True, default=0)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='inventory_variation_product')

    class Meta:
        verbose_name = 'InventoryVariation'
        verbose_name_plural = 'InventoryVariations'
        db_table = 'inventory_variation'

    def __str__(self):
        return self.inventory.product.title + ' ' + self.variation_initial_quantity + ' ' + self.variation_current_quantity