from statistics import mode
from django.db import models
from ecommerce.models import AbstractTimeStamp
from vendor.models import Vendor
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
from user.models import User, CustomerProfile
import string
import random

class Category(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False, default="")
    logo = models.ImageField(upload_to='product_category', blank=True, null=True)
    cover = models.ImageField(upload_to='product_category', blank=True, null=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'category'

    def __str__(self):
        return self.title

class SubCategory(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False, default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='sub_category_category')

    class Meta:
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'
        db_table = 'sub_category'

    def __str__(self):
        return self.title

class SubSubCategory(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False, default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='sub_sub_category_category')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.PROTECT, related_name='sub_sub_category_sub_category')

    class Meta:
        verbose_name = 'SubSubCategory'
        verbose_name_plural = 'SubSubCategories'
        db_table = 'sub_sub_category'

    def __str__(self):
        return self.title

class Brand(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False, default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        db_table = 'brand'

    def __str__(self):
        return self.title

class Units(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False, default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'
        db_table = 'units'

    def __str__(self):
        return self.title

class DiscountTypes(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False, default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'DiscountType'
        verbose_name_plural = 'DiscountTypes'
        db_table = 'discount_types'

    def __str__(self):
        return self.title

class Product(AbstractTimeStamp):
    PRODUCT_STATUSES = [
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active')]

    title = models.CharField(max_length=500, null=False, blank=False, default="")
    slug  = models.SlugField(null=False, allow_unicode=True, blank=True)
    # sku = models.CharField(max_length=500, null=True, blank=True, default="", unique=True)
    sku = models.CharField(max_length=500, null=True, blank=True, default="")
    warranty  = models.CharField(max_length=255, blank=True, help_text="eg: 1 year or 6 months")
    full_description = models.TextField(default='')
    short_description = models.CharField(max_length=800, default='')
    status = models.CharField(max_length=20, choices=PRODUCT_STATUSES, default=PRODUCT_STATUSES[0][0])
    is_featured = models.BooleanField(null=False, blank=False, default=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT,related_name='product_vendor', blank=False, null=False)
    category = models.ForeignKey(Category, related_name='product_category', blank=False, null=True, on_delete=models.PROTECT)
    sub_category = models.ForeignKey(SubCategory, related_name='product_sub_category', blank=True, null=True, on_delete=models.PROTECT)
    sub_sub_category = models.ForeignKey(SubSubCategory, related_name='product_sub_sub_category', blank=True, null=True, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, related_name='product_brand', blank=True, null=True, on_delete=models.PROTECT)
    unit = models.ForeignKey(Units, related_name="product_unit", blank=True, null=True, on_delete=models.PROTECT)
    unit_price = models.FloatField(max_length=255, null=False, blank=False, default=0)
    purchase_price = models.FloatField(max_length=255, null=False, blank=False, default=0)
    tax_in_percent = models.IntegerField(null=True, blank=True, default=0)
    discount_type = models.ForeignKey(DiscountTypes, related_name="product_discount_type", null=True, blank=True, on_delete=models.PROTECT)
    discount_amount = models.FloatField(max_length=255, null=True, blank=True, default=0)
    total_quantity = models.IntegerField(null=False, blank=False, default=0)
    shipping_cost = models.FloatField(max_length=255, null=True, blank=True, default=0)
    shipping_cost_multiply = models.BooleanField(null=True, blank=True, default=False)
    total_shipping_cost = models.FloatField(max_length=255, null=True, blank=True, default=0)
    shipping_time = models.IntegerField(null=True, blank=True, default=0, help_text="eg: Days in count.")
    thumbnail = models.FileField(upload_to='products', blank=True, null=True)
    youtube_link = models.URLField(null=True, blank=True)
    sell_count = models.BigIntegerField(null=True, blank=True, default=0)

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

class ProductAttribute(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False, default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)
    class Meta:
        verbose_name = 'ProductAttribute'
        verbose_name_plural = 'ProductAttributes'
        db_table = 'product_attributes'

    def __str__(self):
        return self.title

class ProductCombinations(AbstractTimeStamp):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_combinations_product')
    # sku = models.CharField(max_length=500, null=True, blank=True, unique=True)
    sku = models.CharField(max_length=500, null=True, blank=True)
    
    product_attribute = models.ForeignKey(ProductAttribute, related_name="product_combinations_product_attribute", null=False, blank=False, on_delete=models.PROTECT, default=0)
    product_attribute_value = models.CharField(max_length=500, null=False, blank=False, default="")
    product_attribute_color_code = models.CharField(max_length=100, null=False, blank=False, default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductCombination'
        verbose_name_plural = 'ProductCombinations'
        db_table = 'product_combinations'

    def __str__(self):
        title = self.product.title
        combine = title + ' ' + self.product_attribute.title
        return combine

class VariantType(AbstractTimeStamp):
    title = models.CharField(max_length=500, null=False, blank=False, default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'VariantType'
        verbose_name_plural = 'VariantTypes'
        db_table = 'variant_types'

    def __str__(self):
        return self.title

class ProductCombinationsVariants(AbstractTimeStamp):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_combinations_variant_product', null=False, blank=False)
    product_combination = models.ForeignKey(ProductCombinations, related_name="product_combinations_variant_product_combination", null=False, blank=False, on_delete=models.PROTECT)
    variant_type = models.ForeignKey(VariantType, related_name="product_combinations_variant_variant_type", null=True, blank=True, on_delete=models.PROTECT)
    variant_value = models.CharField(max_length=500, null=False, blank=False)
    variant_price = models.FloatField(max_length=255, null=False, blank=False, default=0)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    discount_type = models.ForeignKey(DiscountTypes, related_name="product_combinations_discount_type", null=True, blank=True, on_delete=models.PROTECT)
    discount_amount = models.FloatField(max_length=255, null=True, blank=True, default=0)

    class Meta:
        verbose_name = 'ProductCombinationsVariant'
        verbose_name_plural = 'ProductCombinationsVariants'
        db_table = 'product_combinations_variant'

    def __str__(self):
        return self.product.title + ' ' + self.variant_type.title + ' ' + self.variant_value

    def save(self, *args, **kwargs):
        super(ProductCombinationsVariants, self).save(*args, **kwargs)
        try:
            product = Product.objects.get(id=self.product.id)
            p_cs = ProductCombinationsVariants.objects.filter(product=self.product)
            total = 0
            for p_c in p_cs:
                total += p_c.quantity
            product.total_quantity = total
            product.save()
        except :
            print("Error in product combination save.")

class ProductTags(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False, default="")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=False, blank=False, related_name='product_tags_product', default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductTag'
        verbose_name_plural = 'ProductTags'
        db_table = 'product_tags'

    def __str__(self):
        return self.title

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

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_media_product')
    file = models.FileField(upload_to='products', validators=[validate_file_extension])
    status = models.CharField(max_length=20, choices=CHOICES, default=CHOICES[0][0])

    class Meta:
        verbose_name = 'ProductMedia'
        verbose_name_plural = 'ProductMedias'
        db_table = 'product_medias'

    def __str__(self):
        return self.product.title

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

    product_combination = models.ForeignKey(ProductCombinations, on_delete=models.PROTECT, related_name='product_media_product_combination')
    file = models.FileField(upload_to='products', validators=[validate_file_extension])
    status = models.CharField(max_length=20, choices=CHOICES, default=CHOICES[0][0])

    class Meta:
        verbose_name = 'ProductCombinationMedia'
        verbose_name_plural = 'ProductCombinationMedias'
        db_table = 'product_combination_medias'

    def __str__(self):
        return self.pk
        # return self.product_combination.product.title

class ProductReview(AbstractTimeStamp):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=False, blank=False, related_name='product_review_product', default="")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='product_review_user',blank=True, null=True)
    rating_number = models.IntegerField(default=0)
    review_text = models.TextField(default='',blank=True, null=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)
    class Meta:
        verbose_name = 'ProductReview'
        verbose_name_plural = 'ProductReviews'
        db_table = 'product_review'

    def __str__(self):
        return str(self.pk)