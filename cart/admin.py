from django.contrib import admin
from cart.models import BillingAddress, PaymentType, ShippingType, Coupon, UseRecordOfCoupon, Order, \
     OrderItem, DeliveryAddress, Wishlist


# Register your models here.
admin.site.register(ShippingType)
admin.site.register(Coupon)
admin.site.register(UseRecordOfCoupon)
admin.site.register(PaymentType)
admin.site.register(BillingAddress)
admin.site.register(DeliveryAddress)
admin.site.register(Wishlist)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'quantity', 'unit_price', 'total_price', 'product_warranty', 'price_after_add_warranty']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline,
    ]
