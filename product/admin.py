from django.contrib import admin
from product.models import FlashDealProduct, ProductVariation, Specification, SpecificationValue, TextColor, Attribute, AttributeValues, Category, Color, FlashDealInfo, Inventory, InventoryVariation, ProductAttributeValues, ProductColor, ProductImages, ShippingClass, SubCategory, SubSubCategory, Brand, Tags, Units, DiscountTypes, Product, ProductAttributes, VariantType, ProductTags, ProductCombinationMedia, ProductReview, ProductVideoProvider, VatType, SpecificationTitle, FilterAttributes, ProductFilterAttributes


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(SubSubCategory)
admin.site.register(Tags)
admin.site.register(Brand)
admin.site.register(Units)
admin.site.register(DiscountTypes)
# admin.site.register(ProductAttributes)
# admin.site.register(ProductAttributeValues)
admin.site.register(VariantType)
admin.site.register(ProductTags)
admin.site.register(ProductReview)
admin.site.register(ProductImages)
admin.site.register(ProductVideoProvider)
# admin.site.register(Color)
admin.site.register(Attribute)
admin.site.register(AttributeValues)
admin.site.register(FlashDealInfo)
admin.site.register(VatType)
# admin.site.register(ProductColor)
admin.site.register(Inventory)
# admin.site.register(InventoryVariation)
# admin.site.register(ProductVariation)
admin.site.register(ShippingClass)
admin.site.register(TextColor)
admin.site.register(Specification)
admin.site.register(SpecificationTitle)
admin.site.register(SpecificationValue)
admin.site.register(FlashDealProduct) 
admin.site.register(FilterAttributes)
admin.site.register(ProductFilterAttributes)

class ProductImageInline(admin.TabularInline):
    model = ProductImages
    fields = ['file']


class ProductTagsInline(admin.TabularInline):
    model = ProductTags
    fields = ['tag']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline, ProductTagsInline
    ]


class ProductCombinationImageInline(admin.TabularInline):
    model = ProductCombinationMedia
    fields = ['file']

