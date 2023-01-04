from django.contrib import admin
from blog.models import BlogCategory, Blog

admin.site.register(Blog),
admin.site.register(BlogCategory)