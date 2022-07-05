from django.contrib import admin
from product.models import \
    Category, \
    SubCategory, \
    SubSubCategory, \
    Brand, \
    Units, \
    DiscountTypes, \
    Product, \
    ProductAttributes, \
    ProductCombinations, \
    VariantType, \
    ProductCombinationsVariants, \
    ProductTags, \
    ProductMedia, \
    ProductCombinationMedia, \
    ProductReview

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(SubSubCategory)
admin.site.register(Brand)
admin.site.register(Units)
admin.site.register(DiscountTypes)
admin.site.register(ProductAttributes)
admin.site.register(VariantType)
admin.site.register(ProductCombinationsVariants)
admin.site.register(ProductTags)
admin.site.register(ProductReview)

class ProductImageInline(admin.TabularInline):
    model = ProductMedia
    fields = ['file']
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
    ]

class ProductCombinationImageInline(admin.TabularInline):
    model = ProductCombinationMedia
    fields = ['file']
@admin.register(ProductCombinations)
class ProductCombinationsAdmin(admin.ModelAdmin):
    inlines = [
        ProductCombinationImageInline,
    ]

