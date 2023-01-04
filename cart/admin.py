from django.contrib import admin
from cart.models import BillingAddress, PaymentType, ShippingType, Coupon, UseRecordOfCoupon, Order, \
     OrderItem, DeliveryAddress, Wishlist


# Register your models here.
admin.site.register(ShippingType)
admin.site.register(Coupon)
admin.site.register(UseRecordOfCoupon)
admin.site.register(PaymentType)
admin.site.register(BillingAddress)
admin.site.register(OrderItem)
admin.site.register(DeliveryAddress)
admin.site.register(Wishlist)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline,
    ]
