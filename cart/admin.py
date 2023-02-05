from django.contrib import admin
from cart.models import BillingAddress, PaymentType, ShippingType, Coupon, UseRecordOfCoupon, Order, \
     OrderItem, DeliveryAddress, Wishlist, SubOrder


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
    fields = ['product', 'quantity', 'unit_price', 'unit_price_after_add_warranty', 'total_price', 'product_warranty']

class SubOrderInline(admin.TabularInline):
    model = SubOrder
    fields = ['sub_order_id', 'in_house_order']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        SubOrderInline, OrderItemInline
    ]

@admin.register(SubOrder)
class SubOrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]
