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


class DealsOfTheDay(AbstractTimeStamp):
    CHOICES = [
        ('per', 'Percentage'),
        ('flat', 'Flat'),]

    product = models.ManyToManyField(Product)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    discount_price = models.FloatField(max_length=255, null=False, blank=False, default=0)
    discount_price_type = models.CharField(max_length=20, null=False, blank=False, choices=CHOICES)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'DealsOfTheDay'
        verbose_name_plural = 'DealsOfTheDays'
        db_table = 'dealsOfTheDay'

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
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'HomeSingleRowData'
        verbose_name_plural = 'HomeSingleRowDatas'
        db_table = 'home_single_row_data'

    def __str__(self):
        return f"{self.pk}"


class PosterUnderSlider(AbstractTimeStamp):
    image = models.ImageField(upload_to='HomeImage', default="")
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'PosterUnderSlider'
        verbose_name_plural = 'PosterUnderSliders'
        db_table = 'poster_under_slider'

    def __str__(self):
        return f"{self.pk}"


class PopularProductsUnderPoster(AbstractTimeStamp):
    image = models.ImageField(upload_to='HomeImage', default="")
    bold_text = models.TextField(null=True, blank=True)
    small_text = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)
    is_gaming = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        verbose_name = 'PopularProductsUnderPoster'
        verbose_name_plural = 'PopularProductsUnderPosters'
        db_table = 'popular_products_under_poster'

    def __str__(self):
        return f"{self.pk}"


class FeaturedProductsUnderPoster(AbstractTimeStamp):
    image = models.ImageField(upload_to='HomeImage', default="")
    bold_text = models.TextField(null=True, blank=True)
    small_text = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)
    is_gaming = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        verbose_name = 'FeaturedProductsUnderPoster'
        verbose_name_plural = 'FeaturedProductsUnderPosters'
        db_table = 'featured_products_under_poster'

    def __str__(self):
        return f"{self.pk}"


class CorporateDeal(AbstractTimeStamp):
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=255, unique=True)
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