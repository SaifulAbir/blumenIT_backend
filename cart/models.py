from django.db import models
from ecommerce.models import AbstractTimeStamp
from .utils import unique_slug_generator_cart
from django.db.models.signals import pre_save
from user.models import User
from django.utils.translation import gettext as _
from product.models import Product

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

class Coupon(AbstractTimeStamp):
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        unique_together = [('code')]
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
        db_table = 'coupons'

    def __str__(self):
        return self.code

class Order(AbstractTimeStamp):
    ORDER_CHOICES = [
        ('PENDING', 'pending'),
        ('PROCESSING', 'processing'),
        ('SHIPPED', 'shipped'),
        ('DELIVERED', 'delivered'),
        ('RETURN', 'return'),
        ('CANCEL', 'cancel'),
        ]

    user = models.ForeignKey(User, on_delete=models.PROTECT,related_name='order_user', blank=True, null=True)
    slug  = models.SlugField(null=False, blank=False, allow_unicode=True)
    ref_code = models.CharField(max_length=20)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    shipping_type = models.ForeignKey(ShippingType, on_delete=models.SET_NULL, blank=True, null=True)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    coupon_status = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True, default='')
    total_price = models.FloatField(max_length=255, null=False, blank=False, default=0)
    discounted_price = models.FloatField(max_length=255, null=False, blank=False, default=0)
    order_status = models.CharField(max_length=20, null=False, blank=False, choices=ORDER_CHOICES, default=ORDER_CHOICES[1][1])

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        db_table = 'orders'

    def __str__(self):
        return self.user.username

def pre_save_order(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_cart(instance)

pre_save.connect(pre_save_order, sender=Order)

class OrderItem(AbstractTimeStamp):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT,related_name='order_items_user', blank=True, null=True)

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

class CustomerAddress(AbstractTimeStamp):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=100, null=False, blank=False, default='')
    last_name = models.CharField(max_length=100, null=False, blank=False, default='')
    country = models.CharField(max_length=100, blank=True, null=True, default='')
    company_name = models.CharField(max_length=100, null=False, blank=False, default='')
    street_address = models.CharField(max_length=100, blank=True, null=True, default='')
    city = models.CharField(max_length=100, blank=True, null=True, default='')
    zip_code = models.CharField(max_length=100, blank=True, null=True, default='')
    phone = models.CharField(max_length=255, null=True, blank=True, default='')
    email = models.CharField(max_length=255, null=True, blank=True, default='')
    address_type = models.CharField(max_length=100, null=False, blank=False, default='')
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'CustomerAddress'
        verbose_name_plural = 'CustomerAddresses'
        db_table = 'customer_addresses'

    def __str__(self):
        return f"{self.pk}"

class Refund(AbstractTimeStamp):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
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
    user = models.ForeignKey(User, on_delete=models.PROTECT,related_name='wishlist_user', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)