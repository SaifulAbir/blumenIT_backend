from django.contrib import admin
from user.models import User, CustomerProfile, OTPModel, Subscription

admin.site.register(User)
admin.site.register(CustomerProfile) 
admin.site.register(OTPModel)
admin.site.register(Subscription)
