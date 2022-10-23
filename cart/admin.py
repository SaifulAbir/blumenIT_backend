from django.contrib import admin
from cart.models import BillingAddress, OrderItemCombination, PaymentType, ShippingType, Coupon, UseRecordOfCoupon, Order, VendorOrder, OrderItem,DiscountType


# Register your models here.
admin.site.register(ShippingType)
admin.site.register(Coupon)
admin.site.register(UseRecordOfCoupon)
admin.site.register(PaymentType)
admin.site.register(BillingAddress)
admin.site.register(VendorOrder)
admin.site.register(OrderItem)
admin.site.register(OrderItemCombination)
admin.site.register(DiscountType)

# admin.site.register(Order)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'quantity', 'vendor_order']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline,
    ]
