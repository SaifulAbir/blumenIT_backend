# from rest_framework import serializers
# from .models import *
# from product.models import Product, ProductCategory
# from product.serializers import ProductDetailsSerializer, ProductMediaSerializer

# # list Serializer start
# class SliderImagesListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SliderImage
#         fields = [
#                 'id',
#                 'file',
#                 'text',
#                 ]

# class DealsOfTheDayListSerializer(serializers.ModelSerializer):
#     product = ProductDetailsSerializer(many=True, read_only=True)
#     class Meta:
#         model = DealsOfTheDay
#         fields = [
#                 'id',
#                 'product',
#                 'discount_price',
#                 'discount_price_type',
#                 'start_date',
#                 'end_date'
#                 ]

# class productListSerializer(serializers.ModelSerializer):
#     product_media = ProductMediaSerializer(many=True, read_only=True)
#     product_category_name = serializers.SerializerMethodField()
#     average_rating = serializers.CharField(read_only=True)
#     class Meta:
#         model = Product
#         fields = [
#                 'id',
#                 'title',
#                 'slug',
#                 'price',
#                 'old_price',
#                 'short_description',
#                 'quantity',
#                 'rating',
#                 'average_rating',
#                 'status',
#                 'is_featured',
#                 'product_category_name',
#                 'product_brand',
#                 'thumbnail',
#                 'product_media'
#                 ]

#     def get_product_category_name(self, obj):
#         if obj.product_category:
#             get_product_category=ProductCategory.objects.get(id= obj.product_category.id)
#             return get_product_category.name
#         else :
#             return obj.get_product_category

# class product_catListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductCategory
#         fields = [
#                 'id',
#                 'name',
#                 'logo',
#                 'cover',
#                 ]

# # list Serializer end




# # class mostPopularProductListSerializer(serializers.ModelSerializer):
# #     average_rating = serializers.CharField(read_only=True)
# #     class Meta:
# #         model = Product
# #         fields = [
# #                 'id',
# #                 'title',
# #                 'slug',
# #                 'price',
# #                 'rating',
# #                 'thumbnail',
# #                 'average_rating'
# #                 ]
