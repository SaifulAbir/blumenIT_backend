
from blog.models import BlogCategory, Blog
from rest_framework import serializers


class BlogCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)

    class Meta:
        model = BlogCategory
        fields = ['id', 'title', 'is_active']

class BlogSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    slug = serializers.SlugField(required=True)

    class Meta:
        model = Blog
        fields = ['id','title', 'slug', 'blog_category', 'full_description', 'short_description', 'status', 'is_active']
