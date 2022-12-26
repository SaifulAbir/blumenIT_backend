from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import forms
from django.template.loader import render_to_string

from ecommerce.common.emails import send_email_without_delay
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


class VendorRequest(AbstractTimeStamp):
    VENDOR_TYPES = [
        ('ORGANIZATION', 'Organization'),
        ('INDIVIDUAL', 'Individual'), ]

    email = models.EmailField(
        max_length=255, null=False, blank=False, unique=True)
    organization_name = models.CharField(
        max_length=254, null=False, blank=False, verbose_name=_('Organization/ Vendor Name'), unique=True)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    vendor_type = models.CharField(max_length=20, choices=VENDOR_TYPES)
    is_verified = models.BooleanField(default=False, null=True)
    nid = models.CharField(max_length=50, null=False, blank=False)
    trade_license = models.ImageField(
        upload_to='images/trade_license', null=True, blank=True)

    def __str__(self):
        return self.organization_name

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = "Vendor Request"
        verbose_name_plural = "Vendor Requests"
        db_table = 'vendor_requests'


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
    vendor_request = models.ForeignKey(
        VendorRequest, on_delete=models.PROTECT, blank=True, null=True, related_name="vendor_request",
        verbose_name=_('Vendor Request'))
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


class VendorReview(AbstractTimeStamp):
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, null=False,
                               blank=False, related_name='vendor_review_vendor', default="")
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             related_name='vendor_review_user', blank=True, null=True)
    rating_number = models.IntegerField(default=0)
    review_text = models.TextField(default='', blank=True, null=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'VendorReview'
        verbose_name_plural = 'VendorReviews'
        db_table = 'vendor_review'

    def __str__(self):
        return str(self.pk)


# @receiver(post_save, sender=VendorRequest)
# def create_vendor(sender, instance, created, **kwargs):
#     is_verified = instance.is_verified
#     try:
#         vendor = Vendor.objects.get(vendor_request=instance)
#     except Vendor.DoesNotExist:
#         vendor = None
#     if is_verified is True and not vendor:
#         password = User.objects.make_random_password()
#
#         user = User.objects.create(username=instance.email, email=instance.email,
#                                    first_name=instance.first_name, last_name=instance.last_name)
#         user.set_password(password)
#         user.save()
#         vendor_instance = Vendor.objects.create(organization_name=instance.organization_name,
#                                                 vendor_admin=user, email=instance.email, vendor_request=instance, password=password)
#         if vendor_instance:
#             email_list = user.email
#             subject = "Your Account Credentials"
#             html_message = render_to_string('vendor_email.html',
#                                             {'username': user.first_name, 'email': user.email, 'password': password})
#             send_email_without_delay(subject, html_message, email_list)
