from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField, IntegerField, HiddenField, CurrentUserDefault
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from apps.models import Product, Category, User, ProductImage, Film, Genre


class DynamicFieldsModelSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    # todo DynamicFieldsModelSerializer bu orqali detail lar yozsak boladi


class CategoryModelSerializer(DynamicFieldsModelSerializer):
    product_count = IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = 'id', 'name', 'product_count',


class ProductImageModelSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
        depth = 1 # todo product malumotlarini ob bergani yordam beradi


class ProductModelSerializer(ModelSerializer):
    category = CategoryModelSerializer()
    images = ProductImageModelSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = 'id', 'name', 'price', 'is_premium', 'category', 'images',

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
        categories = obj.products.prefetch_related('category').values_list('category__name', flat=True)
        return list(categories)

    def get_level(self, obj):
        if obj.score > 89:
            return 'hard'
        elif obj.score >= 76:
            return 'medium'
        else:
            return 'easy'


class GenreModelSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class FilmModelSerializer(ModelSerializer):
    genres_ids = PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        source='genres'
    )
    owner = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Film
        fields = 'id', 'name', 'released_date', 'genres_ids', 'owner',

    def to_representation(self, instance: Film):
        repr = super().to_representation(instance)
        repr['genres_ids'] = GenreModelSerializer(instance.genres.all(), many=True).data
        if instance.owner:
            owner = instance.owner.username
        else:
            owner = None
        repr['owner'] = owner
        return repr


def validate_custom(value):
    if value < 2000:
        raise ValidationError('2000 dan kichik bolishi mn emas')
    return value
