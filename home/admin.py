from django.contrib import admin
from home.models import SliderImage, DealsOfTheDay

admin.site.register(SliderImage)

@admin.register(DealsOfTheDay)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['product','start_date']
