from django.db.models import Count
from rest_framework.generics import ListCreateAPIView

from apps.models import Product, Category, User, ProductImage
from apps.serializers import ProductModelSerializer, CategoryModelSerializer, UserModelSerializer, \
    ProductImageModelSerializer


class ProductListCreate(ListCreateAPIView):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductModelSerializer


class CategoryListView(ListCreateAPIView):
    queryset = Category.objects.annotate(product_count=Count('products'))
    serializer_class = CategoryModelSerializer


class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.annotate(product_count=Count('products'))
    serializer_class = UserModelSerializer


class ProductImageListCreateAPIView(ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageModelSerializer
