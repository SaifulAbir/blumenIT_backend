from datetime import datetime
from django.db import models
from ecommerce.models import AbstractTimeStamp
from product.models import Product
from user.models import User, CustomerProfile


class SliderImage(AbstractTimeStamp):
    def validate_file_extension(value):
        import os
        from django.core.exceptions import ValidationError
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.jpg', '.png', '.jpeg']
        if not ext.lower() in valid_extensions:
            raise ValidationError('Unsupported file extension.')
    image = models.ImageField(upload_to='sliderImage', validators=[
                              validate_file_extension], default="")
    bold_text = models.TextField(null=True, blank=True)
    small_text = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)
    is_gaming = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        verbose_name = 'SliderImage'
        verbose_name_plural = 'SliderImages'
        db_table = 'sliderImages'

    def __str__(self):
        return f"{self.pk}"


class ProductView(AbstractTimeStamp):

    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='product_view_count')
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='user_product_view')
    customer = models.ForeignKey(
        CustomerProfile, on_delete=models.PROTECT, related_name='customer_product_view')
    view_date = models.DateTimeField(default=datetime.now)
    view_count = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Product View'
        verbose_name_plural = 'Product Views'
        db_table = 'product_views'

    def __str__(self):
        return self.product.title


class FAQ(AbstractTimeStamp):
    question = models.TextField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        db_table = 'faqs'

    def __str__(self):
        return f"{self.pk}"


class ContactUs(AbstractTimeStamp):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'ContactUs'
        verbose_name_plural = 'ContactUs'
        db_table = 'contactUs'

    def __str__(self):
        return f"{self.pk}"


class HomeSingleRowData(AbstractTimeStamp):
    phone = models.CharField(max_length=20, null=True, blank=True)
    whats_app_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    bottom_banner = models.ImageField(upload_to='HomeImage', default="")
    shop_address = models.TextField(default='', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    header_logo = models.ImageField(
        upload_to='HomeImage', null=True, blank=True)
    footer_logo = models.ImageField(
        upload_to='HomeImage', null=True, blank=True)
    footer_description = models.TextField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    whatsapp = models.URLField(null=True, blank=True)
    messenger = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = 'HomeSingleRowData'
        verbose_name_plural = 'HomeSingleRowDatas'
        db_table = 'home_single_row_data'

    def __str__(self):
        return f"{self.pk}"


class CorporateDeal(AbstractTimeStamp):
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=255)
    company_name = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    details_text = models.TextField(null=True, blank=True)
    attached_file = models.FileField(
        upload_to='corporate', blank=True, null=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'CorporateDeal'
        verbose_name_plural = 'CorporateDeals'
        db_table = 'corporate_deal'

    def __str__(self):
        return 'First Name: ' + self.first_name + ' Last Name: ' + self.last_name + ' Company Name: ' + self.company_name + ' Phone:' + self.phone


class RequestQuote(AbstractTimeStamp):
    SERVICES = [
        ('Wholesale Business Plan', 'Wholesale'),
        ('Retail Business Plan', 'Retail'),
        ('Reseller Business Plan', 'Reseller'),
        ('Support Business Plan', 'Support'),
        ('Sales Business Plan', 'Sales'),
        ('Others', 'Others')
    ]
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=120, blank=True)
    website = models.CharField(max_length=120, blank=True)
    address = models.CharField(max_length=255, blank=True)
    services = models.CharField(max_length=120, choices=SERVICES)
    overview = models.TextField()
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'RequestQuote'
        verbose_name_plural = 'RequestQuotes'
        db_table = 'request_quote'

    def __str__(self):
        return self.name


class Advertisement(AbstractTimeStamp):
    WORK_FOR = [
        ('SLIDER', 'slider'),
        ('SLIDER_SMALL_CAROUSEL', 'slider_small_carousel'),
        ('SLIDER_SMALL_STATIC', 'slider_small_static'),
        ('POPULAR_PRODUCT_POSTER', 'popular_product_poster'),
        ('FEATURED_PRODUCT_POSTER', 'featured_product_poster'),
        ('OFFER', 'offer'),
    ]

    image = models.ImageField(upload_to='HomeImage', default="")
    image_url = models.TextField(null=True, blank=True)
    bold_text = models.TextField(null=True, blank=True)
    small_text = models.TextField(null=True, blank=True)
    work_for = models.CharField(
        max_length=30, choices=WORK_FOR, default=WORK_FOR[0][0])
    is_active = models.BooleanField(null=False, blank=False, default=True)
    is_gaming = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        verbose_name = 'Advertisement'
        verbose_name_plural = 'Advertisements'
        db_table = 'advertisement'

    def __str__(self):
        return self.work_for


