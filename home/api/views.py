from rest_framework.views import APIView
from home.models import SliderImage, DealsOfTheDay, ProductView
from home.serializers import SliderImagesListSerializer, DealsOfTheDayListSerializer, productListSerializer, product_catListSerializer
# from home.serializers import SliderImagesListSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from datetime import date, timedelta
from django.db.models import Avg, Prefetch, Q

from product.models import Product, ProductCategory, ProductReview

class HomeDataAPIView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        # slider images
        slider_images = SliderImage.objects.filter(is_active=True)
        slider_images_serializer = SliderImagesListSerializer(slider_images, many=True)

        # deals of the day
        today = date.today()
        deals_of_the_day = DealsOfTheDay.objects.filter( start_date__lte=today, end_date__gte=today, is_active = True)
        deals_of_the_day_serializer = DealsOfTheDayListSerializer(deals_of_the_day, many=True)

        # top 20 best seller
        top_20_best_seller = Product.objects.filter(status='ACTIVE').order_by('-sell_count')[:10]
        top_20_best_seller_serializer = productListSerializer(top_20_best_seller, many=True)

        # top category of the month
        top_best_sellers = Product.objects.filter(status='ACTIVE').order_by('-sell_count')
        category_ids = top_best_sellers.values_list('product_category__id', flat=True).distinct()
        final_category_ids = []
        for category_id in category_ids:
            if category_id not in final_category_ids:
                final_category_ids.append(category_id)
        product_cat = ProductCategory.objects.filter(id__in=final_category_ids)[:6]
        product_cat_serializer = product_catListSerializer(product_cat, many=True)

        # new arrivals
        new_arrivals = Product.objects.filter(status='ACTIVE').order_by('-created_at')[:10]
        new_arrivals_serializer = productListSerializer(new_arrivals, many=True)

        # featured
        featured = Product.objects.filter(status='ACTIVE', is_featured=True).order_by('-created_at')[:10]
        featured_serializer = productListSerializer(featured, many=True)

        # most popular 
        # most_popular = Product.objects.annotate(Avg('productReview__rating_number'))
        # product = Product.objects.filter(status='ACTIVE').order_by('-created_at')
        # review_avg = ProductReview.objects.filter(product = product).annotate(avg=Avg('rating_number'))
        # product = get_object_or_404(Product.objects.annotate(avg_rating_number=Avg('productReview__rating_number')),pk=1)
        # beers = Product.objects.order_by('-created_at').annotate(avg_rating_number=Avg('ratemodel__rating_number'))
        product = Product.objects.filter(status='ACTIVE').order_by('-created_at')
        # query = ProductReview.objects.annotate(avg=Avg('rating_number')).prefetch_related(
        #     Prefetch("product", queryset=Product.objects.filter(id__in=product).order_by('-created_at')))
        query = ProductReview.objects.annotate(avg=Avg('rating_number'))
        ca_ids = query.values_list('product__id', flat=True).distinct()
        print(str(ca_ids))


        return Response({"slider_images": slider_images_serializer.data, "deals_of_the_day": deals_of_the_day_serializer.data, "top_20_best_seller": top_20_best_seller_serializer.data, "product_cat_serializer": product_cat_serializer.data, "new_arrivals": new_arrivals_serializer.data, "featured": featured_serializer.data})

class RecentAPIView(APIView):
    def get(self, request):
        today = date.today()
        some_day_last_week = today - timedelta(days=7)
        user = self.request.user.id
        # recent_view = Product.objects.filter(id__in = ProductView.objects.filter(user=user).values('product').order_by('-view_count'))[:24]
        recent_view = Product.objects.filter(product_view_count__view_date__gt=some_day_last_week)[:24]
        recent_view_serializer = productListSerializer(recent_view, many=True)
        return Response({"recent_view":recent_view_serializer.data })