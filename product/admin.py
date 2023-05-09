from django.contrib import admin
from product.models import FlashDealProduct, Specification, SpecificationValue, TextColor, Attribute, AttributeValues, \
    Category, Inventory, ProductImages, ShippingClass, SubCategory, SubSubCategory, Brand, Tags, Units, \
    DiscountTypes, Product, VariantType, ProductTags, ProductReview, ProductVideoProvider, VatType, SpecificationTitle, ProductReviewReply, \
    FilterAttributes, ProductFilterAttributes, ProductCondition, Warranty, ProductWarranty, SavePc, SavePcItems, Offer, \
    OfferProduct, OfferCategory, ShippingCountry, ShippingState, ShippingCity


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(SubSubCategory)
admin.site.register(Tags)
admin.site.register(Brand)
admin.site.register(Units)
admin.site.register(DiscountTypes)
admin.site.register(VariantType)
admin.site.register(ProductTags) 
admin.site.register(ProductReview)
admin.site.register(ProductReviewReply)
admin.site.register(ProductImages)
admin.site.register(ProductVideoProvider)
admin.site.register(Attribute)
admin.site.register(AttributeValues)
admin.site.register(VatType)
admin.site.register(Inventory)
admin.site.register(ShippingCountry)
admin.site.register(ShippingState)
admin.site.register(ShippingCity)
admin.site.register(ShippingClass)
admin.site.register(TextColor)
admin.site.register(SpecificationTitle)
admin.site.register(SpecificationValue)
admin.site.register(FlashDealProduct)
admin.site.register(FilterAttributes)
admin.site.register(ProductCondition)
admin.site.register(Warranty)
# admin.site.register(OfferCategory)

class ProductImageInline(admin.TabularInline):
    model = ProductImages
    fields = ['file']


class ProductTagsInline(admin.TabularInline):
    model = ProductTags
    fields = ['tag']

class SpecificationInline(admin.TabularInline):
    model = Specification
    fields = ['title', 'is_active']


class ProductFilterAttributesInline(admin.TabularInline):
    model = ProductFilterAttributes
    fields = ['filter_attribute', 'attribute_value', 'is_active']


class ProductWarrantyInline(admin.TabularInline):
    model = ProductWarranty
    fields = ['warranty', 'warranty_value', 'warranty_value_type', 'is_active']


class ProductOfferProductInline(admin.TabularInline):
    model = OfferProduct
    fields = ['offer', 'is_active']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline, ProductTagsInline, SpecificationInline, ProductFilterAttributesInline, ProductWarrantyInline, ProductOfferProductInline
    ]


class OfferProductInline(admin.TabularInline):
    model = OfferProduct
    fields = ['product']


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    inlines = [
        OfferProductInline
    ]



class SavePcItemsInline(admin.TabularInline):
    model = SavePcItems
    fields = ['sub_category', 'product']


@admin.register(SavePc)
class SavePcAdmin(admin.ModelAdmin):
    inlines = [
        SavePcItemsInline
    ]