class AboutUs(AbstractTimeStamp):
    our_values = models.TextField(null=True, blank=True, default="")
    our_vision = models.TextField(null=True, blank=True, default="")
    our_mission = models.TextField(null=True, blank=True, default="")
    our_goals = models.TextField(null=True, blank=True, default="")
    customer_relationship = models.TextField(null=True, blank=True, default="")
    our_target_market = models.TextField(null=True, blank=True, default="")
    retail_wholesale_trade = models.TextField(
        null=True, blank=True, default="")
    promise_text = models.TextField(null=True, blank=True, default="")
    footer_text = models.TextField(null=True, blank=True, default="")
    our_values_image = models.ImageField(upload_to='About_us', default="")
    customer_relationship_image = models.ImageField(
        upload_to='About_us', default="")
    our_target_market_image = models.ImageField(
        upload_to='About_us', default="")
    retail_wholesale_trade_image = models.ImageField(
        upload_to='About_us', default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'AboutUs'
        verbose_name_plural = 'AboutUs'
        db_table = 'about_us'

    def __str__(self):
        return f"{self.pk}"


class TermsAndCondition(AbstractTimeStamp):
    content = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'TermsAndCondition'
        verbose_name_plural = 'TermsAndConditions'
        db_table = 'terms_and_condition'

    def __str__(self):
        return f"{self.pk}"


class OnlineServiceSupport(AbstractTimeStamp):
    content = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'OnlineServiceSupport'
        verbose_name_plural = 'OnlineServiceSupports'
        db_table = 'online_service_support'

    def __str__(self):
        return f"{self.pk}"


class PaymentMethod(AbstractTimeStamp):
    content = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'PaymentMethod'
        verbose_name_plural = 'PaymentMethods'
        db_table = 'payment_method'

    def __str__(self):
        return f"{self.pk}"


class RefundAndReturnPolicy(AbstractTimeStamp):
    content = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'RefundAndReturnPolicy'
        verbose_name_plural = 'RefundAndReturnPolicies'
        db_table = 'refund_and_return_policy'

    def __str__(self):
        return f"{self.pk}"


class Shipping(AbstractTimeStamp):
    content = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'Shipping'
        verbose_name_plural = 'Shippings'
        db_table = 'shipping'

    def __str__(self):
        return f"{self.pk}"


class PrivacyPolicy(AbstractTimeStamp):
    content = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'PrivacyPolicy'
        verbose_name_plural = 'PrivacyPolicies'
        db_table = 'privacy_policy'

    def __str__(self):
        return f"{self.pk}"


class ServiceCenter(AbstractTimeStamp):
    content = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'ServiceCenter'
        verbose_name_plural = 'ServiceCenters'
        db_table = 'service_center'

    def __str__(self):
        return f"{self.pk}"


class Pages(AbstractTimeStamp):
    TYPE = [
        ('INFO', 'Info'),
        ('CS', 'customer_service')
    ]
    title = models.CharField(max_length=800, default='')
    content = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=30, choices=TYPE, default=TYPE[0][0])
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        db_table = 'pages'

    def __str__(self):
        return f"{self.title}"


class MediaChunk(AbstractTimeStamp):
    title = models.CharField(max_length=800, default='', null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'MediaChunk'
        verbose_name_plural = 'MediaChunks'
        db_table = 'media_chunks'

    def __str__(self):
        return f"{self.pk}"


class MediaFiles(AbstractTimeStamp):
    title = models.CharField(max_length=800, default='', null=True, blank=True)
    chunk = models.ForeignKey(
        MediaChunk, on_delete=models.CASCADE, related_name='media_files_chunk', null=True, blank=True)
    file = models.FileField(upload_to='media_files', null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'MediaFile'
        verbose_name_plural = 'MediaFiles'
        db_table = 'media_files'

    def __str__(self):
        return f"{self.pk}"
