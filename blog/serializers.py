from blog.models import BlogCategory, Blog, BlogReview, BlogReviewReply
from rest_framework import serializers
from django.db.models import Q


class BlogCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)

    class Meta:
        model = BlogCategory
        fields = ['id', 'title', 'is_active']


class BlogListDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ['id', 'is_active']


class BlogSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'blog_category', 'banner', 'banner', 'short_description', 'full_description',
                  'meta_title', 'meta_image', 'meta_description', 'meta_keywords', 'is_active', 'status']

    def create(self, validated_data):
        blog_instance = Blog.objects.create(
            **validated_data, created_by=self.context['request'].user)
        return blog_instance


class BlogListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    slug = serializers.SlugField(read_only=True)
    blog_category = BlogCategorySerializer()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'blog_category', 'banner', 'banner', 'short_description', 'full_description',
                  'meta_title', 'meta_image', 'meta_description', 'meta_keywords', 'is_active', 'status']

    def create(self, validated_data):
        blog_instance = Blog.objects.create(
            **validated_data, created_by=self.context['request'].user)
        return blog_instance


class CustomerBlogListSerializer(serializers.ModelSerializer):
    created_by_email = serializers.CharField(
        source='created_by.email', read_only=True)
    created_by_name = serializers.CharField(
        source='created_by.name', read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'banner', 'created_by_email', 'created_by_name',
                  'title', 'slug', 'view_count', 'created_at', 'is_active']


class PopularBlogSerializer(serializers.ModelSerializer):
    created_by_email = serializers.CharField(
        source='created_by.email', read_only=True)
    created_by_name = serializers.CharField(
        source='created_by.name', read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'thumbnail', 'title', 'created_by_email', 'created_by_name',
                  'created_at', 'slug', 'is_active', 'total_average_rating_number']


class BlogCommentsRepliesSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    created_at = serializers.DateTimeField(format="%d %B, %Y %I:%M %p")

    class Meta:
        model = BlogReviewReply
        fields = [
            'id',
            'review',
            'user',
            'user_name',
            'review_text',
            'created_at'
        ]


class BlogReviewSerializer(serializers.ModelSerializer):
    created_by_email = serializers.CharField(
        source='user.email', read_only=True)
    created_by_name = serializers.CharField(source='user.name', read_only=True)
    replies = serializers.SerializerMethodField('get_replies')
    created_at = serializers.DateTimeField(format="%d %B, %Y %I:%M %p")

    class Meta:
        model = BlogReview
        fields = ['id', 'reviewer_name', 'created_by_email', 'created_by_name',
                  'created_at', 'replies', 'review_text', 'rating_number']

    def get_replies(self, obj):
        replies = BlogReviewReply.objects.filter(review=obj, is_active=True).order_by('-created_at')
        return BlogCommentsRepliesSerializer(replies, many=True).data


class CustomerBlogDataSerializer(serializers.ModelSerializer):
    created_by_email = serializers.CharField(
        source='created_by.email', read_only=True)
    created_by_name = serializers.CharField(
        source='created_by.name', read_only=True)
    popular_blog = serializers.SerializerMethodField()
    blog_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['id', 'banner', 'title', 'created_by_email', 'created_by_name', 'view_count', 'created_at',
                  'full_description', 'popular_blog', 'blog_reviews', 'meta_title', 'meta_description', 'meta_image']

    def get_popular_blog(self, obj):
        try:
            queryset = Blog.objects.filter(Q(is_active=True), ~Q(
                id=obj.id)).order_by('-total_average_rating_number')[:8]
            serializer = PopularBlogSerializer(instance=queryset, many=True, context={
                                               'request': self.context['request']})
            return serializer.data
        except:
            return []

    def get_blog_reviews(self, obj):
        try:
            queryset = BlogReview.objects.filter(
                Q(is_active=True), Q(blog=obj.id)).order_by('-created_at')
            serializer = BlogReviewSerializer(instance=queryset, many=True, context={
                                              'request': self.context['request']})
            return serializer.data
        except:
            return []


class ReviewCreateSerializer(serializers.ModelSerializer):
    blog = serializers.PrimaryKeyRelatedField(
        queryset=Blog.objects.all(), many=False, write_only=True, required=True)
    review_text = serializers.CharField(required=True)
    reviewer_name = serializers.CharField(required=True)
    rating_number = serializers.FloatField(required=True)

    class Meta:
        model = BlogReview
        fields = ['id', 'blog', 'rating_number',
                  'review_text', 'reviewer_name']
