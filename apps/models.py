from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db.models import Model, CharField, PositiveIntegerField, ForeignKey, CASCADE, BooleanField, Case, When, \
    Value, ImageField
from rest_framework.exceptions import ValidationError


class User(AbstractUser):
    score = PositiveIntegerField(default=0)

    @property
    def level(self):
        queryset = User.objects.annotate(level=Case
            (
            When(score__gt=89, then=Value('hard')),
            When(score__gte=76, then=Value('medium')),
            default=Value('easy'),
            output_field=CharField(),
        )
        )
        return queryset.get(pk=self.pk).level


class Category(Model):
    name = CharField(max_length=100)


class Product(Model):
    name = CharField(max_length=120)
    price = PositiveIntegerField(db_default=True)
    is_premium = BooleanField(default=False)
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
    owner = ForeignKey('apps.User', CASCADE, related_name='products')


def file_size_validator(file):
    max_size = 10 * 1024 * 1024  # 10 MB
    if file.size > max_size:
        raise ValidationError(f"Hajm: {file.size / (1024 * 1024):.2f} MB")


class ProductImage(Model):
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='images')
    image = ImageField(
        upload_to='products/image/',
        validators=[FileExtensionValidator(
            ['png', 'jpg', 'jpeg']),
            file_size_validator
        ]
    )
