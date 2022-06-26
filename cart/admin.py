from django.contrib import admin
from cart.models import PaymentType, ShippingType, Coupon, UseRecordOfCoupon, Order, OrderItem

# Register your models here.
admin.site.register(ShippingType)
admin.site.register(Coupon)
admin.site.register(UseRecordOfCoupon)
admin.site.register(PaymentType)

# admin.site.register(Order)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'quantity']
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline,
    ]