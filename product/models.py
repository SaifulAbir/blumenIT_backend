from statistics import mode
from django.db import models
from ecommerce.models import AbstractTimeStamp
from vendor.models import Vendor
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
from user.models import User, CustomerProfile

class Category(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'category'

    def __str__(self):
        return self.title

class SubCategory(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False)

class SubSubCategory(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False)

class Brand(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False)

class Units(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False)

class DiscountTypes(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False)

class Product(AbstractTimeStamp):
    PRODUCT_STATUSES = [
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active')]

    title = models.CharField(max_length=500, null=False, blank=False)
    slug  = models.SlugField(null=False, allow_unicode=True, blank=True)
    warranty  = models.CharField(max_length=255, blank=True, help_text="eg: 1 year or 6 months")
    full_description = models.TextField(default='')
    short_description = models.CharField(max_length=800, default='')
    status = models.CharField(max_length=20, choices=PRODUCT_STATUSES, default=PRODUCT_STATUSES[0][0])
    is_featured = models.BooleanField(null=False, blank=False, default=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,related_name='product_vendor', blank=False, null=False)
    category = models.ForeignKey(Category, related_name='category', blank=False, null=True, on_delete=models.SET_NULL)
    sub_category = models.ForeignKey(SubCategory, related_name='sub_category', blank=True, null=True, on_delete=models.SET_NULL)
    sub_sub_category = models.ForeignKey(SubSubCategory, related_name='sub_sub_category', blank=True, null=True, on_delete=models.SET_NULL)
    brand = models.ForeignKey(Brand, related_name='brand', blank=True, null=True, on_delete=models.SET_NULL)
    unit = models.ForeignKey(Units, related_name="unit", blank=True, null=True, on_delete=models.SET_NULL)
    unit_price = models.FloatField(max_length=255, null=False, blank=False, default=0)
    purchase_price = models.FloatField(max_length=255, null=False, blank=False, default=0)
    tax_in_percent = models.IntegerField(null=True, blank=True, default=0)
    discount_type = models.ForeignKey(DiscountTypes, related_name="discount_type", null=True, blank=True, on_delete=models.SET_NULL)
    discount_amount = models.FloatField(max_length=255, null=True, blank=True, default=0)
    total_quantity = models.IntegerField(null=False, blank=False, default=0)
    shipping_cost = models.FloatField(max_length=255, null=True, blank=True, default=0)
    shipping_cost_multiply = models.BooleanField(null=True, blank=True, default=False)
    total_shipping_cost = models.FloatField(max_length=255, null=True, blank=True, default=0)
    shipping_time = models.IntegerField(null=True, blank=True, default=0, help_text="eg: Days in count.")
    thumbnail = models.FileField(upload_to='products', blank=True, null=True)
    youtube_link = models.URLField(null=True, blank=True)



    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'products'

    def __str__(self):
        return self.title

def pre_save_product(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_product, sender=Product)

class Colors(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False)

class Attributes(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False)

class ProductColors(AbstractTimeStamp):
    color = models.ForeignKey(Colors, on_delete=models.PROTECT, related_name='product_colors')

class ProductAttributes(AbstractTimeStamp):
    attribute = models.ForeignKey(Attributes, on_delete=models.Prefetch, related_name='product_attributes_attributes')

class ProductAttributesValues(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False)
    product_attribute = models.ForeignKey(ProductAttributes, on_delete=models.PROTECT, related_name='product_attributes_values_product_attributes')

class ProductCombinations(AbstractTimeStamp):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_combinations_product')
    sku = models.CharField(max_length=500, null=False, blank=False)
    varient = models.CharField(max_length=500, null=False, blank=False)
    varient_price = models.FloatField(max_length=255, null=False, blank=False, default=0)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    product_color = models.ForeignKey(ProductColors, related_name="product_colors", null=True, blank=True, on_delete=models.SET_NULL)
    product_attribute = models.ForeignKey(ProductAttributes, related_name="product_attributes", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'ProductCombination'
        verbose_name_plural = 'ProductCombinations'
        db_table = 'product_combinations'

    def __str__(self):
        return self.sku

class ProductTags(AbstractTimeStamp):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_tags_product')

class ProductMedia(AbstractTimeStamp):
    CHOICES = [
        ('IN_QUEUE', 'In_Queue'),
        ('IN_PROCESSING', 'In_Processing'),
        ('COMPLETE', 'Complete'),]

    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    VIDEO_TYPES = [
        ('UPDATE', 'Update'),
        ('THANK_YOU', 'Thank you'),
    ]

    def validate_file_extension(value):
        import os
        from django.core.exceptions import ValidationError
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.jpg', '.png', '.jpeg', '.mp4']
        if not ext.lower() in valid_extensions:
            raise ValidationError('Unsupported file extension.')

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_media_product')
    type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    file = models.FileField(upload_to='products', validators=[validate_file_extension])
    status = models.CharField(max_length=20, choices=CHOICES)
    video_type = models.CharField(max_length=50, null=True, blank=True, choices=VIDEO_TYPES)

    class Meta:
        verbose_name = 'ProductMedia'
        verbose_name_plural = 'ProductMedias'
        db_table = 'product_medias'

    def __str__(self):
        return self.product.title

class ProductReview(AbstractTimeStamp):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_review_product')

