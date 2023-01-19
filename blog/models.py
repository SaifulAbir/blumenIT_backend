from django.db import models
from ecommerce.models import AbstractTimeStamp
from user.models import User
from django.db.models import Avg
from django.db.models.signals import pre_save
from .utils import unique_slug_generator_blog


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
        BlogCategory, related_name='blog_category', on_delete=models.PROTECT, null=True, blank=True)
    blog_text = models.TextField(default='', null=True, blank=True)
    banner = models.ImageField(upload_to='blog', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='blog', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='blog_created_user', blank=True, null=True)
    view_count = models.BigIntegerField(null=True, blank=True, default=0)
    total_average_rating_number = models.FloatField(null=True, blank=True, default=0.0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
        db_table = 'blogs'

    def __str__(self):
        return self.title

def pre_save_blog(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_blog(instance)

pre_save.connect(pre_save_blog, sender=Blog)


class BlogReview(AbstractTimeStamp):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True, related_name='blog_review_blog')
    user = models.ForeignKey(User, on_delete=models.SET_NULL,related_name='blog_review_user', blank=True, null=True)
    rating_number = models.FloatField(null=True, blank=True, default=0.0)
    review_text = models.TextField(default='', blank=True, null=True)
    reviewer_name = models.CharField(default='', blank=True, null=True, max_length=255)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'BlogReview'
        verbose_name_plural = 'BlogReviews'
        db_table = 'blog_review'

    def __str__(self):
        return 'Blog: '+ str(self.blog.title)

    def save(self, *args, **kwargs):
        super(BlogReview,self).save(*args, **kwargs)
        if self.blog:
            average_rating = BlogReview.objects.filter(blog=self.blog).aggregate(Avg('rating_number'))['rating_number__avg']
            Blog.objects.filter(id=self.blog.id).update(total_average_rating_number=average_rating)