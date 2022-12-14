from django.urls import path
from .views import *

urlpatterns = [
    path('admin/blog-category-create/', BlogCategoryCreateAPIView.as_view()),
    path('admin/blog-category-list/', BlogCategoryListAPIView.as_view()),
    path('admin/blog-category-update/<int:id>/', BlogCategoryUpdateAPIView.as_view()),

]