from django.db import models
from ecommerce.models import AbstractTimeStamp
from user.models import User
from .utils import unique_slug_generator_support

class Ticket(AbstractTimeStamp):
    SUPPORT_STATUSES = [
        ('UN-PAID', 'Un-Paid'),
        ('PAID', 'Paid'),
    ]

    ticket_id = models.SlugField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT,related_name='support_user', blank=True, null=True)
    ticket_title = models.CharField(max_length=255, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'tickets'
        db_table = 'ticket'

    def __str__(self):
        return self.ticket_id

def pre_save_support(sender, instance, *args, **kwargs):
    if not instance.ticket_id:
        instance.ticket_id = '#' + \
            str(unique_slug_generator_support(instance))
