from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path('store-category-list/', StoreCategoryListAPIView.as_view()), # mega menu api for front end
     path('product-details/<str:slug>/', ProductDetailsAPI.as_view()),
     path('product-list/', ProductListAPI.as_view()),
     path('search-product/', ProductSearchAPI.as_view()),
     path('filtering-attributes/<int:id>/<str:type>/',FilterAttributesAPI.as_view()),
     path('product-list-by-category-popular-products/<int:id>/<str:type>/<int:pagination>/',
          ProductListByCategoryPopularProductsAPI.as_view()),
     path('product-list-by-category/<int:cid>/<int:pagination>/',
          ProductListByCategoryAPI.as_view()),
     path('product-list-by-sub-category/<int:subcid>/<int:pagination>/',
          ProductListBySubCategoryAPI.as_view()),
     path('product-list-by-sub-sub-category/<int:subsubcid>/<int:pagination>/',
          ProductListBySubSubCategoryAPI.as_view()),
     path('create-product-review/', ProductReviewCreateAPIView.as_view()),
     path('vendor-product-list-for-frontend/<int:vid>/',
          VendorProductListForFrondEndAPI.as_view()),
     path('admin-brand-create/', BrandCreateAPIView.as_view()),
     path('admin-brand-delete/<int:id>/', BrandDeleteAPIView.as_view()),
     path('only-title/', OnlyTitleAPIView.as_view()),

     path('pc_builder-categories/',PcBuilderCategoryAPIView.as_view()),
     path('pc_builder/',PcBuilderChooseAPIView.as_view()),

     path('gaming-category-list/', GamingCategoryListAPIView.as_view()),
     path('product-list-by-category-gaming-popular-products/<int:id>/<str:type>/<int:pagination>/',
          ProductListByCategoryGamingPopularProductsAPI.as_view()),
     path('gaming-featured-product-list/<int:pagination>/', GamingFeaturedProductListAPI.as_view()),
     path('brand-list/', BrandListAPIView.as_view()),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
