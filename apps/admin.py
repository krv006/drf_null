from django.contrib import admin

from apps.models import Product, Category, User, ProductImage

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(ProductImage)
