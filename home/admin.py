from django.contrib import admin
from home.models import ProductView, FAQ, ContactUs, HomeSingleRowData, \
    CorporateDeal, RequestQuote, Advertisement, Pages, AboutUs, TermsAndCondition, OnlineServiceSupport, PaymentMethod, RefundAndReturnPolicy, \
    Shipping, PrivacyPolicy, ServiceCenter

admin.site.register(ProductView)
admin.site.register(FAQ)
admin.site.register(ContactUs)
admin.site.register(HomeSingleRowData)
admin.site.register(CorporateDeal)
admin.site.register(RequestQuote)
admin.site.register(Advertisement)
admin.site.register(AboutUs)
admin.site.register(TermsAndCondition)
admin.site.register(OnlineServiceSupport)
admin.site.register(PaymentMethod)
admin.site.register(RefundAndReturnPolicy)
admin.site.register(Shipping)
admin.site.register(PrivacyPolicy)
admin.site.register(ServiceCenter)
admin.site.register(Pages)
