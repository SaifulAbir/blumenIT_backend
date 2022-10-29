from django.contrib import admin
from product.models import FlashDealProduct, ProductVariation, Specification, SpecificationValue, TextColor, Attribute, AttributeValues, Category, Color, FlashDealInfo, Inventory, InventoryVariation, ProductAttributeValues, ProductColor, ProductImages, ShippingClass, SubCategory, SubSubCategory, Brand, Tags, Units, DiscountTypes, Product, ProductAttributes, ProductCombinations, VariantType, ProductCombinationsVariants, ProductTags, ProductMedia, ProductCombinationMedia, ProductReview, ProductVideoProvider, VatType


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(SubSubCategory)
admin.site.register(Tags)
admin.site.register(Brand)
admin.site.register(Units)
admin.site.register(DiscountTypes)
admin.site.register(ProductAttributes)
admin.site.register(ProductAttributeValues)
admin.site.register(VariantType)
admin.site.register(ProductCombinationsVariants)
admin.site.register(ProductTags)
admin.site.register(ProductReview)
admin.site.register(ProductCombinations)
admin.site.register(ProductImages) 
admin.site.register(ProductVideoProvider) 
admin.site.register(Color) 
admin.site.register(Attribute) 
admin.site.register(AttributeValues) 
admin.site.register(FlashDealInfo) 
admin.site.register(VatType) 
admin.site.register(ProductColor)
admin.site.register(Inventory) 
admin.site.register(InventoryVariation)
admin.site.register(ShippingClass) 
admin.site.register(TextColor)
admin.site.register(ProductVariation)
admin.site.register(Specification)
admin.site.register(SpecificationValue)
admin.site.register(FlashDealProduct)




# class ProductSubCategoryInline(admin.TabularInline):
#     model = SubCategory
#     fields = ['title']


# class ProductSubSubCategoryInline(admin.TabularInline):
#     model = SubSubCategory
#     fields = ['title']


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     inlines = [
#         ProductSubCategoryInline, ProductSubSubCategoryInline
#     ]


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


# @admin.register(ProductCombinations)
# class ProductCombinationsAdmin(admin.ModelAdmin):
#     inlines = [
#         ProductCombinationImageInline,
#     ]
