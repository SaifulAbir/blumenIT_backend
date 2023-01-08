from rest_framework import serializers
from .models import *
from product.models import Category, SubCategory, SubSubCategory

class SliderImagesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderImage
        fields = [
                'id',
                'image',
                'bold_text',
                'small_text',
                ]


class product_catListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
                'id',
                'title',
                'icon',
                'banner',
                ]


class product_sub_catListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = [
                'id',
                'title',
                'icon'
                ]


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
                ]


class PosterUnderSliderDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosterUnderSlider
        fields = [
                'id',
                'image',
                'is_active',
                ]


class PosterUnderPopularProductsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularProductsUnderPoster
        fields = [
                'id',
                'image',
                'bold_text',
                'small_text',
                'is_active',
                ]


class PosterUnderFeaturedProductsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedProductsUnderPoster
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
            queryset = SubCategory.objects.filter(category=obj.id, is_active=True).distinct()
            serializer = SubCategorySerializerForMegaMenu(instance=queryset, many=True)
            return serializer.data
        except:
            return []