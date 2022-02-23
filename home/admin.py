from django.contrib import admin
from home.models import SliderImage, DealsOfTheDay, ProductView

admin.site.register(SliderImage)
admin.site.register(ProductView)

@admin.register(DealsOfTheDay)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date', 'discount_price', 'discount_price_type', 'is_active']
