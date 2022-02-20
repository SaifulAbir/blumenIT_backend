from django.db import models
from ecommerce.models import AbstractTimeStamp
from product.models import Product

class SliderImage(AbstractTimeStamp):
    def validate_file_extension(value):
        import os
        from django.core.exceptions import ValidationError
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.jpg', '.png', '.jpeg']
        if not ext.lower() in valid_extensions:
            raise ValidationError('Unsupported file extension.')
    file = models.ImageField(upload_to='sliderImage', validators=[validate_file_extension])
    text = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

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
