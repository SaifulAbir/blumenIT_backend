from django.db import models
from ecommerce.models import AbstractTimeStamp
from ecommerce.models import AbstractTimeStamp
from django.utils.translation import gettext as _
from user.models import User
from django.core import validators


class Header(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=True, blank=False)
    phone_number = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=100, null=True, blank=False)
    whatsapp_number = models.CharField(max_length=100, null=True, blank=False)
    address = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Header"
        verbose_name_plural = "Headers"
        db_table = 'header'

    def __str__(self):
        return self.title


class Footer(AbstractTimeStamp):
    title = models.CharField(max_length=100, null=True, blank=False)
    phone_number = models.CharField(max_length=100, null=False, blank=False)
    short_description = models.CharField(max_length=500, null=False, blank=False)
    email = models.EmailField(max_length=100, null=True, blank=False)
    whatsapp_number = models.CharField(max_length=100, null=True, blank=False)
    address = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Footer"
        verbose_name_plural = "Footers"
        db_table = 'footer'

    def __str__(self):
        return self.title

