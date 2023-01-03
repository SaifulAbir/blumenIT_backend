from django.db import models
from ecommerce.models import AbstractTimeStamp


class BlogCategory(AbstractTimeStamp):
    title = models.CharField(max_length=100, help_text="name")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'BlogCategory'
        verbose_name_plural = 'BlogCategories'
        db_table = 'blog_categories'

    def __str__(self):
        return self.title


class Blog(AbstractTimeStamp):
    title = models.CharField(max_length=100, help_text="name")
    slug = models.SlugField(
        null=False, allow_unicode=True, blank=True, max_length=255)
    blog_category = models.ForeignKey(
        BlogCategory, related_name='blog_category', on_delete=models.PROTECT)
    full_description = models.TextField()
    short_description = models.CharField(max_length=800)
    banner = models.ImageField(upload_to='blog', blank=True, null=True)
    status = models.BooleanField(default=True, null=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
        db_table = 'blogs'

    def __str__(self):
        return self.title
