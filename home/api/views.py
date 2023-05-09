from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView, UpdateAPIView
from home.models import FAQ, ContactUs, HomeSingleRowData, Advertisement, RequestQuote, AboutUs, TermsAndCondition, OnlineServiceSupport, \
    PaymentMethod, RefundAndReturnPolicy, Shipping, PrivacyPolicy, ServiceCenter
from home.serializers import product_catListSerializer,\
    ContactUsSerializer, FaqSerializer, SingleRowDataSerializer, SliderAdvertisementDataSerializer, AdvertisementDataSerializer, \
    StoreCategoryAPIViewListSerializer, product_sub_catListSerializer, AboutUsSerializer, \
    CorporateDealCreateSerializer, RequestQuoteSerializer, TermsAndConditionSerializer, OnlineServiceSupportSerializer,\
    PaymentMethodSerializer, RefundAndReturnPolicySerializer, ShippingSerializer, PrivacyPolicySerializer, ServiceCenterSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q, Count

from product.models import Product, Category, SubCategory, Brand
from product.serializers import ProductListBySerializer, BrandSerializer, ProductListBySerializerForHomeData
from rest_framework.exceptions import ValidationError
from product.pagination import ProductCustomPagination


class HomeDataAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        # slider images
        slider_images = Advertisement.objects.filter(Q(work_for='SLIDER'), Q(
            is_active=True), Q(is_gaming=False)).order_by('-created_at')[:3]
        slider_images_serializer = AdvertisementDataSerializer(
            slider_images, many=True, context={"request": request})

        # Offer slider images
        offer_slider_images = Advertisement.objects.filter(Q(work_for='OFFER'), Q(
            is_active=True), Q(is_gaming=False)).order_by('-created_at')[:3]
        offer_slider_images_serializer = AdvertisementDataSerializer(
            offer_slider_images, many=True, context={"request": request})

        # categories
        categories = Category.objects.filter(
            is_featured=True, is_active=True).order_by('-ordering_number')
        categories_serializer = product_catListSerializer(
            categories, many=True, context={"request": request})

        # categories
        sub_categories = SubCategory.objects.filter(
            is_featured=True, is_active=True).order_by('-ordering_number')
        sub_categories_serializer = product_sub_catListSerializer(
            sub_categories, many=True, context={"request": request})

        featured_categories_serializer = categories_serializer.data + \
            sub_categories_serializer.data

        # featured
        featured = Product.objects.filter(
            status='PUBLISH', is_featured=True, is_active=True).order_by('-created_at')
        featured_serializer = ProductListBySerializerForHomeData(
            featured, many=True, context={"request": request})

        # most popular
        popular = Product.objects.filter(status="PUBLISH").annotate(
            count=Count('product_review_product')).order_by('-count')
        popular_serializer = ProductListBySerializerForHomeData(
            popular, many=True, context={"request": request})

        # gaming product
        gaming_product = Product.objects.filter(
            status="PUBLISH").order_by('-created_at')
        gaming_serializer = ProductListBySerializerForHomeData(
            gaming_product, many=True, context={"request": request})

        # brand list
        brand_list = Brand.objects.filter(
            is_active=True).order_by('-created_at')
        brand_list_serializer = BrandSerializer(
            brand_list, many=True, context={"request": request})

        # single row data
        single_row_data = HomeSingleRowData.objects.filter(
            Q(is_active=True)).order_by('-created_at')[:1]
        single_row_data_serializer = SingleRowDataSerializer(
            single_row_data, many=True, context={"request": request})

        # poster under slider static
        poster_under_static_data = Advertisement.objects.filter(Q(work_for='SLIDER_SMALL_STATIC'), Q(
            is_active=True), Q(is_gaming=False)).order_by('-created_at')[:2]
        poster_under_static_data_serializer = SliderAdvertisementDataSerializer(
            poster_under_static_data, many=True, context={"request": request})

        # poster under slider carousel
        poster_under_carousel_data = Advertisement.objects.filter(
            Q(work_for='SLIDER_SMALL_CAROUSEL'), Q(is_active=True), Q(is_gaming=False)).order_by('-created_at')
        poster_under_carousel_data_serializer = SliderAdvertisementDataSerializer(
            poster_under_carousel_data, many=True, context={"request": request})

        # poster under popular products
        poster_under_popular_products_data = Advertisement.objects.filter(
            Q(work_for='POPULAR_PRODUCT_POSTER'), Q(is_active=True), Q(is_gaming=False)).order_by('-created_at')[:3]
        poster_under_popular_products_data_serializer = AdvertisementDataSerializer(
            poster_under_popular_products_data, many=True, context={"request": request})

        # poster under featured products
        poster_under_featured_products_data = Advertisement.objects.filter(
            Q(work_for='FEATURED_PRODUCT_POSTER'), Q(is_active=True), Q(is_gaming=False)).order_by('-created_at')[:3]
        poster_under_featured_products_data_serializer = AdvertisementDataSerializer(
            poster_under_featured_products_data, many=True, context={"request": request})

        return Response({
            "slider_images": slider_images_serializer.data,
            "offer_slider_images": offer_slider_images_serializer.data,
            "featured_categories": featured_categories_serializer,
            "featured_products": featured_serializer.data,
            "popular_product": popular_serializer.data,
            "gaming_product": gaming_serializer.data,
            "brand_list": brand_list_serializer.data,
            "single_row_data_serializer": single_row_data_serializer.data,
            "poster_under_carousel_data_serializer": poster_under_carousel_data_serializer.data,
            "poster_under_static_data_serializer": poster_under_static_data_serializer.data,
            "poster_under_popular_products_data_serializer": poster_under_popular_products_data_serializer.data,
            "poster_under_featured_products_data_serializer": poster_under_featured_products_data_serializer.data,
        })


class GamingDataAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        # slider images
        slider_images = Advertisement.objects.filter(Q(work_for='SLIDER'), Q(
            is_active=True), Q(is_gaming=True)).order_by('-created_at')[:3]
        slider_images_serializer = AdvertisementDataSerializer(
            slider_images, many=True, context={"request": request})

        # sub_categories_with_logo
        categories_with_logo = SubCategory.objects.filter(
            category__is_gaming__icontains=True, is_active=True).order_by('-created_at')[:8]
        categories_with_logo_serializer = product_sub_catListSerializer(
            categories_with_logo, many=True, context={"request": request})

        # popular_sub_categories
        popular_categories = SubCategory.objects.filter(
            category__is_gaming__icontains=True, is_active=True).order_by("ordering_number")
        popular_categories_serializer = product_sub_catListSerializer(
            popular_categories, many=True, context={"request": request})

        # popular products
        popular = Product.objects.filter(category__is_gaming__icontains=True, status="PUBLISH").annotate(
            count=Count('product_review_product')).order_by('-count')
        popular_serializer = ProductListBySerializer(
            popular, many=True, context={"request": request})

        # poster under popular products
        poster_under_popular_products_data = Advertisement.objects.filter(
            Q(work_for='POPULAR_PRODUCT_POSTER'), Q(is_active=True), Q(is_gaming=True)).order_by('-created_at')[:3]
        poster_under_popular_products_data_serializer = AdvertisementDataSerializer(
            poster_under_popular_products_data, many=True, context={"request": request})

        # featured
        featured = Product.objects.filter(
            category__is_gaming__icontains=True, status='PUBLISH', is_featured=True).order_by('-created_at')
        featured_serializer = ProductListBySerializer(
            featured, many=True, context={"request": request})

        # poster under featured products
        poster_under_featured_products_data = Advertisement.objects.filter(
            Q(work_for='FEATURED_PRODUCT_POSTER'), Q(is_active=True), Q(is_gaming=True)).order_by('-created_at')[:3]
        poster_under_featured_products_data_serializer = AdvertisementDataSerializer(
            poster_under_featured_products_data, many=True, context={"request": request})

        # brand list
        brand_list = Brand.objects.filter(
            is_active=True, is_gaming=True).order_by('-created_at')
        brand_list_serializer = BrandSerializer(
            brand_list, many=True, context={"request": request})

        # single row data
        single_row_data = HomeSingleRowData.objects.filter(
            Q(is_active=True)).order_by('-created_at')[:1]
        single_row_data_serializer = SingleRowDataSerializer(
            single_row_data, many=True, context={"request": request})

        return Response({
            "poster_under_featured_products_data_serializer": poster_under_featured_products_data_serializer.data,
            "slider_images": slider_images_serializer.data,
            "categories_with_logo_serializer": categories_with_logo_serializer.data,
            "popular_categories_serializer": popular_categories_serializer.data,
            "popular_product": popular_serializer.data,
            "poster_under_popular_products_data_serializer": poster_under_popular_products_data_serializer.data,
            "featured_products": featured_serializer.data,
            "brand_list": brand_list_serializer.data,
            "single_row_data_serializer": single_row_data_serializer.data,
        })


class ContactUsAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ContactUsSerializer

    def post(self, request):
        try:
            name = request.data.get('name')
            email = request.data.get('email')
            phone = request.data.get('phone')
            message = request.data.get('message')
            contact = ContactUs(name=name, email=email,
                                phone=phone, message=message)
            contact.save()
            return Response({"message": "Your message has been sent successfully."})
        except:
            return Response({"message": "Fill up all the fields."})

    def get(self, request):
        contact = ContactUs.objects.all()
        contact_serializer = ContactUsSerializer(contact, many=True)
        return Response(contact_serializer.data)


class CreateGetFaqAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = FaqSerializer

    def post(self, request):
        try:
            question = request.data.get('question')
            answer = request.data.get('answer')
            faq = FAQ(question=question, answer=answer)
            faq.save()
            return Response({"message": "Faq has been created successfully."})
        except:
            return Response({"message": "Fill up all the fields."})

    def get(self, request):
        faq = FAQ.objects.all()
        faq_serializer = FaqSerializer(faq, many=True)
        return Response(faq_serializer.data)


class ProductListHomeCompareAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListBySerializer

    def get_queryset(self):
        queryset = Product.objects.filter(
            status='PUBLISH').order_by('-created_at')
        if queryset:
            return queryset
        else:
            raise ValidationError({"msg": 'No Publish products available!'})


class GamingCategoryListAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = StoreCategoryAPIViewListSerializer

    def get_queryset(self):
        queryset = Category.objects.filter(
            title__icontains='gaming', is_active=True).order_by('ordering_number')
        return queryset


class ProductListByCategoryGamingPopularProductsAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListBySerializer
    pagination_class = ProductCustomPagination
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        # work with dynamic pagination page_size
        try:
            pagination = self.kwargs['pagination']
        except:
            pagination = 10
        self.pagination_class.page_size = pagination

        id = self.kwargs['id']
        type = self.kwargs['type']

        queryset = Product.objects.filter(category__title__icontains='gaming', status='PUBLISH').annotate(
            count=Count('product_review_product')).order_by('-count')

        if id and type:
            if type == 'category':
                queryset = queryset.filter(Q(category=id))

            if type == 'sub_category':
                queryset = queryset.filter(Q(sub_category=id))

            if type == 'sub_sub_category':
                queryset = queryset.filter(Q(sub_sub_category=id))

        else:
            queryset = Product.objects.filter(category__title__icontains='gaming', status='PUBLISH').annotate(
                count=Count('product_review_product')).order_by('-count')

        return queryset


class GamingFeaturedProductListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListBySerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        # work with dynamic pagination page_size
        try:
            pagination = self.kwargs['pagination']
        except:
            pagination = 10
        self.pagination_class.page_size = pagination

        queryset = Product.objects.filter(
            category__title__icontains='gaming', is_featured=True, status='PUBLISH').order_by('-created_at')

        return queryset


class CorporateDealCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CorporateDealCreateSerializer

    def post(self, request, *args, **kwargs):
        return super(CorporateDealCreateAPIView, self).post(request, *args, **kwargs)


class RequestQuoteAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RequestQuoteSerializer

    def post(self, request, *args, **kwargs):
        return super(RequestQuoteAPIView, self).post(request, *args, **kwargs)


class SingleRowDataAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        # single row data
        single_row_data = HomeSingleRowData.objects.filter(
            Q(is_active=True)).order_by('-created_at')[:1]
        single_row_data_serializer = SingleRowDataSerializer(
            single_row_data, many=True, context={"request": request})

        return Response({
            "single_row_data": single_row_data_serializer.data,
        })


class AboutUsDataAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AboutUsSerializer

    def get(self, request, *args, **kwargs):
        about_us = AboutUs.objects.filter(
            is_active=True).order_by('-created_at')[:1]
        serializer = AboutUsSerializer(about_us, many=True)
        return Response(serializer.data)


class TermsAndConditionDataAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = TermsAndConditionSerializer

    def get(self, request, *args, **kwargs):
        about_us = TermsAndCondition.objects.filter(
            is_active=True).order_by('-created_at')[:1]
        serializer = TermsAndConditionDataAPIView(about_us, many=True)
        return Response(serializer.data)


class OnlineServiceSupportDataAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = OnlineServiceSupportSerializer

    def get(self, request, *args, **kwargs):
        about_us = OnlineServiceSupport.objects.filter(
            is_active=True).order_by('-created_at')[:1]
        serializer = OnlineServiceSupportDataAPIView(about_us, many=True)
        return Response(serializer.data)


class PaymentMethodDataAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PaymentMethodSerializer

    def get(self, request, *args, **kwargs):
        about_us = PaymentMethod.objects.filter(
            is_active=True).order_by('-created_at')[:1]
        serializer = PaymentMethodDataAPIView(about_us, many=True)
        return Response(serializer.data)


class RefundAndReturnPolicyDataAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RefundAndReturnPolicySerializer

    def get(self, request, *args, **kwargs):
        about_us = RefundAndReturnPolicy.objects.filter(
            is_active=True).order_by('-created_at')[:1]
        serializer = RefundAndReturnPolicyDataAPIView(about_us, many=True)
        return Response(serializer.data)


class ShippingDataAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ShippingSerializer

    def get(self, request, *args, **kwargs):
        about_us = Shipping.objects.filter(
            is_active=True).order_by('-created_at')[:1]
        serializer = ShippingDataAPIView(about_us, many=True)
        return Response(serializer.data)


class PrivacyPolicyDataAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PrivacyPolicySerializer

    def get(self, request, *args, **kwargs):
        about_us = PrivacyPolicy.objects.filter(
            is_active=True).order_by('-created_at')[:1]
        serializer = PrivacyPolicyDataAPIView(about_us, many=True)
        return Response(serializer.data)


class ServiceCenterDataAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ServiceCenterSerializer

    def get(self, request, *args, **kwargs):
        about_us = ServiceCenter.objects.filter(
            is_active=True).order_by('-created_at')[:1]
        serializer = ServiceCenterDataAPIView(about_us, many=True)
        return Response(serializer.data)


class AboutUsListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AboutUsSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = AboutUs.objects.all().order_by('-created_at')
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'About Us data does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not view About Us list, because you are not an Admin or a Staff!'})


class TermsAndConditionListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TermsAndConditionSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = TermsAndCondition.objects.all().order_by('-created_at')
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Terms And Condition data does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not view Terms And Condition list, because you are not an Admin or a Staff!'})


class OnlineServiceSupportListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnlineServiceSupportSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = OnlineServiceSupport.objects.all().order_by('-created_at')
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Online Service Support data does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not view Online Service Support list, because you are not an Admin or a Staff!'})


class PaymentMethodListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentMethodSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = PaymentMethod.objects.all().order_by('-created_at')
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Payment Method data does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not view Payment Method list, because you are not an Admin or a Staff!'})


class RefundAndReturnPolicyListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RefundAndReturnPolicySerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = RefundAndReturnPolicy.objects.all().order_by('-created_at')
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Refund And Return Policy data does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not view Refund And Return Policy list, because you are not an Admin or a Staff!'})


class ShippingListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShippingSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = Shipping.objects.all().order_by('-created_at')
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Shipping data does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not view Shipping list, because you are not an Admin or a Staff!'})


class PrivacyPolicyListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrivacyPolicySerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = PrivacyPolicy.objects.all().order_by('-created_at')
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Privacy Policy data does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not view Privacy Policy list, because you are not an Admin or a Staff!'})


class ServiceCenterListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceCenterSerializer
    pagination_class = ProductCustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            queryset = ServiceCenter.objects.all().order_by('-created_at')
            if queryset:
                return queryset
            else:
                raise ValidationError(
                    {"msg": 'Service Center data does not exist!'})
        else:
            raise ValidationError(
                {"msg": 'You can not view Service Center list, because you are not an Admin or a Staff!'})


class AboutUsCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AboutUsSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(AboutUsCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create about us, because you are not an Admin or a Staff!'})


class TermsAndConditionCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TermsAndConditionSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(TermsAndConditionCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create Terms And Condition, because you are not an Admin or a Staff!'})


class OnlineServiceSupportCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnlineServiceSupportSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(OnlineServiceSupportCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create Online Service Support, because you are not an Admin or a Staff!'})


class PaymentMethodCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentMethodSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(PaymentMethodCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create Payment Method, because you are not an Admin or a Staff!'})


class RefundAndReturnPolicyCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RefundAndReturnPolicySerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(RefundAndReturnPolicyCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create Refund And Return Policy, because you are not an Admin or a Staff!'})


class ShippingCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShippingSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(ShippingCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create Shipping, because you are not an Admin or a Staff!'})


class PrivacyPolicyCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrivacyPolicySerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(PrivacyPolicyCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create Privacy Policy, because you are not an Admin or a Staff!'})


class ServiceCenterCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceCenterSerializer

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True or self.request.user.is_staff == True:
            return super(ServiceCenterCreateAPIView, self).post(request, *args, **kwargs)
        else:
            raise ValidationError(
                {"msg": 'You can not create Service Center, because you are not an Admin or a Staff!'})


class AboutUsUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AboutUsSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        target_id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            query = AboutUs.objects.filter(id=target_id)
            if query:
                return query
            else:
                raise ValidationError({"msg": 'About Us not found'})
        else:
            raise ValidationError(
                {"msg": 'You can not update  About Us, because you are not an Admin, Staff or owner!'})


class TermsAndConditionUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TermsAndCondition
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        target_id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            query = TermsAndCondition.objects.filter(id=target_id)
            if query:
                return query
            else:
                raise ValidationError({"msg": 'Terms And Condition not found'})
        else:
            raise ValidationError(
                {"msg": 'You can not update  Terms And Condition, because you are not an Admin, Staff or owner!'})


class OnlineServiceSupportUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnlineServiceSupport
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        target_id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            query = OnlineServiceSupport.objects.filter(id=target_id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Online Service Support not found'})
        else:
            raise ValidationError(
                {"msg": 'You can not update  Online Service Support, because you are not an Admin, Staff or owner!'})


class PaymentMethodUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentMethod
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        target_id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            query = PaymentMethod.objects.filter(id=target_id)
            if query:
                return query
            else:
                raise ValidationError({"msg": 'Payment Method not found'})
        else:
            raise ValidationError(
                {"msg": 'You can not update  Payment Method, because you are not an Admin, Staff or owner!'})


class RefundAndReturnPolicyUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RefundAndReturnPolicy
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        target_id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            query = RefundAndReturnPolicy.objects.filter(id=target_id)
            if query:
                return query
            else:
                raise ValidationError(
                    {"msg": 'Refund And Return Policy not found'})
        else:
            raise ValidationError(
                {"msg": 'You can not update  Refund And Return Policy, because you are not an Admin, Staff or owner!'})


class ShippingUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Shipping
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        target_id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            query = Shipping.objects.filter(id=target_id)
            if query:
                return query
            else:
                raise ValidationError({"msg": 'Shipping not found'})
        else:
            raise ValidationError(
                {"msg": 'You can not update  Shipping, because you are not an Admin, Staff or owner!'})


class PrivacyPolicyUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrivacyPolicy
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        target_id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            query = PrivacyPolicy.objects.filter(id=target_id)
            if query:
                return query
            else:
                raise ValidationError({"msg": 'Privacy Policy not found'})
        else:
            raise ValidationError(
                {"msg": 'You can not update  Privacy Policy, because you are not an Admin, Staff or owner!'})


class ServiceCenterUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceCenter
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def get_queryset(self):
        target_id = self.kwargs['id']
        if self.request.user.is_superuser == True or self.request.user.is_staff == True or self.request.user.is_seller == True:
            query = ServiceCenter.objects.filter(id=target_id)
            if query:
                return query
            else:
                raise ValidationError({"msg": 'Service Center not found'})
        else:
            raise ValidationError(
                {"msg": 'You can not update  Service Center, because you are not an Admin, Staff or owner!'})
