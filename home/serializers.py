from rest_framework import serializers
from .models import *
from product.models import Category, SubCategory, SubSubCategory


class product_catListSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField('get_type')

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'icon',
            'banner',
            'type'
        ]

    def get_type(self, obj):
        return 'cate'


class product_sub_catListSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField('get_type')

    class Meta:
        model = SubCategory
        fields = [
            'id',
            'title',
            'icon',
            'type'
        ]

    def get_type(self, obj):
        return 'sub'


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = [
            'id',
            'question',
            'answer',
            'is_active',
        ]


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'message',
            'is_active',
        ]


class SingleRowDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSingleRowData
        fields = [
            'id',
            'phone',
            'whats_app_number',
            'email',
            'bottom_banner',
            'is_active',
            'header_logo',
            'footer_logo',
            'footer_description',
            'facebook',
            'twitter',
            'instagram',
            'whatsapp',
            'messenger',
            'linkedin',
            'youtube',
        ]


class SliderAdvertisementDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = [
            'id',
            'image',
            'is_active',
        ]


class AdvertisementDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = [
            'id',
            'image',
            'bold_text',
            'small_text',
            'is_active',
        ]


class GamingSubSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSubCategory
        fields = ['id', 'title']


class SubCategorySerializerForMegaMenu(serializers.ModelSerializer):
    sub_sub_category = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = [
            'id',
            'title',
            'sub_sub_category'
        ]

    def get_sub_sub_category(self, obj):
        selected_sub_sub_category = SubSubCategory.objects.filter(
            sub_category=obj).distinct()
        return GamingSubSubCategorySerializer(selected_sub_sub_category, many=True).data


class StoreCategoryAPIViewListSerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'icon', 'banner', 'sub_category']

    def get_sub_category(self, obj):
        try:
            queryset = SubCategory.objects.filter(
                category=obj.id, is_active=True).distinct()
            serializer = SubCategorySerializerForMegaMenu(
                instance=queryset, many=True)
            return serializer.data
        except:
            return []


class CorporateDealCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorporateDeal
        fields = ['id', 'first_name', 'last_name', 'email', 'company_name',
                  'phone', 'region', 'details_text', 'attached_file']


class RequestQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestQuote
        fields = [
            'name',
            'email',
            'phone',
            'company_name',
            'website',
            'address',
            'services',
            'overview'
        ]


class PagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pages
        fields = [
            'id',
            'title',
            'content',
            'type',
            'is_active',
            'created_at'
        ]
