from django.db import models
from ecommerce.models import AbstractTimeStamp
from vendor.models import Vendor, Seller
from .utils import unique_slug_generator_cart, unique_order_id_generator_for_order, unique_order_id_generator_for_vendor_order
from django.db.models.signals import pre_save
from user.models import CustomerProfile, User
from django.utils.translation import gettext as _
from product.models import Product, ProductAttributes, VariantType, ShippingClass, DiscountTypes
from django.utils import timezone

# from django_countries.fields import CountryField

'''
    1. Item added to cart
    2. Adding a BillingAddress
    (Failed Checkout)
    3. Payment
    4. Being delivered
    5. Received
    6. Refunds
'''


class Coupon(AbstractTimeStamp):
    code = models.CharField(max_length=15)
    coupon_type = models.CharField(max_length=255, null=False, blank=False)
    min_shopping = models.IntegerField(default=0, null=True, blank=True)
    amount = models.FloatField(max_length=255, null=True, blank=True, default=0, help_text="Amount Coupon")
    discount_type = models.ForeignKey(DiscountTypes, on_delete=models.CASCADE, related_name='discount_type_coupon', null=True, blank=True)
    number_of_uses = models.IntegerField(default=0, null=False, blank=False)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('code',)
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
        db_table = 'coupons'

    def __str__(self):
        return self.code


class UseRecordOfCoupon(AbstractTimeStamp):
    coupon_id = models.ForeignKey(
        Coupon, on_delete=models.CASCADE, related_name='coupon')
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')

    class Meta:
        verbose_name = 'UseRecordOfCoupon'
        verbose_name_plural = 'UseRecordOfCoupons'
        db_table = 'use_record_of_coupon'

    def __str__(self):
        return f"{self.pk}"


class ShippingType(AbstractTimeStamp):
    type_name = models.CharField(max_length=50)
    price = models.FloatField(default=0.00)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'ShippingType'
        verbose_name_plural = 'ShippingTypes'
        db_table = 'shipping_types'

    def __str__(self):
        return f"{self.type_name}"


class PaymentType(AbstractTimeStamp):
    type_name = models.CharField(max_length=50)
    note = models.TextField(null=True, blank=True, default='')
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'PaymentType'
        verbose_name_plural = 'PaymentTypes'
        db_table = 'payment_types'

    def __str__(self):
        return f"{self.type_name}"


class Payment(AbstractTimeStamp):
    charge_id = models.CharField(max_length=50)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        db_table = 'payments'

    def __str__(self):
        return f"{self.pk}"


class DeliveryAddress(AbstractTimeStamp):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(
        max_length=100, null=False, blank=False, default='')
    address = models.CharField(
        max_length=100, null=False, blank=False, default='')
    phone = models.CharField(max_length=255, null=True, blank=True, default='')
    email = models.CharField(max_length=255, null=True, blank=True, default='')
    country = models.CharField(
        max_length=100, blank=True, null=True, default='')
    city = models.CharField(max_length=100, blank=True, null=True, default='')
    state = models.CharField(max_length=100, blank=True, null=True, default='')
    zip_code = models.CharField(
        max_length=100, blank=True, null=True, default='')
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'DeliveryAddress'
        verbose_name_plural = 'DeliveryAddresses'
        db_table = 'delivery_addresses'

    def __str__(self):
        return f"{self.pk}"


