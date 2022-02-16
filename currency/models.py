from django.db import models
from ecommerce.models import AbstractTimeStamp

class Currency(AbstractTimeStamp):
    currency_name = models.CharField(max_length=100, null=False, blank=False)
    currency_symbol = models.CharField(max_length=100, null=False, blank=False)
    currency_rate = models.FloatField(max_length=255, null=False, blank=False, default=0)
    is_default = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'
        db_table = 'currencies'

    def __str__(self):
        return self.currency_name
