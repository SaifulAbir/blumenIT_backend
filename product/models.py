from statistics import mode
from django.db import models
from ecommerce.models import AbstractTimeStamp
from vendor.models import Vendor
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
from user.models import User, CustomerProfile

class Product(AbstractTimeStamp):
    title = models.CharField(max_length=500, null=False, blank=False)

class Category(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False)

class SubCategory(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False)

class SubSubCategory(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False)

class Brand(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False)

class Units(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False)

class Colors(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False)

class Attributes(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False)

class ProductColors(AbstractTimeStamp):
    color = models.ForeignKey(Colors, on_delete=models.PROTECT, related_name='product_colors')

class ProductAttributes(AbstractTimeStamp):
    attribute = models.ForeignKey(Attributes, on_delete=models.Prefetch, related_name='product_attributes')

class ProductAttributesValues(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False)
    product_attribute = models.ForeignKey(ProductAttributes, on_delete=models.PROTECT, related_name='product_attribute')

class Productcomibinations(AbstractTimeStamp):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product')

class DiscountTypes(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=False, blank=False)

class ProductTags(AbstractTimeStamp):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product')

class ProductMedia(AbstractTimeStamp):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product')

class ProductReview(AbstractTimeStamp):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product')

