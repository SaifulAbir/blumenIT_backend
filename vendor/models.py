from django.db import models
from ecommerce.models import AbstractTimeStamp
from django.utils.translation import gettext as _


class VendorRequest(AbstractTimeStamp):
    VENDOR_STATUSES = [
        ('ORGANIZATION', 'Organization'),
        ('INDIVIDUAL', 'Individual'), ]

    email = models.EmailField(
        max_length=255, null=False, blank=False, unique=True)
    organization_name = models.CharField(
        max_length=254, null=False, blank=False, verbose_name=_('Organization/ Vendor Name'), unique=True)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    vendor_status = models.CharField(max_length=20, choices=VENDOR_STATUSES)
    nid = models.CharField(max_length=50, null=False, blank=False)
    trade_license = models.ImageField(upload_to='images/trade_license', null=True, blank=True)

    def __str__(self):
        return self.organization_name

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = "Vendor Request"
        verbose_name_plural = "Vendor Requests"
        db_table = 'vendor_requests'
