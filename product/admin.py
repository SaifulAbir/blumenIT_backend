from django.contrib import admin
from product.models import Category, SubCategory, SubSubCategory, Brand, Units, DiscountTypes, Product, Colors, Attributes, ProductColors, ProductAttributes, ProductAttributesValues, ProductCombinations, ProductTags, ProductMedia, ProductReview

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(SubSubCategory)
admin.site.register(Brand)
admin.site.register(Units)
admin.site.register(DiscountTypes)
admin.site.register(ProductMedia)
class ProductImageInline(admin.TabularInline):
    model = ProductMedia
    fields = ['file']
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
    ]
admin.site.register(Colors)
admin.site.register(Attributes)
admin.site.register(ProductColors)
admin.site.register(ProductAttributes)
admin.site.register(ProductAttributesValues)
admin.site.register(ProductCombinations)
admin.site.register(ProductTags)
admin.site.register(ProductReview)