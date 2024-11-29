from django.contrib import admin

from apps.models import Product, Category, User, ProductImage, Genre, Film

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(ProductImage)
admin.site.register(Genre)
admin.site.register(Film)
