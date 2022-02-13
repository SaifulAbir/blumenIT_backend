from django.contrib import admin
from cart.models import PaymentType, ShippingType

# Register your models here.
admin.site.register(ShippingType)
admin.site.register(PaymentType)