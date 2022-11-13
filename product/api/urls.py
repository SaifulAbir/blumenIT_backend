from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('mega-menu-data/', MegaMenuDataAPIView.as_view()),
    path('product-details/<str:slug>/', ProductDetailsAPI.as_view()),
    path('product-list/', ProductListAPI.as_view()),
    path('search-product/', ProductSearchAPI.as_view()),
    path('product-list-by-category/<int:cid>/',
         ProductListByCategoryAPI.as_view()),
    path('product-list-by-sub-category/<int:subcid>/',
         ProductListBySubCategoryAPI.as_view()),
    path('product-list-by-sub-sub-category/<int:subsubcid>/',
         ProductListBySubSubCategoryAPI.as_view()),
    path('create-product-review/', ProductReviewCreateAPIView.as_view()),
    path('vendor-product-list-for-frontend/<int:vid>/',
         VendorProductListForFrondEndAPI.as_view()),
    path('brand-create/', BrandCreateAPIView.as_view()),

    # store front api
    # path('store-fetured-product-list/', FeaturedProductListStoreFront.as_view()),
    # path('store-popular-product-list/', PopularProductListStoreFront.as_view()),
    # path('store-gaming-product-list/', GamingProductListStoreFront.as_view()),
    # path('store-product-details/<str:slug>/', StoreProductDatailsAPI.as_view()),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
