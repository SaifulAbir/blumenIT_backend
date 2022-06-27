from statistics import mode
from django.db import models
from ecommerce.models import AbstractTimeStamp
from vendor.models import Vendor
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
from user.models import User, CustomerProfile

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_category_category')

    class Meta:
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'
        db_table = 'sub_category'

    def __str__(self):
        return self.title

class SubSubCategory(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False, default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_sub_category_category')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='sub_sub_category_sub_category')

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
    warranty  = models.CharField(max_length=255, blank=True, help_text="eg: 1 year or 6 months")
    full_description = models.TextField(default='')
    short_description = models.CharField(max_length=800, default='')
    status = models.CharField(max_length=20, choices=PRODUCT_STATUSES, default=PRODUCT_STATUSES[0][0])
    is_featured = models.BooleanField(null=False, blank=False, default=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,related_name='product_vendor', blank=False, null=False)
    category = models.ForeignKey(Category, related_name='product_category', blank=False, null=True, on_delete=models.SET_NULL)
    sub_category = models.ForeignKey(SubCategory, related_name='product_sub_category', blank=True, null=True, on_delete=models.SET_NULL)
    sub_sub_category = models.ForeignKey(SubSubCategory, related_name='product_sub_sub_category', blank=True, null=True, on_delete=models.SET_NULL)
    brand = models.ForeignKey(Brand, related_name='product_brand', blank=True, null=True, on_delete=models.SET_NULL)
    unit = models.ForeignKey(Units, related_name="product_unit", blank=True, null=True, on_delete=models.SET_NULL)
    unit_price = models.FloatField(max_length=255, null=False, blank=False, default=0)
    purchase_price = models.FloatField(max_length=255, null=False, blank=False, default=0)
    tax_in_percent = models.IntegerField(null=True, blank=True, default=0)
    discount_type = models.ForeignKey(DiscountTypes, related_name="product_discount_type", null=True, blank=True, on_delete=models.SET_NULL)
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
    title = models.CharField(max_length=100, null=False, blank=False, default="")
    color_code = models.CharField(max_length=100, null=True, blank=True, default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'
        db_table = 'colors'

    def __str__(self):
        return self.title

class Attributes(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False, default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'Attribute'
        verbose_name_plural = 'Attributes'
        db_table = 'attributes'

    def __str__(self):
        return self.title

class ProductColors(AbstractTimeStamp):
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE, related_name="product_colors_product", default="")
    color = models.ForeignKey(Colors, on_delete=models.CASCADE, null=False, blank=False, related_name='product_colors', default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductColor'
        verbose_name_plural = 'ProductColors'
        db_table = 'product_colors'

    def __str__(self):
        return self.product.title + ' ' + self.color.title


class ProductAttributes(AbstractTimeStamp):
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE, related_name="product_attributes_product")
    attribute = models.ForeignKey(Attributes, on_delete=models.CASCADE, null=False, blank=False, related_name='product_attributes_attributes')
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductAttribute'
        verbose_name_plural = 'ProductAttributes'
        db_table = 'product_attributes'

    def __str__(self):
        return self.product.title + ' ' + self.attribute.title

    @property
    def product_attribute_name(self):
        return self.attribute.title


class ProductAttributesValues(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False, default="")
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE, related_name="product_attributes_values_product")
    product_attribute = models.ForeignKey(ProductAttributes, on_delete=models.CASCADE, related_name='product_attributes_values_product_attributes')

    class Meta:
        verbose_name = 'ProductAttributesValue'
        verbose_name_plural = 'ProductAttributesValues'
        db_table = 'product_attributes_values'

    def __str__(self):
        return self.title

    @property
    def product_attribute_name(self):
        return self.product_attribute.attribute.title

class ProductCombinations(AbstractTimeStamp):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_combinations_product')
    sku = models.CharField(max_length=500, null=False, blank=False)
    varient = models.CharField(max_length=500, null=False, blank=False)
    varient_price = models.FloatField(max_length=255, null=False, blank=False, default=0)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    product_color = models.ForeignKey(ProductColors, related_name="product_combinations_product_color", null=True, blank=True, on_delete=models.SET_NULL)
    product_attribute = models.ForeignKey(ProductAttributes, related_name="product_combinations_product_attributes", null=True, blank=True, on_delete=models.SET_NULL)
    product_attribute_values = models.ForeignKey(ProductAttributesValues, related_name="product_combinations_product_attributes_values", null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductCombination'
        verbose_name_plural = 'ProductCombinations'
        db_table = 'product_combinations'

    def __str__(self):
        title = self.product.title
        if self.product_color:
            color = self.product_color.color.title
        else:
            color = ''
        if self.product_attribute:
            attribute = self.product_attribute.attribute.title
        else:
            attribute = ''
        if self.product_attribute_values:
            attribute_value = self. product_attribute_values.title
        else:
            attribute_value = ''
        combine = title + ' ' + color + ' ' + attribute + ' '+ attribute_value
        return combine

    @property
    def product_color_name(self):
        return self.product_color.color.title

    @property
    def product_color_code(self):
        return self.product_color.color.color_code

    def save(self, *args, **kwargs):
        super(ProductCombinations, self).save(*args, **kwargs)
        try:
            product = Product.objects.get(id=self.product.id)
            p_cs = ProductCombinations.objects.filter(product=self.product)
            total = 0
            for p_c in p_cs:
                total += p_c.quantity
            product.total_quantity = total
            product.save()
        except :
            print("Error in product combination save.")
        

class ProductTags(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False, default="")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False, related_name='product_tags_product', default="")
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
    status = models.CharField(max_length=20, choices=CHOICES, default=CHOICES[0][0])
    video_type = models.CharField(max_length=50, null=True, blank=True, choices=VIDEO_TYPES)

    class Meta:
        verbose_name = 'ProductMedia'
        verbose_name_plural = 'ProductMedias'
        db_table = 'product_medias'

    def __str__(self):
        return self.product.title

class ProductReview(AbstractTimeStamp):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False, related_name='product_review_product', default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_review_user',blank=True, null=True)
    rating_number = models.IntegerField(default=0)
    review_text = models.TextField(default='',blank=True, null=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)
    class Meta:
        verbose_name = 'ProductReview'
        verbose_name_plural = 'ProductReviews'
        db_table = 'product_review'

    def __str__(self):
        return str(self.pk)

