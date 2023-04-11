from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from blog.models import Blog
from product.pagination import ProductCustomPagination
from product.serializers import DiscountTypeSerializer, TagsSerializer, ProductListBySerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from product.models import Brand, Category, DiscountTypes, Product, ProductReview, SubCategory, SubSubCategory, Tags, \
    Units, ProductImages, \
    ProductVideoProvider, VatType, FilterAttributes, Attribute, AttributeValues, Inventory, FlashDealInfo, Warranty, \
    ShippingClass, SpecificationTitle, Offer, ShippingCountry, ShippingState, ShippingCity, OfferCategory
from user.models import User
from user.serializers import CustomerProfileSerializer
from vendor.models import Seller
from home.models import CorporateDeal, Advertisement, HomeSingleRowData, RequestQuote, ContactUs
from vendor.serializers import AddNewSubCategorySerializer, AddNewSubSubCategorySerializer, \
    VendorBrandSerializer, AdminCategoryListSerializer, VendorProductListSerializer, \
    ProductUpdateSerializer, VendorProductViewSerializer, AdminSubCategoryListSerializer, \
    AdminSubSubCategoryListSerializer, VendorUnitSerializer, SellerSerializer, \
    ProductVideoProviderSerializer, ProductVatProviderSerializer, UpdateCategorySerializer, \
    UpdateSubSubCategorySerializer, ProductCreateSerializer, AddNewCategorySerializer, \
    SellerCreateSerializer, FlashDealInfoSerializer, UpdateSubCategorySerializer, FilteringAttributesSerializer, \
    AdminProfileSerializer, AdminContactUsSerializer, AdminOfferDetailsSerializer, \
    ReviewListSerializer, AttributeSerializer, AttributeValuesSerializer, AdminFilterAttributeSerializer, \
    SellerCreateSerializer, UpdateSubCategorySerializer, FilteringAttributesSerializer, \
    AdminProfileSerializer, AdminOrderViewSerializer, AdminOrderListSerializer, AdminOrderUpdateSerializer, \
    AdminCustomerListSerializer, AdminRequestQuoteSerializer, AdminTicketConversationSerializer, \
    AdminTicketListSerializer, AdminTicketDataSerializer, TicketStatusSerializer, CategoryWiseProductSaleSerializer, \
    CategoryWiseProductStockSerializer, AdminWarrantyListSerializer, AdminShippingClassSerializer, \
    AdminSpecificationTitleSerializer, AdminSubscribersListSerializer, AdminCorporateDealSerializer, \
    AdminCouponSerializer, VatTypeSerializer, WebsiteConfigurationSerializer, AdminFilterAttributeValueSerializer, \
    AdminOfferSerializer, AdminPosProductListSerializer, AdminShippingCountrySerializer, AdminShippingCitySerializer, \
    AdminShippingStateSerializer, AdminPosOrderSerializer, AdminCategoryToggleSerializer, AdminProductToggleSerializer, \
    AdminBlogToggleSerializer, AdminProductReviewSerializer, AdvertisementPosterSerializer, \
    ProductUpdateDetailsSerializer, \
    AdminPosCustomerCreateSerializer, AdminSubCategoryToggleSerializer, AdminOfferCategoryListSerializer, \
    AdminBrandIsGamingSerializer, \
    AdminCategoryIsPcBuilderSerializer, UpdateCategoryDetailsSerializer, UpdateSubCategoryDetailsSerializer, \
    UpdateSubSubCategoryDetailsSerializer, WebsiteConfigurationViewSerializer, WebsiteConfigurationUpdateSerializer, \
    GeneralSettingsViewSerializer

from cart.models import Order, OrderItem, Coupon
from cart.models import Order, OrderItem, SubOrder
from user.models import User, Subscription
from rest_framework.exceptions import ValidationError
from vendor.pagination import OrderCustomPagination
from support_ticket.models import Ticket

# Seller related admin apies views............................ start
class AdminSellerCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerCreateSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminSellerCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create seller, because you are not an Admin or a Staff!'})


class AdminSellerDetailsAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_object(self):
        seller_id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            try:
                query = Seller.objects.get(id=seller_id)
                return query
            except:
                raise ValidationError({"details": "Seller doesn't exist!"})
        else:
            raise ValidationError(
                {"msg": 'You can not see seller details, because you are not an Admin or a Staff!'})

class SellerListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SellerSerializer

    def get_queryset(self):
        queryset = Seller.objects.filter(is_active=True)
        if queryset:
            return queryset
        else:
            raise ValidationError({"msg": "No seller available! " })

class AdminSellerListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = Seller.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No seller available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see seller list, because you are not an Admin or a staff!'})


class AdminSellerUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        seller_id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            query = Seller.objects.filter(id=seller_id)
            if query:
                return query
            else:
                raise ValidationError({"msg": 'Seller not found'})
        else:
            query = Seller.objects.filter(id=seller_id, user=self.request.user)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'You can not update seller, because you are not an Admin, Staff or owner!'})
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class AdminSellerDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerSerializer
    queryset = Seller.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        seller_id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
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
                {"msg": 'You can not delete seller, because you are not an Admin or a Staff!'})
# Seller related admin apies views............................ end