class Order(AbstractTimeStamp):
    ORDER_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('PICKED-UP', 'Picked Up'),
        ('DELIVERED', 'Delivered'),
        ('RETURN', 'Return'),
        ('CANCEL', 'Cancel'),
    ]

    PAYMENT_STATUSES = [
        ('UN-PAID', 'Un-Paid'),
        ('PAID', 'Paid'),
    ]

    order_id = models.SlugField(null=False, blank=False, allow_unicode=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT,
                             related_name='order_user', blank=True, null=True)
    # customer_profile = models.ForeignKey(
    #     CustomerProfile, on_delete=models.PROTECT, related_name='order_customer_profile', blank=True, null=True)
    product_count = models.IntegerField(blank=True, null=True)
    vendor = models.ForeignKey(
        Seller, on_delete=models.PROTECT, related_name='order_vendor', blank=True, null=True)
    total_price = models.FloatField(
        max_length=255, null=False, blank=False, default=0)
    order_status = models.CharField(
        max_length=20, null=False, blank=False, choices=ORDER_CHOICES, default=ORDER_CHOICES[1][1])
    payment_status = models.CharField(
        max_length=20, null=False, blank=False, choices=PAYMENT_STATUSES, default=PAYMENT_STATUSES[1][1])
    delivery_agent = models.CharField(max_length=100, null=True, blank=True)
    refund = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    coupon_discount_amount = models.FloatField(max_length=255, null=True, blank=True)
    coupon_status = models.BooleanField(default=False)
    tax_amount = models.FloatField(max_length=255, null=True, blank=True)
    shipping_cost = models.FloatField(max_length=255, null=True, blank=True)
    shipping_class = models.ForeignKey(
        ShippingClass, on_delete=models.SET_NULL, blank=True, null=True)
    payment_type = models.ForeignKey(
        PaymentType, on_delete=models.SET_NULL, blank=True, null=True)
    cash_on_delivery = models.BooleanField(default=False)
    delivery_address = models.ForeignKey(
        DeliveryAddress, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.TextField(null=True, blank=True)
    # ordered = models.BooleanField(default=True)
    # being_delivered = models.BooleanField(default=False)
    # received = models.BooleanField(default=False)
    # refund_requested = models.BooleanField(default=False)
    # refund_granted = models.BooleanField(default=False)
    # payment = models.ForeignKey(
    #     Payment, on_delete=models.SET_NULL, blank=True, null=True)
    # shipping_type = models.ForeignKey(
    #     ShippingType, on_delete=models.SET_NULL, blank=True, null=True)
    # payment_type = models.ForeignKey(
    #     PaymentType, on_delete=models.SET_NULL, blank=True, null=True)
    # coupon = models.ForeignKey(
    #     Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    # coupon_status = models.BooleanField(default=False)
    # notes = models.TextField(null=True, blank=True, default='')
    # total_price = models.FloatField(
    #     max_length=255, null=False, blank=False, default=0)
    # discounted_price = models.FloatField(
    #     max_length=255, null=False, blank=False, default=0)


    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        db_table = 'orders'

    def __str__(self):
        return self.order_id


def pre_save_order(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = 'orid-' + \
            str(unique_order_id_generator_for_order(instance))
        # instance.order_id = 'or-' + str(unique_slug_generator_cart(instance))


pre_save.connect(pre_save_order, sender=Order)


class VendorOrder(AbstractTimeStamp):
    ORDER_CHOICES = [
        ('PENDING', 'pending'),
        ('PROCESSING', 'processing'),
        ('SHIPPED', 'shipped'),
        ('DELIVERED', 'delivered'),
        ('RETURN', 'return'),
        ('CANCEL', 'cancel'),
    ]

    order = models.ForeignKey(Order, on_delete=models.PROTECT,
                              related_name='vendor_order_order', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT,
                             related_name='vendor_order_user', blank=True, null=True)
    customer_profile = models.ForeignKey(
        CustomerProfile, on_delete=models.PROTECT, related_name='vendor_order_customer_profile', blank=True, null=True)
    vendor_order_id = models.SlugField(
        null=False, blank=False, allow_unicode=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=True)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    shipping_type = models.ForeignKey(
        ShippingType, on_delete=models.SET_NULL, blank=True, null=True, related_name='vendor_order_shipping_type')
    order_status = models.CharField(
        max_length=20, null=False, blank=False, choices=ORDER_CHOICES, default=ORDER_CHOICES[1][1])
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT,
                               related_name='vendor_order_vendor', blank=True, null=True)

    class Meta:
        verbose_name = 'VendorOrder'
        verbose_name_plural = 'VendorOrders'
        db_table = 'vendor_orders'

    def __str__(self):
        return self.vendor_order_id


def pre_save_order(sender, instance, *args, **kwargs):
    if not instance.vendor_order_id:
        instance.vendor_order_id = 'vorid-' + \
            str(unique_order_id_generator_for_vendor_order(instance))


pre_save.connect(pre_save_order, sender=VendorOrder)


class OrderItem(AbstractTimeStamp):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, blank=False)
    quantity = models.IntegerField(default=1)
    unit_price = models.FloatField(
        max_length=255, null=False, blank=False, default=0)
    total_price = models.FloatField(
        max_length=255, null=False, blank=False, default=0)
    # is_attribute = models.BooleanField(default=False)
    # is_varient = models.BooleanField(default=False)
    # attribute = models.ForeignKey(
    #     ProductAttributes, on_delete=models.CASCADE, blank=True, null=True)

    # variation = models.ForeignKey(ProductVariation, on_delete=models.PROTECT,
    #                                  related_name='order_items_variation', blank=True, null=True)

    @property
    def subtotal(self):
        total_item_price = self.quantity * self.product.price
        return total_item_price

    class Meta:
        verbose_name = 'OrderItem'
        verbose_name_plural = 'OrderItems'
        db_table = 'order_items'

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

    def get_total_item_price(self):
        return self.quantity * self.product.price

    # TAX_AMOUNT = 19.25

    # def price_ttc(self):
    #     return self.price_ht * (1 + TAX_AMOUNT/100.0)

    # def get_total_discount_item_price(self):
    #     return self.quantity * self.product.discount_price

    # def get_amount_saved(self):
    #     return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        # if self.item.discount_price:
        #     return self.get_total_discount_item_price()
        return self.get_total_item_price()


