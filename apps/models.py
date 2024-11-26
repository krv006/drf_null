from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, PositiveIntegerField, ForeignKey, CASCADE, BooleanField, Case, When, \
    Value


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
