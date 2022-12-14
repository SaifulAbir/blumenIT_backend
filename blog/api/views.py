from requests import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from blog.pagination import BlogCustomPagination



from blog.models import BlogCategory
from blog.serializers import BlogCategorySerializer


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
            queryset = BlogCategory.objects.all().order_by('-created_at')
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
