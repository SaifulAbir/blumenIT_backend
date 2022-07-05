from django.contrib import admin
from vendor.models import StoreSettings, VendorRequest, Vendor

admin.site.register(VendorRequest)
admin.site.register(Vendor)
admin.site.register(StoreSettings)
