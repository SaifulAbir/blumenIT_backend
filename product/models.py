from django.db import models
from ecommerce.models import AbstractTimeStamp
from .utils import unique_slug_generator
from django.db.models.signals import pre_save


class ProductBrand(AbstractTimeStamp):
    name = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductBrand'
        verbose_name_plural = 'ProductBrands'
        db_table = 'productBrands'

    def __str__(self):
        return self.name

class ProductCategory(AbstractTimeStamp):
    name = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductCategory'
        verbose_name_plural = 'ProductCategories'
        db_table = 'productCategory'

    def __str__(self):
        return self.name

class Product(AbstractTimeStamp):
    PRODUCT_STATUSES = [
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active')]

    title = models.CharField(max_length=500, null=False, blank=False)
    slug  = models.SlugField(null=False, blank=False, allow_unicode=True)
    price = models.FloatField(max_length=255, null=False, blank=False, default=0)
    old_price = models.FloatField(max_length=255, null=True, blank=True, default=0)
    full_description = models.TextField()
    short_description = models.CharField(max_length=800)
    quantity = models.BigIntegerField(null=True, blank=True, default=0)
    quantity_left = models.BigIntegerField(null=True, blank=True, default=0, help_text="Automatic quantity decreased after order placed. Leave it empty for unlimited/manual quantity of the product.")
    thumbnail = models.ImageField(upload_to='images/product_thumbnail_images', blank=True)
    warranty  = models.CharField(max_length=255, blank=True, help_text="eg: 1 year or 6 months")
    variation = models.CharField(max_length=255, blank=True)
    rating = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=PRODUCT_STATUSES, default=PRODUCT_STATUSES[0][0])
    is_featured = models.BooleanField(null=False, blank=False, default=False)
    product_category = models.ForeignKey(ProductCategory, related_name='category', blank=True, null=True, on_delete=models.CASCADE)
    product_brand = models.ForeignKey(ProductBrand, related_name='brand', blank=True, null=True, on_delete=models.CASCADE)
    # vendor                      = models.ForeignKey(Vendor, related_name='vendor', blank=True, null=True, on_delete=models.CASCADE)

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

class ProductSize(AbstractTimeStamp):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name = 'product_size', blank=True, null=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ProductSize'
        verbose_name_plural = 'ProductSizes'
        db_table = 'productSizes'

    def __str__(self):
        return self.name


