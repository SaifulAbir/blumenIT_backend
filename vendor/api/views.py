from datetime import datetime
from django.db.models import Q
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from product.pagination import ProductCustomPagination
from product.serializers import DiscountTypeSerializer, ProductTagsSerializer, TagsSerializer, VariantTypeSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from product.models import Brand, Category, DiscountTypes, Product, ProductAttributes, ProductReview, ProductTags, SubCategory, SubSubCategory, Tags, Units, VariantType, ProductVideoProvider, VatType, FilterAttributes
from user.models import CustomerProfile, User
from vendor.models import VendorRequest, Vendor, Seller
from vendor.serializers import AddNewSubCategorySerializer, AddNewSubSubCategorySerializer,\
    VendorBrandSerializer, AdminCategoryListSerializer, VendorProductListSerializer,\
    ProductUpdateSerializer, VendorProductViewSerializer, \
    SellerDetailSerializer, AdminSubCategoryListSerializer, \
    AdminSubSubCategoryListSerializer, VendorUnitSerializer, SellerSerializer, ProductAttributesSerializer, \
    ProductVideoProviderSerializer, ProductVatProviderSerializer, UpdateCategorySerializer,\
    UpdateSubSubCategorySerializer, ProductCreateSerializer, AddNewCategorySerializer, \
    SellerCreateSerializer, FlashDealCreateSerializer, UpdateSubCategorySerializer, FilteringAttributesSerializer, \
    AdminProfileSerializer, AdminOrderViewSerializer, AdminOrderListSerializer, AdminOrderUpdateSerializer
from cart.models import Order
from cart.serializers import OrderSerializer
from user.models import User
from cart.models import Coupon
from rest_framework.exceptions import ValidationError
from vendor.pagination import OrderCustomPagination


class AdminSellerCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerCreateSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True:
            return super(AdminSellerCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create seller, because you are not an Admin!'})


class AdminSellerDetailsAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_object(self):
        seller_id = self.kwargs['id']
        if self.request.user.is_superuser == True:
            try:
                query = Seller.objects.get(id=seller_id)
                return query
            except:
                raise ValidationError({"details": "Seller doesn't exist!"})
        else:
            raise ValidationError(
                {"msg": 'You can not see seller details, because you are not an Admin!'})


class AdminSellerListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            queryset = Seller.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No seller available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see seller list, because you are not an Admin!'})


class AdminSellerUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        seller_id = self.kwargs['id']
        if self.request.user.is_superuser == True:
            query = Seller.objects.filter(id=seller_id)
            if query:
                return query
            else:
                raise ValidationError({"msg": 'Seller not found'})
        else:
            raise ValidationError(
                {"msg": 'You can not update seller, because you are not an Admin!'})

class AdminSellerDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerSerializer
    queryset = Seller.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        seller_id = self.kwargs['id']
        if self.request.user.is_superuser == True:
            seller_obj = Seller.objects.filter(id=seller_id).exists()
            if seller_obj:
                seller_obj = Seller.objects.filter(id=seller_id)
                seller_obj.update(is_active=False)

                queryset = Seller.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Seller Does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not delete seller, because you are not an Admin!'})

class AdminProductCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductCreateSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True:
            return super(AdminProductCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create product, because you are not an Admin!'})

class AdminProductUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductUpdateSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs['slug']
        if self.request.user.is_superuser == True:
            query = Product.objects.filter(slug=slug)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Product does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not update this product, because you are not an Admin!'})

class AdminFilterAttributesAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FilteringAttributesSerializer
    def get_queryset(self):
        id = self.kwargs['id']
        type = self.kwargs['type']
        if self.request.user.is_superuser == True:
            if id and type:
                if type == 'category':
                    queryset = FilterAttributes.objects.filter(Q(category__id=id) & Q(is_active=True)).order_by('-created_at')
                if type == 'sub_category':
                    queryset = FilterAttributes.objects.filter(Q(sub_category__id=id) & Q(is_active=True)).order_by('-created_at')
                if type == 'sub_sub_category':
                    queryset = FilterAttributes.objects.filter(Q(sub_sub_category__id=id) & Q(is_active=True)).order_by('-created_at')

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": 'Filter Attributes not found!'})
        else:
            raise ValidationError({"msg": 'You can not see filtering attributes, because you are not an Admin!'})

class AdminCategoryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCategoryListSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            queryset = Category.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No category available!" })
        else:
            raise ValidationError(
                {"msg": 'You can not see category list, because you are not an Admin!'})

class AdminAddNewCategoryAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddNewCategorySerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True:
            return super(AdminAddNewCategoryAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create category, because you are not an Admin!'})

class AdminUpdateCategoryAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateCategorySerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True:
            query = Category.objects.filter(id=id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Category does not found!'})
        else:
            raise ValidationError({"msg": 'You can not update category, because you are not an Admin!'})

class AdminDeleteCategoryAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCategoryListSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True:
            category_obj_exist = Category.objects.filter(id=id).exists()
            if category_obj_exist:
                category_obj = Category.objects.filter(id=id)
                category_obj.update(is_active=False)
                queryset = Category.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Category Does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not delete category, because you are not an Admin!'})

class AdminSubCategoryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSubCategoryListSerializer
    lookup_field = 'cid'
    lookup_url_kwarg = "cid"

    def get_queryset(self):
        cid = self.kwargs['cid']
        if self.request.user.is_superuser == True:
            queryset = SubCategory.objects.filter(category=cid, is_active=True).order_by('-created_at')
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No sub category available!" })
        else:
            raise ValidationError(
                {"msg": 'You can not see sub category list, because you are not an Admin!'})

class AdminAddNewSubCategoryAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddNewSubCategorySerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True:
            return super(AdminAddNewSubCategoryAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create sub category, because you are not an Admin!'})

class AdminUpdateSubCategoryAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateSubCategorySerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True:
            query = SubCategory.objects.filter(id=id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Sub Category does not found!'})
        else:
            raise ValidationError({"msg": 'You can not update sub category, because you are not an Admin!'})

class AdminDeleteSubCategoryAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSubCategoryListSerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True:
            sub_category_obj_exist = SubCategory.objects.filter(
                id=id).exists()
            if sub_category_obj_exist:
                sub_category_obj = SubCategory.objects.filter(id=id)
                sub_category_obj.update(is_active=False)

                queryset = SubCategory.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Sub Category Does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not delete sub category, because you are not an Admin!'})

class AdminSubSubCategoryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSubSubCategoryListSerializer
    lookup_field = 'sid'
    lookup_url_kwarg = "sid"

    def get_queryset(self):
        sid = self.kwargs['sid']
        if self.request.user.is_superuser == True:
            if sid:
                queryset = SubSubCategory.objects.filter(
                    sub_category=sid, is_active=True).order_by('-created_at')
            else:
                queryset = SubSubCategory.objects.filter(
                    is_active=True).order_by('-created_at')
            return queryset
        else:
            raise ValidationError(
                {"msg": 'You can not see sub sub category list, because you are not an Admin!'})

class AdminAddNewSubSubCategoryAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddNewSubSubCategorySerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True:
            return super(AdminAddNewSubSubCategoryAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create sub sub category, because you are not an Admin!'})

class AdminUpdateSubSubCategoryAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateSubSubCategorySerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True:
            query = SubSubCategory.objects.filter(id=id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Sub Sub Category does not found!'})
        else:
            raise ValidationError({"msg": 'You can not update sub sub category, because you are not an Admin!'})

class AdminDeleteSubSubCategoryAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSubSubCategoryListSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True:
            sub_sub_category_obj_exist = SubSubCategory.objects.filter(id=id).exists()
            if sub_sub_category_obj_exist:
                sub_sub_category_obj = SubSubCategory.objects.filter(id=id)
                sub_sub_category_obj.update(is_active=False)

                queryset = SubSubCategory.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Sub Sub Category Does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not delete sub sub category, because you are not an Admin!'})

class AdminBrandListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorBrandSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            queryset = Brand.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No brand available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see brand list, because you are not an Admin!'})

class AdminUnitListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorUnitSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            queryset = Units.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No unit available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see unit list, because you are not an Admin!'})

class AdminDiscountListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = DiscountTypeSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            queryset = DiscountTypes.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No discount available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see discount list, because you are not an Admin!'})

class AdminTagListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TagsSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            queryset = Tags.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No tag available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see tag list, because you are not an Admin!'})

class VendorAttributeListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = ProductAttributes.objects.filter(is_active=True)
    serializer_class = ProductAttributesSerializer

class VendorVariantListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = VariantType.objects.filter(is_active=True)
    serializer_class = VariantTypeSerializer

class AdminProductListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorProductListSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            queryset = Product.objects.filter(status='PUBLISH').order_by('-created_at')
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "Product doesn't exist! " })
        else:
            raise ValidationError(
                {"msg": 'You can not show product list, because you are not an Admin!'})

class AdminProductViewAPI(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorProductViewSerializer
    lookup_field = 'slugi'
    lookup_url_kwarg = "slugi"

    def get_object(self):
        slug = self.kwargs['slugi']
        if self.request.user.is_superuser == True:
            query = Product.objects.get(slug=slug)
            if query:
                return query
            else:
                raise ValidationError({"msg": "Product doesn't exist! " })
        else:
            raise ValidationError(
                {"msg": 'You can not show product view, because you are not an Admin!'})

class AdminProductDeleteAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorProductListSerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs['slug']
        if self.request.user.is_superuser == True:
            product_obj_exist = Product.objects.filter(
                slug=slug).exists()
            if product_obj_exist:
                product_obj = Product.objects.filter(slug=slug)
                product_obj.update(status='UNPUBLISH')

                queryset = Product.objects.filter(status='PUBLISH').order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Product Does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not delete this product, because you are not an Admin!'})

class AdminVideoProviderListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductVideoProviderSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            queryset = ProductVideoProvider.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Video provider data does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not view video provider list, because you are not an Admin!'})

class AdminVatTypeListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductVatProviderSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            queryset = VatType.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Vat types does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not view Vat types list, because you are not an Admin!'})

class AdminFlashDealCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FlashDealCreateSerializer


    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True:
            return super(AdminFlashDealCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create flash deal, because you are not an Admin!'})

class AdminProfileAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminProfileSerializer

    def get_object(self):
        if self.request.user.is_superuser == True:
            query = User.objects.get(id=self.request.user.id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'User does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not view your profile, because you are not an Admin!'})


class AdminOrderList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminOrderListSerializer
    pagination_class = OrderCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            request = self.request
            type = request.GET.get('type')

            queryset = Order.objects.all().order_by('-created_at')

            if type == 'seller':
                queryset = queryset.filter(user=Seller)

            if type == 'in_house_order':
                queryset = queryset.filter(vendor__product_seller__in_house_product=True)
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no order till now "})
        else:
            raise ValidationError(
                {"msg": 'You can not show order list, because you are not an Admin!'})

class AdminOrderViewAPI(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminOrderViewSerializer
    lookup_field = 'o_id'
    lookup_url_kwarg = "o_id"

    def get_object(self):
        id = self.kwargs['o_id']
        if self.request.user.is_superuser == True:
            query = Order.objects.get(order_id=id)
            if query:
                return query
            else:
                raise ValidationError({"msg": "No Order available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not show order, because you are not an Admin!'})


class OrderListSearchAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = OrderCustomPagination
    serializer_class = AdminOrderListSerializer


    def get_queryset(self):
        if self.request.user.is_superuser == True:
            request = self.request
            query = request.GET.get('search')
            orders = request.GET.get('order_status')
            date = request.GET.get('order_date')
            start_date = request.GET.get('start')
            end_date = request.GET.get('end')
            # date = Sample.objects.filter(date_created__gte=date_created_start,
            #                       date_created__lte=date_created_end)

            queryset = Order.objects.all().order_by('-created_at')

            if query:
                queryset = queryset.filter(
                    Q(order_id__icontains=query)
                )
            if date:
                queryset = queryset.filter(
                    Q(order_date__gte=start_date) & Q(order_date__lte=end_date)
                )
            if orders:
                queryset = queryset.filter(order_status=orders)

            return queryset
        else:
            raise ValidationError(
                {"msg": 'You can not show Order list, because you are not an Admin!'})


class AdminOrderUpdateAPI(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminOrderUpdateSerializer
    lookup_field = 'o_id'
    lookup_url_kwarg = "o_id"


    def get_queryset(self):
        id = self.kwargs['o_id']
        if self.request.user.is_superuser == True:
            request = self.request

            order_status = request.GET.get('order_status')
            payment_status = request.GET.get('payment_status')
            queryset = Order.objects.filter(order_id=id)
            order_obj_exist = Order.objects.filter(order_id=id).exists()
            if order_obj_exist:
                if order_status:
                    order_obj = queryset.objects.filter(order_id=id)
                    order_obj.update(order_status=order_status)
                if payment_status:
                    order_obj = queryset.objects.filter(order_id=id)
                    order_obj.update(payment_status=payment_status)
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Order Does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not show order, because you are not an Admin!'})


