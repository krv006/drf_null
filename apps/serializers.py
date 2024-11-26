from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, IntegerField
from rest_framework.serializers import ModelSerializer

from apps.models import Product, Category, User


class CategoryModelSerializer(ModelSerializer):
    product_count = IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'product_count',)


class ProductModelSerializer(ModelSerializer):
    category = CategoryModelSerializer()

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'is_premium', 'category',)

    # def to_representation(self, instance):
    #     repr = super().to_representation(instance)
    #     repr['category'] = CategoryModelSerializer(instance.category).data
    #     return repr


class UserModelSerializer(ModelSerializer):
    level = SerializerMethodField()
    product_count = IntegerField(read_only=True)
    product_categories = SerializerMethodField()

    class Meta:
        model = User
        fields = 'id', 'username', 'score', 'last_login', 'level', 'product_count', 'product_categories',

    def get_product_count(self, obj):
        return obj.products.count()

    def get_product_categories(self, obj):
        return list(obj.products.values_list('category__name', flat=True))

    def get_level(self, obj):
        if obj.score > 89:
            return 'hard'
        elif obj.score >= 76:
            return 'medium'
        else:
            return 'easy'
