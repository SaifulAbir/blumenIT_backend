from django.contrib import admin
from home.models import SliderImage, DealsOfTheDay, ProductView, FAQ, ContactUs, HomeSingleRowData, PosterUnderSlider, \
    PopularProductsUnderPoster, FeaturedProductsUnderPoster, CorporateDeal

admin.site.register(SliderImage)
admin.site.register(ProductView)
admin.site.register(FAQ)
admin.site.register(ContactUs)
admin.site.register(HomeSingleRowData)
admin.site.register(PosterUnderSlider)
admin.site.register(PopularProductsUnderPoster) 
admin.site.register(FeaturedProductsUnderPoster)
admin.site.register(CorporateDeal)

@admin.register(DealsOfTheDay)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date', 'discount_price', 'discount_price_type', 'is_active']
