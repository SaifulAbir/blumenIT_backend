from django.contrib import admin
from product.models import Product, ProductCategory, ProductSubCategory, ProductBrand, Tags, Colors, Sizes

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductSubCategory)
admin.site.register(ProductBrand)
admin.site.register(Tags)
admin.site.register(Colors)
admin.site.register(Sizes)