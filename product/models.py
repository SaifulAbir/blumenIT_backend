from django.db import models
from ecommerce.models import AbstractTimeStamp
from vendor.models import Vendor
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
from user.models import User, CustomerProfile


class ProductBrand(AbstractTimeStamp):
    name = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductBrand'
        verbose_name_plural = 'ProductBrands'
        db_table = 'productBrands'

    def __str__(self):
        return self.name

def pre_save_product_brand(sender, instance, *args, **kwargs):
        instance.name = instance.name.upper()
pre_save.connect(pre_save_product_brand, sender=ProductBrand)

class ProductCategory(AbstractTimeStamp):
    name = models.CharField(max_length=100, null=False, blank=False)
    logo = models.ImageField(upload_to='product_category', blank=True, null=True)
    cover = models.ImageField(upload_to='product_category', blank=True, null=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductCategory'
        verbose_name_plural = 'ProductCategories'
        db_table = 'productCategory'

    def __str__(self):
        return self.name

def pre_save_product_category(sender, instance, *args, **kwargs):
        instance.name = instance.name.upper()
pre_save.connect(pre_save_product_category, sender=ProductCategory)

class ProductSubCategory(AbstractTimeStamp):
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='product_sub_category')
    name = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductSubCategory'
        verbose_name_plural = 'ProductSubCategories'
        db_table = 'productSubCategory'

    def __str__(self):
        return self.name

def pre_save_product_sub_category(sender, instance, *args, **kwargs):
        instance.name = instance.name.upper()
pre_save.connect(pre_save_product_sub_category, sender=ProductSubCategory)

class ProductChildCategory(AbstractTimeStamp):
    sub_category = models.ForeignKey(ProductSubCategory, on_delete=models.PROTECT, related_name='product_sub_category')
    name = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductChildCategory'
        verbose_name_plural = 'ProductChildCategories'
        db_table = 'productChildCategory'

    def __str__(self):
        return self.name

def pre_save_product_child_category(sender, instance, *args, **kwargs):
        instance.name = instance.name.upper()
pre_save.connect(pre_save_product_child_category, sender=ProductChildCategory)

class Product(AbstractTimeStamp):
    PRODUCT_STATUSES = [
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active')]

    title = models.CharField(max_length=500, null=False, blank=False)
    slug  = models.SlugField(null=False, allow_unicode=True, blank=True)
    price = models.FloatField(max_length=255, null=False, blank=False, default=0)
    old_price = models.FloatField(max_length=255, null=True, blank=True, default=0)
    full_description = models.TextField(default='')
    short_description = models.CharField(max_length=800, default='')
    quantity = models.BigIntegerField(null=True, blank=True, default=0)
    quantity_left = models.BigIntegerField(null=True, blank=True, default=0, help_text="Automatic quantity decreased after order placed. Leave it empty for unlimited/manual quantity of the product.")
    warranty  = models.CharField(max_length=255, blank=True, help_text="eg: 1 year or 6 months")
    variation = models.CharField(max_length=255, blank=True)
    rating = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=PRODUCT_STATUSES, default=PRODUCT_STATUSES[0][0])
    is_featured = models.BooleanField(null=False, blank=False, default=False)
    product_category = models.ForeignKey(ProductCategory, related_name='category', blank=False, null=True, on_delete=models.PROTECT)
    product_sub_category = models.ForeignKey(ProductSubCategory, related_name='sub_category', blank=True, null=True, on_delete=models.PROTECT)
    product_child_category = models.ForeignKey(ProductChildCategory, related_name='child_category', blank=True, null=True, on_delete=models.PROTECT)
    product_brand = models.ForeignKey(ProductBrand, related_name='brand', blank=True, null=True, on_delete=models.SET_NULL)
    created_by = models.CharField(max_length=255, null=True, blank=True)
    thumbnail = models.FileField(upload_to='products', blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT,related_name='product_vendor', blank=False, null=False)
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

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_media')
    type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    file = models.FileField(upload_to='products', validators=[validate_file_extension])
    status = models.CharField(max_length=20, choices=CHOICES)
    video_type = models.CharField(max_length=50, null=True, blank=True, choices=VIDEO_TYPES)

    class Meta:
        verbose_name = 'ProductMedia'
        verbose_name_plural = 'ProductMedia'
        db_table = 'productMedia'

    def __str__(self):
        return self.product.title

class Tags(AbstractTimeStamp):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(null=False, blank=False, default=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT,related_name='tag_create_user', blank=True, null=True)

    class Meta:
        verbose_name = 'Tags'
        verbose_name_plural = 'Tags'
        db_table = 'tags'

    def __str__(self):
        return self.name

def pre_save_tags(sender, instance, *args, **kwargs):
        instance.name = instance.name.upper()
pre_save.connect(pre_save_tags, sender=Tags)

class ProductTags(AbstractTimeStamp):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name = 'product_tag', blank=True, null=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductTag'
        verbose_name_plural = 'ProductTags'
        db_table = 'productTags'

    def __str__(self):
        return self.name

class Colors(AbstractTimeStamp):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    is_active = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        verbose_name = 'Colors'
        verbose_name_plural = 'Colors'
        db_table = 'colors'

    def __str__(self):
        return self.name

def pre_save_colors(sender, instance, *args, **kwargs):
        instance.name = instance.name.upper()
pre_save.connect(pre_save_colors, sender=Colors)

class ProductColors(AbstractTimeStamp):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name = 'product_color', blank=True, null=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductColor'
        verbose_name_plural = 'ProductColors'
        db_table = 'productColors'

    def __str__(self):
        return self.name

class Sizes(AbstractTimeStamp):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'
        db_table = 'sizes'

    def __str__(self):
        return self.name

def pre_save_sizes(sender, instance, *args, **kwargs):
        instance.name = instance.name.upper()
pre_save.connect(pre_save_sizes, sender=Sizes)

class ProductSizes(AbstractTimeStamp):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name = 'product_size', blank=True, null=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductSize'
        verbose_name_plural = 'ProductSizes'
        db_table = 'productSizes'

    def __str__(self):
        return self.name


class ProductReview(AbstractTimeStamp):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name = 'product_review', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_review',blank=True, null=True)
    # customer = models.ForeignKey(CustomerProfile, on_delete=models.PROTECT, related_name='customer_review',blank=True, null=True)
    rating_number = models.IntegerField(default=0)
    review_text = models.TextField(default='',blank=True, null=True)
    class Meta:
        verbose_name = 'ProductReview'
        verbose_name_plural = 'ProductReviews'
        db_table = 'productReview'

    def __str__(self):
        return str(self.pk)
