from django.contrib import admin
from home.models import SliderImage, ProductView, FAQ, ContactUs, HomeSingleRowData, PosterUnderSlider, \
    PopularProductsUnderPoster, FeaturedProductsUnderPoster, CorporateDeal, RequestQuote

admin.site.register(SliderImage)
admin.site.register(ProductView)
admin.site.register(FAQ)
admin.site.register(ContactUs)
admin.site.register(HomeSingleRowData)
admin.site.register(PosterUnderSlider)
admin.site.register(PopularProductsUnderPoster) 
admin.site.register(FeaturedProductsUnderPoster)
admin.site.register(CorporateDeal)
admin.site.register(RequestQuote)

