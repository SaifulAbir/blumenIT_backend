from django.contrib import admin
from blog.models import BlogCategory, Blog

# Register your models here.
admin.site.register(Blog),
admin.site.register(BlogCategory)