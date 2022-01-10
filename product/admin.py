from django.contrib import admin
from product.models import Product, ProductCategory, ProductBrand, Tags, Colors, Size

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductBrand)
admin.site.register(Tags)
admin.site.register(Colors)
admin.site.register(Size)