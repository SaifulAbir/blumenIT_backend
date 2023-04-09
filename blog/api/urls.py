from django.urls import path
from .views import *

urlpatterns = [
    path('blog-list/', CustomerBlogListAPIView.as_view()),
    path('blog-details/<str:slug>/', CustomerBlogDetailsAPIView.as_view()),
    path('review-create/', CustomerReviewCreateAPIView.as_view()),

    path('admin/blog-category-create/', BlogCategoryCreateAPIView.as_view()),
    path('admin/blog-category-list/', BlogCategoryListAPIView.as_view()),
    path('admin/blog-category-update/<int:id>/', BlogCategoryUpdateAPIView.as_view()),
    path('admin/blog-category-delete/<int:id>/', BlogCategoryDeleteAPIView.as_view()),

    path('admin/blog-create/', AdminBlogCreateAPIView.as_view()),
    path('admin/blog-update/<str:slug>/', AdminBlogUpdateAPIView.as_view()),
    path('admin/blog-list/', AdminBlogListAPIView.as_view()),
    path('admin/blog-list-delete/', AdminBlogListBulkDeleteAPI.as_view()),
    path('admin/blog-search/', AdminBlogSearchAPI.as_view()),
    path('admin/blog-details/<str:slug>/', AdminBlogDetailAPIView.as_view()),
    path('admin/blog-delete/<str:slug>/', AdminBlogDeleteAPIView.as_view()),


]