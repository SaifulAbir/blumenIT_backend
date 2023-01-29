from django.contrib import admin
from blog.models import BlogCategory, Blog, BlogReview

admin.site.register(Blog),
admin.site.register(BlogCategory)
admin.site.register(BlogReview)