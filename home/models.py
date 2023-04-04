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
    image = models.ImageField(upload_to='sliderImage', validators=[validate_file_extension], default="")
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

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_view_count')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_product_view')
    customer = models.ForeignKey(CustomerProfile, on_delete=models.PROTECT, related_name='customer_product_view')
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
    header_logo = models.ImageField(upload_to='HomeImage', null=True, blank=True)
    footer_logo = models.ImageField(upload_to='HomeImage', null=True, blank=True)
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
    attached_file = models.FileField(upload_to='corporate', blank=True, null=True)
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
    ]

    image = models.ImageField(upload_to='HomeImage', default="")
    bold_text = models.TextField(null=True, blank=True)
    small_text = models.TextField(null=True, blank=True)
    work_for = models.CharField(max_length=30, choices=WORK_FOR, default=WORK_FOR[0][0])
    is_active = models.BooleanField(null=False, blank=False, default=True)
    is_gaming = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        verbose_name = 'Advertisement'
        verbose_name_plural = 'Advertisements'
        db_table = 'advertisement'

    def __str__(self):
        return self.work_for