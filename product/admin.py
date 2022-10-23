from django.contrib import admin
from product.models import Category, SubCategory, SubSubCategory, Brand, Tags, Units, DiscountTypes, Product, ProductAttributes, ProductCombinations, VariantType, ProductCombinationsVariants, ProductTags, ProductMedia, ProductCombinationMedia, ProductReview, ProductVideoProvider

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(SubSubCategory)
admin.site.register(Tags)
admin.site.register(Brand)
admin.site.register(Units)
admin.site.register(DiscountTypes)
admin.site.register(ProductAttributes)
admin.site.register(VariantType)
admin.site.register(ProductCombinationsVariants)
admin.site.register(ProductTags)
admin.site.register(ProductReview)
admin.site.register(ProductCombinations)
admin.site.register(ProductMedia)
admin.site.register(ProductVideoProvider)


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
    model = ProductMedia
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
