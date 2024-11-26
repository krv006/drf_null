from django.contrib import admin

from apps.models import Product, Category, User

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(User)

