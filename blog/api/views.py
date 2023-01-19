from requests import Response
from django.db.models import Q
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from blog.pagination import BlogCustomPagination



from blog.models import BlogCategory, Blog
from blog.serializers import BlogCategorySerializer, BlogSerializer, CustomerBlogListSerializer, CustomerBlogDataSerializer, \
    ReviewCreateSerializer


class BlogCategoryCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = BlogCategorySerializer
    def post(self, request):
        if self.request.user.is_superuser == True:
            blog_category = BlogCategorySerializer(data=request.data)

            if BlogCategory.objects.filter(**request.data).exists():
                raise serializers.ValidationError('This data already exists')

            if blog_category.is_valid():
                blog_category.save()
                return Response(blog_category.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            raise ValidationError(
                {"msg": 'You can not create Blog Category, because you are not an Admin!'}
            )


class BlogCategoryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogCategorySerializer
    pagination_class = BlogCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            queryset = BlogCategory.objects.filter(is_active=True).order_by('-created_at')
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Blog Category does not exist!'}
                )
        else:
            raise ValidationError(
                {"msg": 'You can not view Blog Category List, because you are not an Admin!'}
            )


class BlogCategoryUpdateAPIView(RetrieveUpdateAPIView):
        permission_classes = [IsAuthenticated]
        serializer_class = BlogCategorySerializer
        lookup_field = 'id'
        lookup_url_kwarg = "id"

        def get_queryset(self):
            blogcat_id = self.kwargs['id']
            if self.request.user.is_superuser == True:
                queryset = BlogCategory.objects.filter(id=blogcat_id)
                if queryset:
                    return queryset
                else:
                    raise ValidationError({"msg": 'Blog Category not found'})
            else:
                raise ValidationError(
                    {"msg": 'You can not update coupon, because you are not an Admin!'})


class BlogCategoryDeleteAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BlogCategorySerializer
    queryset =  BlogCategory.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            bcat_id = self.kwargs['id']
            brand_obj = BlogCategory.objects.filter(id=bcat_id).exists()
            if brand_obj:
                brand_obj = BlogCategory.objects.filter(id=bcat_id)
                brand_obj.update(is_active=False)

                queryset = BlogCategory.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Blog Category Does not exist!'}
                )
        else:
            raise ValidationError(
                {"msg": 'You can not update coupon, because you are not an Admin!'})


class AdminBlogCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True:
            return super(AdminBlogCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create seller, because you are not an Admin!'}
            )


class AdminBlogDetailAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get_object(self):
        slug = self.kwargs['slug']
        if self.request.user.is_superuser == True:
            try:
                query = Blog.objects.get(slug=slug)
                return query
            except:
                raise ValidationError(
                    {"details": "Blog doesn't exist!"}
                )
        else:
            raise ValidationError(
                {"msg": 'You can not see Blog details, because you are not an Admin!'}
            )


class AdminBlogListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer
    pagination_class = BlogCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            queryset = Blog.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No Blog available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see Blog list, because you are not an Admin!'})


class AdminBlogSearchAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = BlogCustomPagination
    serializer_class = BlogSerializer

    def get_object(self):
        if self.request.user.is_superuser == True:
            request = self.request
            query = request.GET.get('search')

            queryset = Blog.objects.all().order_by('-created_at')
            if query:
                queryset = queryset.filter(
                    Q(order_id__icontains=query)
                )

            return queryset
        else:
            raise ValidationError(
                {"msg": 'You can not show Blog list, because you are not an Admin!'})


class AdminBlogUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs['slug']
        if self.request.user.is_superuser == True:
            query = Blog.objects.filter(slug=slug)
            if query:
                return query
            else:
                raise ValidationError({"msg": 'Blog not found'})
        else:
            raise ValidationError(
                {"msg": 'You can not update blog, because you are not an Admin!'})


class AdminBlogDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer
    pagination_class = BlogCustomPagination
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs['slug']
        if self.request.user.is_superuser == True:
            blog_obj_exist = Blog.objects.filter(
                slug=slug).exists()
            if blog_obj_exist:
                product_obj = Blog.objects.filter(slug=slug)
                product_obj.update(is_active=False)

                queryset = Blog.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Blog Does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not delete this blog, because you are not an Admin!'})


class CustomerBlogListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomerBlogListSerializer
    pagination_class = BlogCustomPagination

    def get_queryset(self):
        queryset = Blog.objects.filter(is_active=True).order_by('-created_at')
        if queryset:
            return queryset
        else:
            raise ValidationError(
                {"msg": 'Blog data does not exist!'}
            )


class CustomerBlogDetailsAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomerBlogDataSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get_object(self):
        slug = self.kwargs['slug']
        try:
            query = Blog.objects.get(slug=slug)
            return query
        except:
            raise ValidationError(
                {"details": "Blog doesn't exist!"}
            )


class CustomerReviewCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReviewCreateSerializer

    def post(self, request, *args, **kwargs):
        return super(CustomerReviewCreateAPIView, self).post(request, *args, **kwargs)



