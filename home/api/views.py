from rest_framework.views import APIView
from home.models import SliderImage, DealsOfTheDay, ProductView
from home.serializers import SliderImagesListSerializer, DealsOfTheDayListSerializer, product_catListSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from datetime import date, timedelta
from django.db.models import Avg, Prefetch, Q, Count

from product.models import Product, Category, ProductReview
from product.serializers import ProductListSerializer

class HomeDataAPIView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        # slider images
        slider_images = SliderImage.objects.filter(is_active=True)
        slider_images_serializer = SliderImagesListSerializer(slider_images, many=True, context={"request": request})

        # deals of the day
        today = date.today()
        deals_of_the_day = DealsOfTheDay.objects.filter( start_date__lte=today, end_date__gte=today, is_active = True)
        deals_of_the_day_serializer = DealsOfTheDayListSerializer(deals_of_the_day, many=True, context={"request": request})

        # top 20 best seller
        top_20_best_seller = Product.objects.filter(status='ACTIVE').order_by('-sell_count')[:10]
        top_20_best_seller_serializer = ProductListSerializer(top_20_best_seller, many=True, context={"request": request})

        # top category of the month
        top_best_sellers = Product.objects.filter(status='ACTIVE').order_by('-sell_count')
        category_ids = top_best_sellers.values_list('category__id', flat=True).distinct()
        final_category_ids = []
        for category_id in category_ids:
            if category_id not in final_category_ids:
                final_category_ids.append(category_id)
        product_cat = Category.objects.filter(id__in=final_category_ids)[:6]
        product_cat_serializer = product_catListSerializer(product_cat, many=True, context={"request": request})

        # new arrivals
        new_arrivals = Product.objects.filter(status='ACTIVE').order_by('-created_at')[:10]
        new_arrivals_serializer = ProductListSerializer(new_arrivals, many=True, context={"request": request})

        # featured
        featured = Product.objects.filter(status='ACTIVE', is_featured=True).order_by('-created_at')[:10]
        featured_serializer = ProductListSerializer(featured, many=True, context={"request": request})

        # most popular
        # most_popular = Product.objects.filter(status="ACTIVE").annotate(Avg("product_review_product__rating_number")).order_by('-product_review_product__rating_number')
        most_popular = Product.objects.filter(status="ACTIVE").annotate(count=Count('product_review_product')).order_by('-count')
        most_popular_serializer = ProductListSerializer(most_popular, many=True, context={"request": request})


        return Response({
            "slider_images": slider_images_serializer.data,
            "deals_of_the_day": deals_of_the_day_serializer.data,
            "top_20_best_seller": top_20_best_seller_serializer.data,
            "categories_of_the_month": product_cat_serializer.data,
            "new_arrivals": new_arrivals_serializer.data,
            "featured": featured_serializer.data,
            "most_popular": most_popular_serializer.data
        })

# # class RecentAPIView(APIView):
# #     def get(self, request):
# #         today = date.today()
# #         last_week = today - timedelta(days=7)
# #         user = self.request.user.id
# #         recent_view = Product.objects.filter(product_view_count__view_date__gt=last_week).order_by('-product_view_count__view_date')[:24]
# #         recent_view_serializer = productListSerializer(recent_view, many=True)
# #         return Response({"recent_view":recent_view_serializer.data })