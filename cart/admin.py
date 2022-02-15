from django.contrib import admin
from cart.models import PaymentType, ShippingType, Coupon

# Register your models here.
admin.site.register(ShippingType)
admin.site.register(Coupon)
admin.site.register(PaymentType)