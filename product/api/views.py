from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, DestroyAPIView 

from product.serializers import ProductSerializer, ProductCategoriesSerializer, ProductBrandsSerializer

class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        return super(ProductCreateAPIView, self).post(request, *args, **kwargs)

class ProductCategoriesCreateAPI(CreateAPIView):
    serializer_class = ProductCategoriesSerializer

    def post(self, request, *args, **kwargs):
        return super(ProductCategoriesCreateAPI, self).post(request, *args, **kwargs)

class ProductBrandsCreateAPI(CreateAPIView):
    serializer_class = ProductBrandsSerializer

    def post(self, request, *args, **kwargs):
        return super(ProductBrandsCreateAPI, self).post(request, *args, **kwargs)