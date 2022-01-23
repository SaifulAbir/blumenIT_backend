from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, DestroyAPIView 

from product.serializers import ProductSerializer, ProductUpdateSerializer
# from product.serializers import ProductSerializer, ProductCategoriesSerializer, ProductBrandsSerializer, ProductTagsSerializer

from product.models import Product

class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        return super(ProductCreateAPIView, self).post(request, *args, **kwargs)

class ProductUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ProductUpdateSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs['slug']
        query = Product.objects.filter(slug=slug)
        return query

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)