from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, DestroyAPIView

from product.serializers import ProductCreateSerializer, ProductUpdateSerializer, ProductListSerializer, TagCreateSerializer,ProductTagsSerializer,  TagListSerializer, ProductCategoryListSerializer, ProductBrandListSerializer, ProductSubCategoryListSerializer, ProductDetailsSerializer

from product.models import Product, Tags, ProductTags, ProductCategory, ProductSubCategory, ProductBrand

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from product.pagination import ProductCustomPagination


# create API views start
class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductCreateSerializer

    def post(self, request, *args, **kwargs):
        return super(ProductCreateAPIView, self).post(request, *args, **kwargs)

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
# create API views end

# list API views start
class ProductListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.filter(status='ACTIVE').order_by('-created_at')
    serializer_class = ProductListSerializer
    pagination_class = ProductCustomPagination

class ProductTagsListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = ProductTags.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ProductTagsSerializer

class TagsListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Tags.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = TagListSerializer

class ProductCategoryListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = ProductCategory.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ProductCategoryListSerializer

class ProductSubCategoryListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductSubCategoryListSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"
    def get_queryset(self):
        slug = self.kwargs['slug']
        if slug == 'all':
            queryset = ProductSubCategory.objects.filter(is_active=True).order_by('-created_at')
        else:
            queryset = ProductSubCategory.objects.filter(category=slug).order_by('-created_at')
        return queryset

class ProductBrandListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = ProductBrand.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ProductBrandListSerializer

class ProductDetailsAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductDetailsSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"
    def get_queryset(self):
        slug = self.kwargs['slug']
        query = Product.objects.filter(slug=slug)
        return query

# list API views end


# update API views start
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
# update API views end

