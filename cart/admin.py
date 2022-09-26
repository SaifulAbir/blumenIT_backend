from django.contrib import admin
from cart.models import BillingAddress, PaymentType, ShippingType, Coupon, UseRecordOfCoupon, Order, VendorOrder, OrderItem

# Register your models here.
admin.site.register(ShippingType)
admin.site.register(Coupon)
admin.site.register(UseRecordOfCoupon)
admin.site.register(PaymentType)
admin.site.register(BillingAddress)
admin.site.register(VendorOrder)

# admin.site.register(Order)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'quantity', 'vendor_order']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline,
    ]
