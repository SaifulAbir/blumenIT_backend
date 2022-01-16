from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, DestroyAPIView 

from product.serializers import ProductCreateSerializer, ProductUpdateSerializer, TagCreateSerializer
# from product.serializers import ProductSerializer, ProductCategoriesSerializer, ProductBrandsSerializer, ProductTagsSerializer

from product.models import Product, Tags

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductCreateSerializer

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

class TagCreateAPIView(CreateAPIView):
    serializer_class = TagCreateSerializer
    queryset = Tags.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if self.request.data =={}:
            raise ValidationError({"name":'this field may not be null'
            })
        else:
            tag_name = self.request.data['name'].upper()
            tags = Tags.objects.filter(name = tag_name)
            # print(tags)
            if not tags.exists():
                obj = Tags()
                obj.name = tag_name
                obj.is_active = True
                obj.created_by = self.request.user.id
                obj.save()
                return Response({"id":self.request.user.id,"name":tag_name}, status=status.HTTP_200_OK)
            else:
                raise ValidationError({"name": str(tag_name)+' Tag name already exist.'})