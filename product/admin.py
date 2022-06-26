from django.contrib import admin
from product.models import Product, ProductMedia, ProductCategory, ProductSubCategory, ProductChildCategory, ProductBrand, Tags, \
Colors, Sizes, ProductReview

# Register your models here.
# admin.site.register(Product)
# admin.site.register(ProductMedia)

# @admin.register(Product)

class ProductImageInline(admin.TabularInline):
    model = ProductMedia
    fields = ['file']
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
    ]


admin.site.register(ProductCategory)
admin.site.register(ProductSubCategory)
admin.site.register(ProductChildCategory)
admin.site.register(ProductBrand)
admin.site.register(Tags)
admin.site.register(Colors)
admin.site.register(Sizes)
admin.site.register(ProductReview)
admin.site.register(ProductMedia)