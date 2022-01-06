from django.db import models
from ecommerce.models import AbstractTimeStamp
from django.utils.translation import gettext as _


class VendorRequest(AbstractTimeStamp):
    email = models.EmailField(
        max_length=255, null=False, blank=False, unique=True)
    organization_name = models.CharField(
        max_length=254, null=False, blank=False, verbose_name=_('Organization/ Vendor Name'), unique=True)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.organization_name

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = "Vendor Request"
        verbose_name_plural = "Vendor Requests"
        db_table = 'vendor_requests'
