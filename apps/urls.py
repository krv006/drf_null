from django.urls import path

from apps.views import ProductListCreate, CategoryListView, UserListCreateAPIView

urlpatterns = [
    path('product/', ProductListCreate.as_view()),
    path('category/', CategoryListView.as_view()),
    path('user/', UserListCreateAPIView.as_view()),

]