class OrderItemCombination(AbstractTimeStamp):
    product = models.ForeignKey(
        Product, related_name="order_item_combination_product", on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(
        Order, related_name="order_item_combination_order", on_delete=models.CASCADE, blank=True, null=True)
    orderItem = models.ForeignKey(
        OrderItem, related_name="order_item_combination_order_item", on_delete=models.CASCADE, blank=True, null=True)
    product_attribute = models.ForeignKey(
        ProductAttributes, related_name="order_item_combination_product_attributes", null=True, blank=True, on_delete=models.PROTECT)
    product_attribute_value = models.CharField(
        max_length=500, null=False, blank=False, default="")
    product_attribute_price = models.FloatField(
        max_length=255, null=True, blank=True, default=0)
    variant_type = models.ForeignKey(
        VariantType, related_name="order_item_combination_variant_type", null=True, blank=True, on_delete=models.PROTECT)
    variant_value = models.CharField(max_length=500, null=True, blank=True)
    variant_price = models.FloatField(
        max_length=255, null=True, blank=True, default=0)
    variant_ordered_quantity = models.IntegerField(
        null=True, blank=True, default=0)

    class Meta:
        verbose_name = 'OrderItemCombination'
        verbose_name_plural = 'OrderItemCombinations'
        db_table = 'order_item_combination'

    def __str__(self):
        return str(self.id)


class CustomerAddress(AbstractTimeStamp):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(
        max_length=100, null=False, blank=False, default='')
    last_name = models.CharField(
        max_length=100, null=False, blank=False, default='')
    country = models.CharField(
        max_length=100, blank=True, null=True, default='')
    company_name = models.CharField(
        max_length=100, null=False, blank=False, default='')
    street_address = models.CharField(
        max_length=100, blank=True, null=True, default='')
    city = models.CharField(max_length=100, blank=True, null=True, default='')
    zip_code = models.CharField(
        max_length=100, blank=True, null=True, default='')
    phone = models.CharField(max_length=255, null=True, blank=True, default='')
    email = models.CharField(max_length=255, null=True, blank=True, default='')
    address_type = models.CharField(
        max_length=100, null=False, blank=False, default='')
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'CustomerAddress'
        verbose_name_plural = 'CustomerAddresses'
        db_table = 'customer_addresses'

    def __str__(self):
        return f"{self.pk}"


class Refund(AbstractTimeStamp):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items_refund')
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    class Meta:
        verbose_name = 'Refund'
        verbose_name_plural = 'Refunds'
        db_table = 'refunds'

    def __str__(self):
        return f"{self.pk}"


class Wishlist(AbstractTimeStamp):
    user = models.ForeignKey(User, on_delete=models.PROTECT,
                             related_name='wishlist_user', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class BillingAddress(AbstractTimeStamp):
    user = models.ForeignKey(User, on_delete=models.PROTECT,
                             related_name='billing_address_user', blank=True, null=True)
    first_name = models.CharField(
        max_length=100, null=False, blank=False, default='')
    last_name = models.CharField(
        max_length=100, null=False, blank=False, default='')
    country = models.CharField(
        max_length=100, blank=True, null=True, default='')
    company_name = models.CharField(
        max_length=100, null=False, blank=False, default='')
    street_address = models.CharField(
        max_length=100, blank=True, null=True, default='')
    city = models.CharField(max_length=100, blank=True, null=True, default='')
    zip_code = models.CharField(
        max_length=100, blank=True, null=True, default='')
    phone = models.CharField(max_length=255, null=True, blank=True, default='')
    email = models.CharField(max_length=255, null=True, blank=True, default='')
    address_type = models.CharField(
        max_length=100, null=False, blank=False, default='')
    title = models.CharField(max_length=200, null=True, blank=True, default='')
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'BillingAddress'
        verbose_name_plural = 'BillingAddresses'
        db_table = 'Billing_addresses'

    def __str__(self):
        return f"{self.pk}"