# Product related admin apies views............................ start
class AdminProductCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductCreateSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            return super(AdminProductCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create product, because you are not an Admin or a Staff or a vendor!'})


# class AdminProductUpdateAPIView(RetrieveUpdateAPIView):
class AdminProductUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductUpdateSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs['slug']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            query = Product.objects.filter(slug=slug)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Product does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not update this product, because you are not an Admin or a Staff or a vendor!'})


class AdminProductUpdateDetailsAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductUpdateDetailsSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs['slug']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            query = Product.objects.filter(slug=slug)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Product does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not update this product, because you are not an Admin or a Staff or a vendor!'})
        

class AdminDeleteProductImageAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def put(self, request, *args, **kwargs):
        try:
            image_id = self.kwargs['id']
            product_image_obj_exist = ProductImages.objects.filter(id=image_id).exists()
            if product_image_obj_exist:
                product_image_obj = ProductImages.objects.filter(id=image_id)
                if product_image_obj:
                    product_image_obj.update(is_active=False)
            return Response({"msg": "Successfully deleted!"})
        except KeyError:
            raise ValidationError({"msg": 'Image delete failed!'})


class AdminProductListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorProductListSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            request = self.request
            type = request.GET.get('type')

            if self.request.user.is_seller == True:
                queryset = Product.objects.filter(is_active=True, seller=Seller.objects.get(seller_user=self.request.user.id)).order_by('-created_at')
            else:
                queryset = Product.objects.filter(is_active=True).order_by('-created_at')

            if type == 'digital':
                queryset = queryset.filter(digital=True)
            if type == 'in_house_product':
                queryset = queryset.filter(in_house_product=True)
            if type == 'whole_sale_product':
                queryset = queryset.filter(whole_sale_product=True)

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "Product doesn't exist! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see product list, because you are not an Admin or a Staff or a vendor!'})


class AdminProductListSearchAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = VendorProductListSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            request = self.request

            seller = request.GET.get('seller')
            sort_by = request.GET.get('sort_by')
            query = request.GET.get('search')

            if self.request.user.is_seller == True:
                queryset = Product.objects.filter(is_active=True, seller=Seller.objects.get(seller_user=self.request.user.id)).order_by('-created_at')
            else:
                queryset = Product.objects.filter(is_active=True).order_by('-created_at')

            if seller:
                queryset = queryset.filter(seller__id=seller)

            if sort_by:
                if sort_by == 'rating_high_low':
                    queryset = queryset.order_by('-total_average_rating_number')

                if sort_by == 'rating_low_high':
                    queryset = queryset.order_by('total_average_rating_number')
                if sort_by == 'num_of_sale_high_low':
                    queryset = queryset.order_by('-sell_count')
                if sort_by == 'num_of_sale_low_high':
                    queryset = queryset.order_by('sell_count')

            if query:
                queryset = queryset.filter(Q(title__icontains=query))

            return queryset
        else:
            raise ValidationError(
                {"msg": 'You can not see product list, because you are not an Admin or a Staff or a vendor!'})


class AdminProductViewAPI(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorProductViewSerializer
    lookup_field = 'slugi'
    lookup_url_kwarg = "slugi"

    def get_object(self):
        slug = self.kwargs['slugi']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            query = Product.objects.get(slug=slug)
            if query:
                return query
            else:
                raise ValidationError({"msg": "Product doesn't exist! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see product view, because you are not an Admin or a Staff or a vendor!'})


class AdminProductDeleteAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorProductListSerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'slug'
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs['slug']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            product_obj_exist = Product.objects.filter(slug=slug).exists()
            if product_obj_exist:
                product_obj = Product.objects.filter(slug=slug)
                product_obj.update(is_active=False, status='UNPUBLISH')

                queryset = Product.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Product Does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not delete this product, because you are not an Admin or a Staff or a vendor!'})
# Product related admin apies views............................ end


# Category,SubCategory,SubSubCategory related admin apies views............................ start
class AdminCategoryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCategoryListSerializer
    pagination_class = OrderCustomPagination

    def get_queryset(self):
        request = self.request
        search = request.GET.get('search')
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = Category.objects.filter(is_active=True).order_by('-created_at')
            if search:
                queryset = queryset.filter(Q(title__icontains=search))
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No category available!" })
        else:
            raise ValidationError(
                {"msg": 'You can not see category list, because you are not an Admin or a Staff!'})


class AdminAddNewCategoryAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddNewCategorySerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminAddNewCategoryAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create category, because you are not an Admin or a Staff!'})


# class AdminUpdateCategoryAPIView(RetrieveUpdateAPIView):
class AdminUpdateCategoryDetailsAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateCategoryDetailsSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            query = Category.objects.filter(id=id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Category does not found!'})
        else:
            raise ValidationError({"msg": 'You can not update category, because you are not an Admin or a Staff!'})

class AdminUpdateCategoryAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateCategorySerializer
    queryset = Category.objects.all()
    # lookup_field = 'id'
    # lookup_url_kwarg = "id"

    # def get_queryset(self):
    #     id = self.kwargs['id']
    #     if self.request.user.is_superuser == True or self.request.user.is_staff == True:
    #         query = Category.objects.filter(id=id)
    #         if query:
    #             return query
    #         else:
    #             raise ValidationError(
    #                 {"msg": 'Category does not found!'})
    #     else:
    #         raise ValidationError({"msg": 'You can not update category, because you are not an Admin or a Staff!'})


class AdminDeleteCategoryAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCategoryListSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
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
            raise ValidationError({"msg": 'You can not delete category, because you are not an Admin or a Staff!'})


class AdminSubCategoryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSubCategoryListSerializer
    lookup_field = 'cid'
    lookup_url_kwarg = "cid"

    def get_queryset(self):
        cid = self.kwargs['cid']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = SubCategory.objects.filter(category=cid, is_active=True).order_by('-created_at')
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No sub category available!" })
        else:
            raise ValidationError(
                {"msg": 'You can not see sub category list, because you are not an Admin or a Staff!'})


class AdminAddNewSubCategoryAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddNewSubCategorySerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminAddNewSubCategoryAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create sub category, because you are not an Admin or a Staff!'})


class AdminUpdateSubCategoryDetailsAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateSubCategoryDetailsSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            query = SubCategory.objects.filter(id=id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Sub Category does not found!'})
        else:
            raise ValidationError({"msg": 'You can not update sub category, because you are not an Admin or a Staff!'})

class AdminUpdateSubCategoryAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateSubCategorySerializer
    queryset = SubCategory.objects.all()


class AdminDeleteSubCategoryAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSubCategoryListSerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            sub_category_obj_exist = SubCategory.objects.filter(
                id=id).exists()
            if sub_category_obj_exist:
                SubCategory.objects.filter(id=id).update(is_active=False)

                queryset = SubCategory.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Sub Category Does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not delete sub category, because you are not an Admin or a Staff!'})


class AdminSubSubCategoryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSubSubCategoryListSerializer
    lookup_field = 'sid'
    lookup_url_kwarg = "sid"

    def get_queryset(self):
        sid = self.kwargs['sid']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            if sid:
                queryset = SubSubCategory.objects.filter(
                    sub_category=sid, is_active=True).order_by('-created_at')
            else:
                queryset = SubSubCategory.objects.filter(
                    is_active=True).order_by('-created_at')
            return queryset
        else:
            raise ValidationError(
                {"msg": 'You can not see sub sub category list, because you are not an Admin or a Staff!'})


class AdminAddNewSubSubCategoryAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddNewSubSubCategorySerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminAddNewSubSubCategoryAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create sub sub category, because you are not an Admin or a Staff!'})


class AdminUpdateSubSubCategoryDetailsAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateSubSubCategoryDetailsSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            query = SubSubCategory.objects.filter(id=id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Sub Sub Category does not found!'})
        else:
            raise ValidationError({"msg": 'You can not update sub sub category, because you are not an Admin or a Staff!'})


class AdminUpdateSubSubCategoryAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateSubSubCategorySerializer
    queryset = SubSubCategory.objects.all()


class AdminDeleteSubSubCategoryAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSubSubCategoryListSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
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
            raise ValidationError({"msg": 'You can not delete sub sub category, because you are not an Admin or a Staff!'})
# Category,SubCategory,SubSubCategory related admin apies views............................ end


class AdminBrandListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorBrandSerializer
    pagination_class = OrderCustomPagination

    def get_queryset(self):
        request = self.request
        search = request.GET.get('search')
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = Brand.objects.filter(is_active=True).order_by('-created_at')
            if search:
                queryset = queryset.filter(Q(title__icontains=search))
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No brand available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see brand list, because you are not an Admin or a Staff!'})


# Unit related admin apies views............................ start
class AdminUnitListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorUnitSerializer
    pagination_class = OrderCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = Units.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No unit available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see unit list, because you are not an Admin or a Staff!'})


class AdminUnitAddAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorUnitSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminUnitAddAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create unit, because you are not an Admin or a Staff!'})


class AdminUnitUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorUnitSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            query = Units.objects.filter(id=id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Units does not found!'})
        else:
            raise ValidationError({"msg": 'You can not update Units, because you are not an Admin or a Staff!'})


class AdminUnitDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorUnitSerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            sub_category_obj_exist = Units.objects.filter(id=id).exists()
            if sub_category_obj_exist:
                Units.objects.filter(id=id).update(is_active=False)

                queryset = Units.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Units Does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not delete Units, because you are not an Admin or a Staff!'})
# Unit related admin apies views............................ end


# Flash Deal related admin apies views............................ start
class AdminFlashDealCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FlashDealInfoSerializer


    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminFlashDealCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create flash deal, because you are not an Admin or a Staff!'})


class AdminFlashDealUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FlashDealInfoSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            query = FlashDealInfo.objects.filter(id=id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Flash Deal does not found!'})
        else:
            raise ValidationError({"msg": 'You can not update flash deal, because you are not an Admin or a Staff!'})


class AdminFlashDealDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = FlashDealInfoSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            flash_deal_info_obj = FlashDealInfo.objects.filter(id=id).exists()
            if flash_deal_info_obj:
                flash_deal_info_obj = FlashDealInfo.objects.filter(id=id)
                flash_deal_info_obj.update(is_active=False)

                queryset = FlashDealInfo.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Flash Deal Info Does not exist!'}
                )
        else:
            raise ValidationError({"msg": 'You can not delete flash deal, because you are not an Admin or a Staff!'})


class AdminFlashDealListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FlashDealInfoSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = FlashDealInfo.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Flash Deal does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not view Flash Deal list, because you are not an Admin or a Staff!'})
# Flash Deal related admin apies views............................ end


class AdminProfileAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminProfileSerializer

    def get_object(self):
        # if self.request.user.is_staff == True:
        query = User.objects.get(id=self.request.user.id)
        if query:
            return query
        else:
            raise ValidationError(
                {"msg": 'User does not exist!'})
        # else:
        #     raise ValidationError({"msg": 'You can not view your profile, because you are not a Staff!'})


# Review related admin apies views............................ start
class AdminReviewListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewListSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        request = self.request
        rating_high_to_low = request.GET.get('rating_high_to_low')
        rating_low_to_high = request.GET.get('rating_low_to_high')
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = ProductReview.objects.all().order_by('-created_at')

            if rating_high_to_low:
                queryset = queryset.order_by('-rating_number').distinct()

            if rating_low_to_high:
                queryset = queryset.order_by('rating_number').distinct()

            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Review data does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not view review data list, because you are not an Admin or a Staff!'})


class AdminReviewInactiveAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewListSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            review_obj_exist = ProductReview.objects.filter(id=id).exists()
            if review_obj_exist:
                review_obj = ProductReview.objects.filter(id=id)
                review_obj.update(is_active=False)
                queryset = ProductReview.objects.all().order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Review data does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not update review data, because you are not an Admin or a Staff!'})


class ReviewSearchAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = ReviewListSerializer

    def get_queryset(self):
        request = self.request
        query = request.GET.get('search')
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = ProductReview.objects.all().order_by('-created_at')
            if query:
                queryset = queryset.filter(Q(product__title__icontains=query) | Q(user__username__icontains=query) | Q(rating_number__icontains=query) | Q(review_text__icontains=query))

            return queryset
        else:
            raise ValidationError({"msg": 'You can not search review data, because you are not an Admin or a Staff!'})
# Review related admin apies views............................ end


# Attribute, AttributeValue related admin apies views............................ start
class AdminAttributeListAllAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttributeSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            queryset = Attribute.objects.filter(is_active=True).order_by('-created_at')
            return queryset
        else:
            raise ValidationError({"msg": 'You can not see attribute data, because you are not an Admin or a Staff!'})


class AdminAttributeListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AttributeSerializer

    def get_queryset(self):
        request = self.request
        search = request.GET.get('search')
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = Attribute.objects.filter(is_active=True).order_by('-created_at')
            if search:
                queryset = queryset.filter(Q(title__icontains=search))
            return queryset
        else:
            raise ValidationError({"msg": 'You can not see attribute data, because you are not an Admin or a Staff!'})


class AdminAttributeDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AttributeSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            attribute_obj = Attribute.objects.filter(id=id).exists()
            if attribute_obj:
                Attribute.objects.filter(id=id).update(is_active=False)
                attribute_values_obj_exist = AttributeValues.objects.filter(attribute=id).exists()
                if attribute_values_obj_exist:
                    attribute_values_objs = AttributeValues.objects.filter(attribute=id)
                    for attribute_values_obj in attribute_values_objs:
                        AttributeValues.objects.filter(attribute=id).update(is_active=False)

                queryset = Attribute.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Attribute Does not exist!'}
                )
        else:
            raise ValidationError({"msg": 'You can not delete attribute, because you are not an Admin or a Staff!'})


class AdminAddNewAttributeAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttributeSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminAddNewAttributeAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create attribute, because you are not an Admin or a Staff!'})


class AdminUpdateAttributeAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttributeSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            query = Attribute.objects.filter(id=id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Attribute does not found!'})
        else:
            raise ValidationError({"msg": 'You can not update attribute, because you are not an Admin or a Staff!'})


class AdminAddNewAttributeValueAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttributeValuesSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminAddNewAttributeValueAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create attribute value, because you are not an Admin or a Staff!'})


class AdminUpdateAttributeValueAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttributeValuesSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            query = AttributeValues.objects.filter(id=id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Attribute Value does not found!'})
        else:
            raise ValidationError({"msg": 'You can not update attribute value, because you are not an Admin or a Staff!'})


class AdminDeleteAttributeValueAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttributeValuesSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            attribute_value_obj = AttributeValues.objects.filter(id=id).exists()
            if attribute_value_obj:
                AttributeValues.objects.filter(id=id).update(is_active=False)
                queryset = AttributeValues.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Attribute Value does not found!'})
        else:
            raise ValidationError({"msg": 'You can not update attribute value, because you are not an Admin or a Staff!'})


class AdminFilterAttributeListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminFilterAttributeSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = FilterAttributes.objects.all().order_by('-created_at')
            return queryset
        else:
            raise ValidationError({"msg": 'You can not see filter attribute data, because you are not an Admin or a Staff!'})


class AdminAddNewFilterAttributeAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminFilterAttributeSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminAddNewFilterAttributeAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create filter attribute value, because you are not an Admin or a Staff!'})


class AdminUpdateFilterAttributeAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminFilterAttributeSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            query = FilterAttributes.objects.filter(id=id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Filter Attribute does not found!'})
        else:
            raise ValidationError({"msg": 'You can not update filter attribute, because you are not an Admin or a Staff!'})


class AdminFilterAttributesAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FilteringAttributesSerializer
    def get_queryset(self):
        id = self.kwargs['id']
        type = self.kwargs['type']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = FilterAttributes.objects.all().order_by('-created_at')
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
            raise ValidationError({"msg": 'You can not see filtering attributes, because you are not an Admin or a Staff!'})
# Attribute, AttributeValue related admin apies views............................ end


# Order related admin apies views............................ start
class AdminOrderList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminOrderListSerializer
    pagination_class = OrderCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            request = self.request
            type = request.GET.get('type')
            order_status = request.GET.get('order_status')

            if self.request.user.is_seller == True:
                queryset = Order.objects.filter(is_active=True, order_item_order__product__seller=Seller.objects.get(seller_user=self.request.user.id)).order_by('-created_at')
            else:
                queryset = Order.objects.filter(is_active=True).order_by('-created_at')

            if type == 'in_house_order':
                queryset = queryset.filter(in_house_order=True)
            if type == 'seller_order':
                queryset = queryset.filter(is_active=True, vendor__isnull=False).order_by('vendor')
            if type == 'pick_up_point_order':
                queryset = queryset.filter(is_active=True, delivery_address__isnull=True)

            if order_status == 'PENDING':
                queryset = queryset.filter(order_status = 'PENDING', is_active=True)
            if order_status == 'CONFIRMED':
                queryset = queryset.filter(order_status = 'CONFIRMED', is_active=True)
            if order_status == 'PICKED-UP':
                queryset = queryset.filter(order_status = 'PICKED-UP', is_active=True)
            if order_status == 'DELIVERED':
                queryset = queryset.filter(order_status = 'DELIVERED', is_active=True)
            if order_status == 'RETURN':
                queryset = queryset.filter(order_status = 'RETURN', is_active=True)
            if order_status == 'CANCEL':
                queryset = queryset.filter(order_status = 'CANCEL', is_active=True)

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no order till now "})
        else:
            raise ValidationError(
                {"msg": 'You can not see order list, because you are not an Admin or a Staff!'})


class AdminSellerOrderList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminOrderListSerializer
    pagination_class = OrderCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            request = self.request
            type = request.GET.get('type')
            order_status = request.GET.get('order_status')
            seller = request.GET.get('seller')

            if seller:
                queryset = Order.objects.filter(is_active=True, order_item_order__product__seller=seller).order_by('-created_at')
            else:
                queryset = Order.objects.filter(is_active=True).order_by('-created_at')

            if type == 'in_house_order':
                queryset = queryset.filter(in_house_order=True)
            if type == 'seller_order':
                queryset = queryset.filter(is_active=True, vendor__isnull=False).order_by('vendor')
            if type == 'pick_up_point_order':
                queryset = queryset.filter(is_active=True, delivery_address__isnull=True).order_by('vendor')

            if order_status == 'PENDING':
                queryset = queryset.filter(order_status = 'PENDING', is_active=True)
            if order_status == 'CONFIRMED':
                queryset = queryset.filter(order_status = 'CONFIRMED', is_active=True)
            if order_status == 'PICKED-UP':
                queryset = queryset.filter(order_status = 'PICKED-UP', is_active=True)
            if order_status == 'DELIVERED':
                queryset = queryset.filter(order_status = 'DELIVERED', is_active=True)
            if order_status == 'RETURN':
                queryset = queryset.filter(order_status = 'RETURN', is_active=True)
            if order_status == 'CANCEL':
                queryset = queryset.filter(order_status = 'CANCEL', is_active=True)

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "There is no order till now "})
        else:
            raise ValidationError(
                {"msg": 'You can not see order list, because you are not an Admin or a Staff!'})


class AdminOrderViewAPI(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    # serializer_class = AdminOrderViewSerializer(many=True, context={"request": request})
    serializer_class = AdminOrderViewSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_object(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            query = Order.objects.get(id=id)
            if query:
                return query
            else:
                raise ValidationError({"msg": "No Order available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see order, because you are not an Admin or a Staff or a vendor!'})


class SallerOrderListSearchAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = OrderCustomPagination
    serializer_class = AdminOrderListSerializer


    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            request = self.request
            order_id = request.GET.get('order_id')
            order_status = request.GET.get('order_status')
            date = request.GET.get('order_date')
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            seller = request.GET.get('seller')

            if seller:
                queryset = Order.objects.filter(is_active=True, order_item_order__product__seller=seller).order_by('-created_at')
                print('seller')
                print(seller)
            else:
                queryset = Order.objects.filter(is_active=True).order_by('-created_at')

            if order_id:
                queryset = queryset.filter(Q(order_id__icontains=order_id))
            if order_status:
                queryset = queryset.filter(order_status__icontains=order_status)
            if date:
                queryset = queryset.filter(Q(order_date__icontains=date))
            if start_date and end_date:
                queryset = queryset.filter(
                    Q(order_date__gte=start_date) & Q(order_date__lte=end_date)
                )

            return queryset
        else:
            raise ValidationError(
                {"msg": 'You can not see Order list, because you are not an Admin or a Staff!'})


class OrderListSearchAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = OrderCustomPagination
    serializer_class = AdminOrderListSerializer


    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            request = self.request
            order_id = request.GET.get('order_id')
            order_status = request.GET.get('order_status')
            date = request.GET.get('order_date')
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')

            if self.request.user.is_seller == True:
                queryset = Order.objects.filter(is_active=True, order_item_order__product__seller=Seller.objects.get(seller_user=self.request.user.id)).order_by('-created_at')
            else:
                queryset = Order.objects.filter(is_active=True).order_by('-created_at')

            if order_id:
                queryset = queryset.filter(Q(order_id__icontains=order_id))
            if order_status:
                queryset = queryset.filter(order_status__icontains=order_status)
            if date:
                queryset = queryset.filter(Q(order_date__icontains=date))
            if start_date and end_date:
                queryset = queryset.filter(
                    Q(order_date__gte=start_date) & Q(order_date__lte=end_date)
                )

            return queryset
        else:
            raise ValidationError(
                {"msg": 'You can not see Order list, because you are not an Admin or a Staff!'})


class AdminOrderUpdateAPI(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminOrderUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"


    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = Order.objects.filter(id=id)
            order_obj_exist = Order.objects.filter(id=id).exists()
            if order_obj_exist:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Order Does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not see order, because you are not an Admin or a Staff!'})


    def put(self, request, *args, **kwargs):
        try:
            try:
                order_status = request.data["order_status"]
            except:
                order_status = None
            try:
                payment_status = request.data["payment_status"]
            except:
                payment_status = None

            order_id = self.kwargs['id']

            try:
                order_obj = Order.objects.filter(id=order_id)
            except:
                order_obj = None

            if order_obj:
                if order_status:
                    order_obj.update(order_status=order_status)
                    # update inventory
                    if order_status == 'RETURN':
                        order_obj_get = Order.objects.get(id=order_id)
                        order_items_obj_exist = OrderItem.objects.filter(order=order_obj_get.id).exists()
                        if order_items_obj_exist:
                            order_items = OrderItem.objects.filter(order=order_obj_get.id)
                            for order_item in order_items:
                                product = order_item.product
                                quantity = order_item.quantity
                                product_filter_obj = Product.objects.filter(id=product.id)
                                latest_inventory_obj = Inventory.objects.filter(product=product).latest('created_at')
                                latest_current_quantity = latest_inventory_obj.current_quantity
                                latest_initial_quantity = latest_inventory_obj.initial_quantity
                                new_current_quantity =  latest_current_quantity + quantity
                                Inventory.objects.create(product=product, initial_quantity=latest_initial_quantity, current_quantity=new_current_quantity)
                                product_filter_obj.update(quantity = new_current_quantity)

                if payment_status:
                    order_obj.update(payment_status=payment_status)

                return Response(data={"order_id": order_obj[0].id}, status=status.HTTP_202_ACCEPTED)
            else:
                raise ValidationError({"msg": 'Order update failed!'})
        except KeyError:
            raise ValidationError({"msg": 'Order update failed. contact with developer!'})
# Order related admin apies views............................ end


# Customer related admin apies views............................ start
class AdminCustomerListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminCustomerListSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            queryset = User.objects.filter(is_customer=True, is_active=True)
            return queryset
        else:
            raise ValidationError({"msg": 'You can not see customer list data, because you are not an Admin or a Staff or a vendor!'})


class AdminCustomerListAllAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCustomerListSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            queryset = User.objects.filter(is_customer=True, is_active=True)
            return queryset
        else:
            raise ValidationError({"msg": 'You can not see customer list data, because you are not an Admin or a Staff or a vendor!'})


class AdminCustomerDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminCustomerListSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            user_obj = User.objects.filter(id=id, is_customer=True, is_active=True).exists()
            if user_obj:
                User.objects.filter(id=id, is_customer=True, is_active=True).update(is_active=False)

                queryset = User.objects.filter(is_customer=True, is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'User Does not exist!'}
                )
        else:
            raise ValidationError({"msg": 'You can not delete User, because you are not an Admin or a Staff!'})
# Customer related admin apies views............................ end


# Ticket related admin apies views............................ start
class AdminTicketListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminTicketListSerializer

    def get_queryset(self):
        request = self.request
        status = request.GET.get('status')
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = Ticket.objects.filter(is_active=True).order_by('-created_at')
            if status:
                queryset = queryset.filter(Q(status=status))
            return queryset
        else:
            raise ValidationError({"msg": 'You can not see ticket list data, because you are not an Admin or a Staff!'})


class AdminTicketDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            ticket_id = self.kwargs['id']
            ticket_details_data = Ticket.objects.filter(id =ticket_id)
            serializer = AdminTicketDataSerializer(ticket_details_data, many=True)
            return Response(serializer.data)
        else:
            raise ValidationError({"msg": 'You can not see ticket details data, because you are not an Admin or a Staff!'})


class AdminTicketStatusUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketStatusSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            ticket_id = self.kwargs['id']
            query = Ticket.objects.filter(id =ticket_id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Ticket does not found!'})
        else:
            raise ValidationError({"msg": 'You can not update ticket status, because you are not an Admin or a Staff!'})


class AdminTicketDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminTicketListSerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            ticket_obj_exist = Ticket.objects.filter(id=id).exists()
            if ticket_obj_exist:
                Ticket.objects.filter(id=id).update(is_active=False)

                queryset = Ticket.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Ticket Does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not delete Ticket, because you are not an Admin or a Staff!'})


class AdminTicketReplyCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminTicketConversationSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminTicketReplyCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create ticket reply, because you are not an Admin or a Staff!'})

# Ticket related admin apies views............................ end


class AdminDashboardDataAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            # total customer
            if User.objects.filter(is_customer=True).exists():
                customer_count = User.objects.filter(is_customer=True).count()
            else:
                customer_count = 0

            # total order
            if Order.objects.filter(is_active=True).exists():
                if self.request.user.is_seller == True:
                    order_count = Order.objects.filter(is_active=True, order_item_order__product__seller=Seller.objects.get(seller_user=self.request.user.id)).count()
                else:
                    order_count = Order.objects.filter(is_active=True).count()
            else:
                order_count = 0

            # total category
            if Category.objects.filter(is_active=True).exists():
                category_count = Category.objects.filter(is_active=True).count()
            else:
                category_count = 0

            # total Brand
            if Brand.objects.filter(is_active=True).exists():
                brand_count = Brand.objects.filter(is_active=True).count()
            else:
                brand_count = 0

            # total published Product
            if Product.objects.filter(status = 'PUBLISH', is_active=True).exists():
                if self.request.user.is_seller == True:
                    published_product_count = Product.objects.filter(status = 'PUBLISH', is_active=True, seller=Seller.objects.get(seller_user=self.request.user.id)).count()
                else:
                    published_product_count = Product.objects.filter(status = 'PUBLISH', is_active=True).count()
            else:
                published_product_count = 0

            # total seller Product
            if Product.objects.filter(~Q(in_house_product = True), Q(is_active=True)).exists():
                if self.request.user.is_seller == True:
                    seller_product_count = Product.objects.filter(~Q(in_house_product = True), Q(is_active=True), Q(seller=Seller.objects.get(seller_user=self.request.user.id))).count()
                else:
                    seller_product_count = Product.objects.filter(~Q(in_house_product = True), Q(is_active=True)).count()
            else:
                seller_product_count = 0

            # total admin Product
            if Product.objects.filter(in_house_product = True, is_active=True).exists():
                admin_product_count = Product.objects.filter(in_house_product = True, is_active=True).count()
            else:
                admin_product_count = 0

            # total sellers
            if Seller.objects.filter(is_active=True).exists():
                seller_count = Seller.objects.filter(is_active=True).count()
            else:
                seller_count = 0

            # total approved sellers
            if Seller.objects.filter(status='APPROVED', is_active=True).exists():
                approved_seller_count = Seller.objects.filter(status='APPROVED', is_active=True).count()
            else:
                approved_seller_count = 0

            # total pending sellers
            if Seller.objects.filter(status='PENDING', is_active=True).exists():
                pending_seller_count = Seller.objects.filter(status='PENDING', is_active=True).count()
            else:
                pending_seller_count = 0

            # Category wise product sale
            categories = Category.objects.filter(is_active=True)
            category_wise_product_sale = CategoryWiseProductSaleSerializer(categories, many=True, context={"request": request})

            # Category wise product stock
            category_wise_product_stock = CategoryWiseProductStockSerializer(categories, many=True, context={"request": request})

            # Top products
            if Product.objects.filter(status='PUBLISH', is_active=True).exists():
                products = Product.objects.filter(status='PUBLISH', is_active=True).order_by('-sell_count')
                products_data = ProductListBySerializer(products, many=True, context={"request": request})


            return Response({
                "customer_count": customer_count,
                "order_count": order_count,
                "category_count": category_count,
                "brand_count": brand_count,
                "published_product_count": published_product_count,
                "seller_product_count": seller_product_count,
                "admin_product_count": admin_product_count,
                "seller_count": seller_count,
                "approved_seller_count": approved_seller_count,
                "pending_seller_count": pending_seller_count,
                "category_wise_product_sale": category_wise_product_sale.data,
                "category_wise_product_stock": category_wise_product_stock.data,
                "top_products": products_data.data
            })

        else:
            raise ValidationError({"msg": 'You can not see dashboard data, because you are not an Admin or a Staff!'})


# brand related admin apies views............................ start
class AdminBrandCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorBrandSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminBrandCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create brand, because you are not an Admin or a Staff!'})


class AdminBrandUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorBrandSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            query = Brand.objects.filter(id=id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Brand does not found!'})
        else:
            raise ValidationError({"msg": 'You can not update brand, because you are not an Admin or a Staff!'})


class AdminBrandDeleteAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = VendorBrandSerializer
    queryset =  Brand.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        brand_id = self.kwargs['id']
        brand_obj = Brand.objects.filter(id=brand_id).exists()
        if brand_obj:
            brand_obj = Brand.objects.filter(id=brand_id)
            brand_obj.update(is_active=False)

            queryset = Brand.objects.filter(is_active=True).order_by('-created_at')
            return queryset
        else:
            raise ValidationError(
                {"msg": 'Brand Does not exist!'}
            )
# brand related admin apies views............................ end


# Warranty admin apies views............................ start
class AdminWarrantyListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminWarrantyListSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = Warranty.objects.filter(is_active=True)
            return queryset
        else:
            raise ValidationError({"msg": 'You can not see ticket list data, because you are not an Admin or a Staff!'})
# Warranty admin apies views............................ end


# shipping related admin apies views............................ start
class AdminShippingCountryAddAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminShippingCountrySerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminShippingCountryAddAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create Shipping Country, because you are not an Admin or a Staff!'})


class AdminShippingCountryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminShippingCountrySerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        request = self.request
        search = request.GET.get('search')
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = ShippingCountry.objects.filter(is_active=True).order_by('-created_at')

            if search:
                queryset = queryset.filter(Q(title__icontains=search))

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "Shipping Country doesn't exist! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see Shipping Country list, because you are not an Admin or a Staff!'})


class AdminShippingCountryListAllAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminShippingCountrySerializer

    def get_queryset(self):
        request = self.request
        search = request.GET.get('search')
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = ShippingCountry.objects.filter(is_active=True).order_by('-created_at')

            if search:
                queryset = queryset.filter(Q(title__icontains=search))

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "Shipping Country doesn't exist! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see Shipping Country list, because you are not an Admin or a Staff!'})


class AdminShippingCountryListFilterAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminShippingCountrySerializer

    def get_queryset(self):
        request = self.request
        search = request.GET.get('search')
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = ShippingCountry.objects.filter(is_active= True).order_by('-created_at')
            if search:
                queryset = queryset.filter(Q(title__icontains=search) | Q(code__icontains=search))

            return queryset
        else:
            raise ValidationError({"msg": 'You can not search Shipping Country data, because you are not an Admin or a Staff!'})


class AdminShippingCountryUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminShippingCountrySerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            query = ShippingCountry.objects.filter(id=id, is_active=True)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Shipping Country does not found!'})
        else:
            raise ValidationError({"msg": 'You can not update Shipping Country, because you are not an Admin or a Staff!'})


class AdminShippingCountryDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminShippingCountrySerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            shipping_country_obj = ShippingCountry.objects.filter(id=id).exists()
            if shipping_country_obj:
                shipping_country_obj = ShippingCountry.objects.filter(id=id).update(is_active=False)
                queryset = ShippingCountry.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Shipping Country Info Does not exist!'}
                )
        else:
            raise ValidationError({"msg": 'You can not delete Shipping Country, because you are not an Admin or a Staff!'})


class AdminShippingCityListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminShippingCitySerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        request = self.request
        search = request.GET.get('search')
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = ShippingCity.objects.filter(is_active=True).order_by('-created_at')

            if search:
                queryset = queryset.filter(Q(title__icontains=search))

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "Shipping City doesn't exist! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see Shipping City list, because you are not an Admin or a Staff!'})


class AdminShippingCityListAllAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminShippingCitySerializer

    def get_queryset(self):
        request = self.request
        search = request.GET.get('search')
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = ShippingCity.objects.filter(is_active=True).order_by('-created_at')

            if search:
                queryset = queryset.filter(Q(title__icontains=search))

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "Shipping City doesn't exist! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see Shipping City list, because you are not an Admin or a Staff!'})


class AdminShippingCityAddAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminShippingCitySerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminShippingCityAddAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create Shipping City, because you are not an Admin or a Staff!'})


class AdminShippingCityUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminShippingCitySerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            query = ShippingCity.objects.filter(id=id, is_active=True)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Shipping City does not found!'})
        else:
            raise ValidationError({"msg": 'You can not update Shipping City, because you are not an Admin or a Staff!'})


class AdminShippingCityDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminShippingCitySerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            shipping_country_obj = ShippingCity.objects.filter(id=id).exists()
            if shipping_country_obj:
                shipping_country_obj = ShippingCity.objects.filter(id=id).update(is_active=False)
                queryset = ShippingCity.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Shipping City Info Does not exist!'}
                )
        else:
            raise ValidationError({"msg": 'You can not delete Shipping City, because you are not an Admin or a Staff!'})


class AdminShippingStateListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminShippingStateSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        request = self.request
        search = request.GET.get('search')
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = ShippingState.objects.filter(is_active=True).order_by('-created_at')

            if search:
                queryset = queryset.filter(Q(title__icontains=search))

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "Shipping State doesn't exist! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see Shipping State list, because you are not an Admin or a Staff!'})


class AdminShippingStateListAllAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminShippingStateSerializer

    def get_queryset(self):
        request = self.request
        search = request.GET.get('search')
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = ShippingState.objects.filter(is_active=True).order_by('-created_at')

            if search:
                queryset = queryset.filter(Q(title__icontains=search))

            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "Shipping State doesn't exist! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see Shipping State list, because you are not an Admin or a Staff!'})


class AdminShippingStateAddAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminShippingStateSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminShippingStateAddAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create Shipping State, because you are not an Admin or a Staff!'})


class AdminShippingStateUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminShippingStateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            query = ShippingState.objects.filter(id=id, is_active=True)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Shipping State does not found!'})
        else:
            raise ValidationError({"msg": 'You can not update Shipping State, because you are not an Admin or a Staff!'})


class AdminShippingStateDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminShippingStateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            shipping_state_obj = ShippingState.objects.filter(id=id).exists()
            if shipping_state_obj:
                shipping_state_obj = ShippingState.objects.filter(id=id).update(is_active=False)
                queryset = ShippingState.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Shipping State Info Does not exist!'}
                )
        else:
            raise ValidationError({"msg": 'You can not delete Shipping State, because you are not an Admin or a Staff!'})


class AdminShippingClassListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminShippingClassSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = ShippingClass.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "Shipping Country doesn't exist! " })
        else:
            raise ValidationError({"msg": 'You can not see ticket list data, because you are not an Admin or a Staff!'})


class AdminShippingClassListAllAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminShippingClassSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = ShippingClass.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "Shipping Country doesn't exist! " })
        else:
            raise ValidationError({"msg": 'You can not see ticket list data, because you are not an Admin or a Staff!'})


class AdminShippingClassAddAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminShippingClassSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminShippingClassAddAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create Shipping Class, because you are not an Admin or a Staff!'})


class AdminShippingClassUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminShippingClassSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            query = ShippingClass.objects.filter(id=id, is_active=True)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Shipping Class does not found!'})
        else:
            raise ValidationError({"msg": 'You can not update Shipping Class, because you are not an Admin or a Staff!'})


class AdminShippingClassDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminShippingClassSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            shipping_class_obj = ShippingClass.objects.filter(id=id).exists()
            if shipping_class_obj:
                shipping_class_obj = ShippingClass.objects.filter(id=id).update(is_active=False)
                queryset = ShippingClass.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Shipping Class Info Does not exist!'}
                )
        else:
            raise ValidationError({"msg": 'You can not delete Shipping Class, because you are not an Admin or a Staff!'})
# shipping related admin apies views............................ end

class AdminSpecificationTitleListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminSpecificationTitleSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = SpecificationTitle.objects.filter(is_active=True)
            return queryset
        else:
            raise ValidationError({"msg": 'You can not see ticket list data, because you are not an Admin or a Staff!'})


class AdminSpecificationCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSpecificationTitleSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminSpecificationCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create Specification title, because you are not an Admin or a Staff!'})


class AdminSpecificationDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminSpecificationTitleSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            specification_title_obj = SpecificationTitle.objects.filter(id=id).exists()
            if specification_title_obj:
                SpecificationTitle.objects.filter(id=id).update(is_active=False)
                queryset = SpecificationTitle.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Specification Title data Does not exist!'}
                )
        else:
            raise ValidationError({"msg": 'You can not delete Specification Title data, because you are not an Admin or a Staff!'})

class AdminSubscribersListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminSubscribersListSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = Subscription.objects.filter(is_active=True).order_by('-created_at')
            return queryset
        else:
            raise ValidationError({"msg": 'You can not see Subscribers list data, because you are not an Admin or a Staff!'})


class AdminSubscribersListAllAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSubscribersListSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = Subscription.objects.filter(is_active=True).order_by('-created_at')
            return queryset
        else:
            raise ValidationError({"msg": 'You can not see Subscribers list data, because you are not an Admin or a Staff!'})


class AdminSubscriberDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminSubscribersListSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            subscription_obj = Subscription.objects.filter(id=id).exists()
            if subscription_obj:
                subscription_obj = Subscription.objects.filter(id=id)
                subscription_obj.update(is_active=False)

                queryset = Subscription.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Subscriber Does not exist!'}
                )
        else:
            raise ValidationError({"msg": 'You can not delete subscriber, because you are not an Admin or a Staff!'})


# Corporate Deal related admin apies views............................ start
class AdminCorporateDealListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminCorporateDealSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = CorporateDeal.objects.filter(is_active=True).order_by('-created_at')
            return queryset
        else:
            raise ValidationError({"msg": 'You can not see Corporate list data, because you are not an Admin or a Staff!'})


class AdminCorporateDealDetailsAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCorporateDealSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_object(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            query = CorporateDeal.objects.get(id=id)
            if query:
                return query
            else:
                raise ValidationError({"msg": "No Corporate Deals data available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see Corporate Deals, because you are not an Admin or a Staff!'})


class AdminCorporateDealDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminCorporateDealSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            corporate_deal_obj = CorporateDeal.objects.filter(id=id).exists()
            if corporate_deal_obj:
                corporate_deal_obj = CorporateDeal.objects.filter(id=id)
                corporate_deal_obj.update(is_active=False)

                queryset = CorporateDeal.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Corporate Deal Does not exist!'}
                )
        else:
            raise ValidationError({"msg": 'You can not delete corporate deal, because you are not an Admin or a Staff!'})
# Corporate Deal related admin apies views............................ end


# Request Quote related admin apies views............................ end
class AdminRequestQuoteListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminRequestQuoteSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = RequestQuote.objects.filter(is_active=True).order_by('-created_at')
            return queryset
        else:
            raise ValidationError({"msg": 'You can not see Request Quote list data, because you are not an Admin or a Staff!'})


class AdminRequestQuoteDetailsAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminRequestQuoteSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_object(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            query = RequestQuote.objects.get(id=id)
            if query:
                return query
            else:
                raise ValidationError({"msg": "No Request Quote Deals data available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see Request Quote Deals, because you are not an Admin or a Staff!'})


class AdminRequestQuoteDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminRequestQuoteSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            request_quote_obj = RequestQuote.objects.filter(id=id).exists()
            if request_quote_obj:
                RequestQuote.objects.filter(id=id).update(is_active=False)

                queryset = RequestQuote.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Request Quote Does not exist!'}
                )
        else:
            raise ValidationError({"msg": 'You can not delete Request Quote, because you are not an Admin or a Staff!'})
# Request Quote related admin apies views............................ end


# Contact Us related admin apies views............................ end
class AdminContactUsListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminContactUsSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = ContactUs.objects.filter(is_active=True).order_by('-created_at')
            return queryset
        else:
            raise ValidationError({"msg": 'You can not see Contact Us list data, because you are not an Admin or a Staff!'})


class AdminContactUsDetailsAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminContactUsSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_object(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            query = ContactUs.objects.get(id=id)
            if query:
                return query
            else:
                raise ValidationError({"msg": "No Contact Us data available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see Contact Us, because you are not an Admin or a Staff!'})


class AdminContactUsDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminContactUsSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            corporate_deal_obj = ContactUs.objects.filter(id=id).exists()
            if corporate_deal_obj:
                ContactUs.objects.filter(id=id).update(is_active=False)

                queryset = ContactUs.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Request Quote Does not exist!'}
                )
        else:
            raise ValidationError({"msg": 'You can not delete Request Quote, because you are not an Admin or a Staff!'})
# Contact Us related admin apies views............................ end


class AdminOrderDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminOrderListSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            order_obj = Order.objects.filter(id=id).exists()
            if order_obj:
                Order.objects.filter(id=id).update(is_active=False)
                queryset = Order.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Orders Does not exist!'}
                )
        else:
            raise ValidationError({"msg": 'You can not delete orders, because you are not an Admin or a Staff!'})


# Coupon related admin apies views............................ start
class AdminCouponCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCouponSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminCouponCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create coupon, because you are not an Admin or a Staff!'})


class AdminCouponListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCouponSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = Coupon.objects.filter(is_active=True).order_by('-created_at')
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Vat types does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not view coupon list, because you are not an Admin or a Staff!'})


class AdminCouponUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCouponSerializer
    queryset = Coupon.objects.filter(is_active=True)
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def put(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminCouponUpdateAPIView, self).put(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not update coupon, because you are not an Admin or a Staff!'})


class AdminCouponDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminCouponSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            coupon_obj = Coupon.objects.filter(id=id).exists()
            if coupon_obj:
                Coupon.objects.filter(id=id).update(is_active=False)
                queryset = Coupon.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Coupon data Does not exist!'}
                )
        else:
            raise ValidationError({"msg": 'You can not delete coupon data, because you are not an Admin or a Staff!'})
# Coupon related admin apies views............................ end


# Offers related admin apies views............................ start
class AdminOfferCategoryListAPIView(ListAPIView):
    serializer_class = AdminOfferCategoryListSerializer
    permission_classes = [IsAuthenticated]
    queryset = OfferCategory.objects.all()

class AdminOffersListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminOfferSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            today_date = datetime.today()
            queryset = Offer.objects.filter(end_date__gte = today_date, is_active=True).order_by('-created_at')
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Offers does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not view offers list, because you are not an Admin or a Staff!'})


class AdminOffersDetailsAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminOfferDetailsSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_object(self):
        offer_id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            try:
                query = Offer.objects.get(id=offer_id)
                return query
            except:
                raise ValidationError({"details": "Offer doesn't exist!"})
        else:
            raise ValidationError(
                {"msg": 'You can not see Offer details, because you are not an Admin or a Staff!'})


class AdminOffersCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminOfferSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminOffersCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create Offers, because you are not an Admin or a Staff!'})


class AdminOffersUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminOfferSerializer
    queryset = Offer.objects.filter(is_active=True)
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def put(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminOffersUpdateAPIView, self).put(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not update Offer, because you are not an Admin or a Staff!'})


class AdminOffersDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductCustomPagination
    serializer_class = AdminOfferSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            offer_obj = Offer.objects.filter(id=id).exists()
            if offer_obj:
                Offer.objects.filter(id=id).update(is_active=False)
                queryset = Offer.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Offer data Does not exist!'}
                )
        else:
            raise ValidationError({"msg": 'You can not delete Offer data, because you are not an Admin or a Staff!'})
# Offers related admin apies views............................ end


# POS related admin apies views............................ start

class AdminPosCustomerCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = User
    serializer_class = AdminPosCustomerCreateSerializer

    def perform_create(self, serializer):
        is_customer = self.request.data.get('is_customer', True)
        serializer.save(is_customer=is_customer)

    def post(self, request, *args, **kwargs):

        return super(AdminPosCustomerCreateAPIView, self).post(request, *args, **kwargs)


class AdminPosCustomerProfileAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerProfileSerializer
    queryset = User.objects.filter(is_customer=True)


class AdminPosProductListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminPosProductListSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            request = self.request
            query = request.GET.get('search')
            category = request.GET.get('category_id')
            brand = request.GET.get('brand')

            queryset = Product.objects.filter(status='PUBLISH').order_by('-created_at')

            if query:
                queryset = queryset.filter(Q(title__icontains=query))

            if category:
                queryset = queryset.filter(category__id=category)

            if brand:
                if category:
                    queryset = queryset.filter(brand_id=brand)

            return queryset
            # else:
            #     raise ValidationError({"msg": "Product doesn't exist! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see product list, because you are not an Admin or a Staff!'})


class AdminPosSearchAPI(ListAPIView):
    pagination_class = ProductCustomPagination
    serializer_class = AdminPosProductListSerializer

    def get_queryset(self):
        request = self.request
        query = request.GET.get('search')
        category = request.GET.get('category_id')
        brand = request.GET.get('brand')

        queryset = Product.objects.filter(status='PUBLISH').order_by('-created_at')

        if query:
            queryset = queryset.filter(Q(title__icontains=query))

        if category:
            queryset = queryset.filter(category__id=category)

        if brand:
            if category:
                queryset = queryset.filter(brand_id=brand)

        return queryset


class AdminPosOrderAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = AdminPosOrderSerializer

    def perform_create(self, serializer):
        in_house_order = self.request.data.get('in_house_order', True)
        serializer.save(in_house_order=in_house_order)

    def post(self, request, *args, **kwargs):
        return super(AdminPosOrderAPIView, self).post(request, *args, **kwargs)
# POS related admin apies views............................ end


class AdminDiscountListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = DiscountTypeSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = DiscountTypes.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No discount available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see discount list, because you are not an Admin or a Staff!'})


class AdminTagListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TagsSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = Tags.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No tag available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see tag list, because you are not an Admin or a Staff!'})


# Video Provider related admin apies views............................ start
class AdminVideoProviderListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductVideoProviderSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = ProductVideoProvider.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Video provider data does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not view video provider list, because you are not an Admin or a Staff!'})


class AdminVideoProviderCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductVideoProviderSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminVideoProviderCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create video provider, because you are not an Admin or a Staff!'})


class AdminVideoProviderUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductVideoProviderSerializer
    queryset = ProductVideoProvider.objects.filter(is_active=True)
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def put(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminVideoProviderUpdateAPIView, self).put(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not update video provider, because you are not an Admin or a Staff!'})


class AdminVideoProviderDeleteAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductVideoProviderSerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            product_obj_exist = ProductVideoProvider.objects.filter(id=id).exists()
            if product_obj_exist:
                product_obj = ProductVideoProvider.objects.filter(id=id).update(is_active=False)

                queryset = ProductVideoProvider.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Video Provider Data Does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not delete Video Provider data, because you are not an Admin or a Staff!'})
# Video Provider related admin apies views............................ end


# Vat Type related admin apies views............................ start
class AdminVatTypeListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VatTypeSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = VatType.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Vat types does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not view Vat types list, because you are not an Admin or a Staff!'})


class AdminVatTypeAddAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VatTypeSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminVatTypeAddAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create vat type, because you are not an Admin or a Staff!'})


class AdminVatTypeUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VatTypeSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            query = VatType.objects.filter(id=id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'VatType does not found!'})
        else:
            raise ValidationError({"msg": 'You can not update VatType, because you are not an Admin or a Staff!'})


class AdminVatTypeDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VatTypeSerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            vat_type_obj_exist = VatType.objects.filter(id=id).exists()
            if vat_type_obj_exist:
                VatType.objects.filter(id=id).update(is_active=False)

                queryset = VatType.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'VatType Does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not delete VatType, because you are not an Admin or a Staff!'})
# Vat Type related admin apies views............................ end


# product create related apies................................. start
class AdminCategoryAllListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCategoryListSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            queryset = Category.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No category available!" })
        else:
            raise ValidationError(
                {"msg": 'You can not see category list, because you are not an Admin or a Staff!'})


class AdminSubCategoryListAllAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSubCategoryListSerializer
    lookup_field = 'cid'
    lookup_url_kwarg = "cid"

    def get_queryset(self):
        cid = self.kwargs['cid']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            queryset = SubCategory.objects.filter(category=cid, is_active=True).order_by('-created_at')
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No sub category available!" })
        else:
            raise ValidationError(
                {"msg": 'You can not see sub category list, because you are not an Admin or a Staff!'})


class AdminSubSubCategoryAllListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSubSubCategoryListSerializer
    lookup_field = 'sid'
    lookup_url_kwarg = "sid"

    def get_queryset(self):
        sid = self.kwargs['sid']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            if sid:
                queryset = SubSubCategory.objects.filter(
                    sub_category=sid, is_active=True).order_by('-created_at')
            else:
                queryset = SubSubCategory.objects.filter(
                    is_active=True).order_by('-created_at')
            return queryset
        else:
            raise ValidationError(
                {"msg": 'You can not see sub sub category list, because you are not an Admin or a Staff!'})


class AdminBrandListAllAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorBrandSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            queryset = Brand.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No brand available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see brand list, because you are not an Admin or a Staff!'})


class AdminUnitListAllAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorUnitSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            queryset = Units.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No unit available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see unit list, because you are not an Admin or a Staff!'})


class AdminSellerListAllAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            queryset = Seller.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No seller available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see seller list, because you are not an Admin or a Staff!'})


class AdminVatTypeListAllAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VatTypeSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            queryset = VatType.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Vat types does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not view Vat types list, because you are not an Admin or a Staff!'})


class AdminVideoProviderListAllAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductVideoProviderSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            queryset = ProductVideoProvider.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Video provider data does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not view video provider list, because you are not an Admin or a Staff!'})


class AdminDiscountTypeListAllAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DiscountTypeSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            queryset = DiscountTypes.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError({"msg": "No discount available! " })
        else:
            raise ValidationError(
                {"msg": 'You can not see discount list, because you are not an Admin or a Staff!'})


class AdminFilterAttributeListAllAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminFilterAttributeSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            request = self.request
            cid = request.GET.get('cid')
            s_cid = request.GET.get('s_cid')
            s_s_cid = request.GET.get('s_s_cid')
            if cid:
                queryset = FilterAttributes.objects.filter(category=cid, is_active=True).order_by('-created_at')
                return queryset
            if s_cid:
                queryset = FilterAttributes.objects.filter(sub_category=s_cid, is_active=True).order_by('-created_at')
                return queryset
            if s_s_cid:
                queryset = FilterAttributes.objects.filter(sub_sub_category=s_s_cid, is_active=True).order_by('-created_at')
                return queryset
            else:
                queryset = FilterAttributes.objects.filter(is_active=True).order_by('-created_at')
                return queryset
        else:
            raise ValidationError({"msg": 'You can not see filter attribute data, because you are not an Admin or a Staff!'})


class AdminFilterAttributeValueListAllAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminFilterAttributeValueSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            request = self.request
            atid = self.kwargs['atid']
            if atid:
                print(atid)
                queryset = AttributeValues.objects.filter(attribute=atid, is_active=True).order_by('-created_at')
                return queryset
            else:
                queryset = AttributeValues.objects.filter(is_active=True).order_by('-created_at')
                return queryset
        else:
            raise ValidationError({"msg": 'You can not see filter attribute values data, because you are not an Admin or a Staff!'})

class AdminFlashDealListAllAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FlashDealInfoSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            queryset = FlashDealInfo.objects.filter(is_active=True)
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Flash Deal does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not view Flash Deal list, because you are not an Admin or a Staff!'})


class AdminOffersListAllAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminOfferSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            today_date = datetime.today()
            queryset = Offer.objects.filter(end_date__gte = today_date, is_active=True).order_by('-created_at')
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Offers does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not view offers list, because you are not an Admin or a Staff!'})


class AdminWarrantyListAllAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminWarrantyListSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            queryset = Warranty.objects.filter(is_active=True)
            return queryset
        else:
            raise ValidationError({"msg": 'You can not see ticket list data, because you are not an Admin or a Staff!'})


class AdminSpecificationTitleListAllAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSpecificationTitleSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            queryset = SpecificationTitle.objects.filter(is_active=True)
            return queryset
        else:
            raise ValidationError({"msg": 'You can not see ticket list data, because you are not an Admin or a Staff!'})
# product create related apies................................. end


#toggle button related apies................................... start
class AdminCategoryToggleUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCategoryToggleSerializer
    queryset = Category.objects.all()


class AdminSubCategoryToggleUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSubCategoryToggleSerializer
    queryset = SubCategory.objects.all()


class AdminProductToggleUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminProductToggleSerializer
    queryset = Product.objects.all()


class AdminBlogToggleUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminBlogToggleSerializer
    queryset = Blog.objects.all()
#toggle button related apies................................... end


class AdminProductReviewToggleAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminProductReviewSerializer
    queryset = ProductReview.objects.all()


class AdminBrandIsGamingToggleAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminBrandIsGamingSerializer
    queryset = Brand.objects.all()


class AdminCategoryIsPcBuilderToggleAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminCategoryIsPcBuilderSerializer
    queryset = Category.objects.all()

#Advertisement related apies................................... start
class AdminAdvertisementListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdvertisementPosterSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = Advertisement.objects.filter(is_active=True)
            return queryset
        else:
            raise ValidationError({"msg": 'You can not see advertisement list data, because you are not an Admin or a Staff!'})


class AdminAdvertisementCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdvertisementPosterSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminAdvertisementCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create Advertisement Poster, because you are not an Admin or a Staff!'})


class AdminAdvertisementUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdvertisementPosterSerializer
    queryset = Advertisement.objects.all()


class AdminAdvertisementDeleteAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdvertisementPosterSerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            advertisement_obj_exist = Advertisement.objects.filter(id=id).exists()
            if advertisement_obj_exist:
                Advertisement.objects.filter(id=id).update(is_active=False)

                queryset = Advertisement.objects.filter(is_active=True).order_by('-created_at')
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Advertisement Does not exist!'})
        else:
            raise ValidationError({"msg": 'You can not delete Advertisement, because you are not an Admin or a Staff!'})

#Advertisement related apies................................... end


#website-configuration related apies................................... start
class AdminWebsiteConfigurationCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WebsiteConfigurationSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AdminWebsiteConfigurationCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create Advertisement Poster, because you are not an Admin or a Staff!'})


class AdminWebsiteConfigurationViewAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WebsiteConfigurationViewSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = HomeSingleRowData.objects.filter(is_active=True).order_by('-created_at')[:1]
            return queryset
        else:
            raise ValidationError({"msg": 'You can not see Website Configuration list data, because you are not an Admin or a Staff!'})


class AdminWebsiteConfigurationUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WebsiteConfigurationUpdateSerializer
    queryset = HomeSingleRowData.objects.all()


class AdminWebsiteGeneralSettingsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GeneralSettingsViewSerializer

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = HomeSingleRowData.objects.filter(is_active=True).order_by('-created_at')[:1]
            return queryset
        else:
            raise ValidationError({"msg": 'You can not see general settings data, because you are not an Admin or a Staff!'})


class AdminWebsiteGeneralSettingsUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GeneralSettingsViewSerializer
    queryset = HomeSingleRowData.objects.all()


class AdminDeleteWebsiteConfigurationImageAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WebsiteConfigurationViewSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def put(self, request, *args, **kwargs):
        try:
            image_id = self.kwargs['id']
            advertisement_obj_exist = Advertisement.objects.filter(id=image_id).exists()
            if advertisement_obj_exist:
                advertisement_obj = Advertisement.objects.filter(id=image_id)
                if advertisement_obj:
                    advertisement_obj.update(is_active=False)
            return Response({"msg": "Successfully deleted!"})
        except KeyError:
            raise ValidationError({"msg": 'Image delete failed!'})


#website-configuration related apies................................... end