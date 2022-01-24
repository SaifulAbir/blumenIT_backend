from django.db import models
from ecommerce.models import AbstractTimeStamp
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
from user.models import User
from django.utils.translation import gettext as _
from product.models import Product

class Cart(AbstractTimeStamp):
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null=False, related_name="cart_user",verbose_name=_('Cart User'))
    slug  = models.SlugField(null=False, blank=False, allow_unicode=True)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        db_table = 'carts'

    def __str__(self):
        return self.id

def pre_save_product(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_product, sender=Product)

class CartItem(AbstractTimeStamp):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price_ht = models.FloatField(blank=True)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)

    # TAX_AMOUNT = 19.25

    # def price_ttc(self):
    #     return self.price_ht * (1 + TAX_AMOUNT/100.0)

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        db_table = 'cart_items'

    def __str__(self):
        return  self.client + " - " + self.product