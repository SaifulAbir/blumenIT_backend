from django.core.validators import RegexValidator
from django.db import models
from ecommerce.models import AbstractTimeStamp
from django.utils.translation import gettext as _
from user.models import User
from django.core import validators

phone_regex = RegexValidator(regex='^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$',message='Invalid phone number')


class Seller(AbstractTimeStamp):
    SELLER_STATUSES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('FREEZE', 'Freeze')
    ]

    name = models.CharField(max_length=254, null=False, blank=False)
    phone = models.CharField(max_length=255, validators=[phone_regex], null=False, blank=False, unique=True)
    email = models.EmailField(max_length=50, null=False, blank=False, unique=True, validators=[validators.EmailValidator(message="Invalid Email")])
    address = models.CharField(max_length=254, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True, upload_to='images/logo')
    status = models.CharField(
        max_length=20, choices=SELLER_STATUSES, default=SELLER_STATUSES[0][0])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Sellers"
        verbose_name = "Seller"
        db_table = 'sellers'


class Vendor(AbstractTimeStamp):
    name = models.CharField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=255, null=False, blank=False, unique=True)
    email = models.EmailField(max_length=255, null=False, blank=False, unique=True)
    logo = models.ImageField( null=True, blank=True)
    organization_name = models.CharField(
        max_length=254, null=True, blank=True)
    address = models.CharField(max_length=254, null=True, blank=True)
    vendor_admin = models.ForeignKey(
        User, on_delete=models.PROTECT, blank=True, null=True)
    banner = models.ImageField(upload_to='images/banner', null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    bio = models.TextField(default='', blank=True, null=True)
    password = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return self

    class Meta:
        verbose_name_plural = "Vendors"
        verbose_name = "Vendor"
        db_table = 'vendors'


class StoreSettings(AbstractTimeStamp):
    store_name = models.CharField(
        max_length=254, null=False, blank=False, verbose_name=_('Organization/ Vendor Name'))
    address = models.CharField(
        max_length=254, null=True, blank=True, verbose_name=_('Address'))
    email = models.EmailField(
        max_length=255, null=False, blank=False, unique=True)
    seller = models.ForeignKey(
        Seller, on_delete=models.PROTECT, blank=True, null=True, related_name="seller_store_setting",
        verbose_name=_('Vendor'))
    logo = models.ImageField(upload_to='images/store_logo')
    banner = models.ImageField(upload_to='images/banner')
    phone = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    bio = models.TextField(default='', blank=True, null=True)

    def __str__(self):
        return self.store_name

    class Meta:
        verbose_name_plural = "Store Settings"
        verbose_name = "Store Setting"
        db_table = 'store_settings'

