from django.urls import path
from .views import *

urlpatterns = [

    path('product-all-category-list/', ProductAllCategoryListAPI.as_view()),
    path('mega-menu-data/', MegaMenuDataAPIView.as_view()),
    path('product-details/<str:slug>/', ProductDetailsAPI.as_view()),

    path('product-list-by-category/<int:cid>/', ProductListByCategoryAPI.as_view()),
    path('product-list-by-sub-category/<int:subcid>/', ProductListBySubCategoryAPI.as_view()),
    path('product-list-by-sub-sub-category/<int:subsubcid>/', ProductListBySubSubCategoryAPI.as_view()),


    # path('product-list/', ProductListAPI.as_view()),

    # path('create-product/', ProductCreateAPIView.as_view()),
    # path('create-tag/', TagCreateAPIView.as_view()),

    # path('product-list/', ProductListAPI.as_view()),
    # path('product-list-by-category/<int:cid>/', ProductListByCategoryAPI.as_view()),
    # path('product-list-by-sub-category/<int:subcid>/', ProductListBySubCategoryAPI.as_view()),
    # path('product-list-by-child-category/<int:childcid>/', ProductListByChildCategoryAPI.as_view()),
    # path('product-tags-list/', ProductTagsListAPI.as_view()),
    # 
    # path('tags-list/', TagsListAPI.as_view()),
    # path('product-category-list/', ProductCategoryListAPI.as_view()),
    # path('product-sub-category-list/<str:slug>/', ProductSubCategoryListAPI.as_view()),

    # path('product-brand-list/', ProductBrandListAPI.as_view()),

    # path('update-product/<str:slug>/', ProductUpdateAPIView.as_view()),
    # path('product-search/', ProductSearchAPIView.as_view()),

    # 

    # # vendor admin apies
    # path('vendor-admin/product-list/<int:id>/', VendorAdminProductListAPI.as_view()),


]

# product-sub-category-list/all/ or product-sub-category-list/1/