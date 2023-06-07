from rest_framework import serializers
from .models import *
from product.models import Category, SubCategory, SubSubCategory, CategoryBannerImages


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


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ['id', 'our_values', 'our_vision', 'our_mission',
                  'our_goals', 'customer_relationship', 'our_target_market', 'retail_wholesale_trade', 'footer_text', 'promise_text', 'our_values_image', 'customer_relationship_image', 'our_target_market_image', 'retail_wholesale_trade_image', 'is_active']


class SingleRowDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSingleRowData
        fields = [
            'id',
            'phone',
            'whats_app_number',
            'shop_address',
            'email',
            'bottom_banner',
            'bottom_banner_url',
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
            'image_url',
            'is_active',
        ]


class AdvertisementDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = [
            'id',
            'image',
            'image_url',
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


class MediaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFiles
        fields = [
            'id',
            'title',
            'file',
            'is_active',
            'created_at'
        ]


class MediaSerializer(serializers.ModelSerializer):
    files = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False)

    class Meta:
        model = MediaChunk
        fields = [
            'id',
            'title',
            'files',
            'is_active',
            'created_at'
        ]

    def create(self, validated_data):

        # files
        try:
            files = validated_data.pop('files')
        except:
            files = ''

        media_chunk_instance = MediaChunk.objects.create(**validated_data)

        # files
        if files:
            for file in files:
                file_name = file.name.split('/')[-1]
                MediaFiles.objects.create(
                    chunk=media_chunk_instance, file=file, title=file_name, is_active=True)

        return media_chunk_instance
