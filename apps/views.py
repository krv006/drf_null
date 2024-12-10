from django.db.models import Count
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView

from apps.models import Product, Category, User, ProductImage, Film, Genre
from apps.serializers import ProductModelSerializer, CategoryModelSerializer, UserModelSerializer, \
    ProductImageModelSerializer, FilmModelSerializer, GenreModelSerializer


@extend_schema(tags=['product'])
class ProductListCreate(ListCreateAPIView):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductModelSerializer


@extend_schema(tags=['product'])
class CategoryListView(ListCreateAPIView):
    queryset = Category.objects.annotate(product_count=Count('products'))
    serializer_class = CategoryModelSerializer


@extend_schema(tags=['user'])
class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.annotate(product_count=Count('products'))
    serializer_class = UserModelSerializer


@extend_schema(tags=['product'])
class ProductImageListCreateAPIView(ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageModelSerializer


@extend_schema(tags=['film'])
class FilmListCreateAPIView(ListCreateAPIView):
    queryset = Film.objects.prefetch_related('genres').all()
    serializer_class = FilmModelSerializer


@extend_schema(tags=['film'])
class GenreListCreateAPIView(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreModelSerializer
