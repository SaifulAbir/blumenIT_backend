from django.contrib import admin
from vendor.models import StoreSettings, VendorRequest, Vendor, VendorReview

admin.site.register(VendorRequest)
admin.site.register(Vendor)
admin.site.register(StoreSettings)
admin.site.register(VendorReview)
