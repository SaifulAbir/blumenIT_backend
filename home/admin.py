from django.contrib import admin
from home.models import SliderImage, DealsOfTheDay, ProductView, FAQ, ContactUs

admin.site.register(SliderImage)
admin.site.register(ProductView)
admin.site.register(FAQ)
admin.site.register(ContactUs)

@admin.register(DealsOfTheDay)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date', 'discount_price', 'discount_price_type', 'is_active']
