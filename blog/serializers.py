from blog.models import BlogCategory
from rest_framework import serializers


class BlogCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)

    class Meta:
        model = BlogCategory
        fields = ['id', 'title', 'is_active']