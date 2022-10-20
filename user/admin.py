from django.contrib import admin
from user.models import User, CustomerProfile, OTPModel

admin.site.register(User)
admin.site.register(CustomerProfile)
admin.site.register(OTPModel)
