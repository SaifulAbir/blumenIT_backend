from django.contrib import admin
from blog.models import BlogCategory, Blog, BlogReview, BlogReviewReply

admin.site.register(Blog),
admin.site.register(BlogCategory)
admin.site.register(BlogReview)
admin.site.register(BlogReviewReply)
