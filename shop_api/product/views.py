from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer
)

# Categories
from django.db.models import Count
class CategoryListView(ListAPIView):
    queryset = Category.objects.annotate(
        products_count=Count('products')
    )
    serializer_class = CategorySerializer


class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'






# Products
class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


# Reviews
class ReviewListView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailView(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'

from rest_framework.generics import ListAPIView
from django.db.models import Prefetch, Count
from .models import Product, Review
from .serializers import ProductReviewSerializer

class ProductWithReviewsView(ListAPIView):
    queryset = Product.objects.prefetch_related(
        Prefetch('reviews', queryset=Review.objects.all())
    )
    serializer_class = ProductReviewSerializer
