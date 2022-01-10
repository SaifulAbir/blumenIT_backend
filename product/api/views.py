from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, DestroyAPIView 

from product.serializers import ProductSerializer
# from product.serializers import ProductSerializer, ProductCategoriesSerializer, ProductBrandsSerializer, ProductTagsSerializer

class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        return super(ProductCreateAPIView, self).post(request, *args, **kwargs)
