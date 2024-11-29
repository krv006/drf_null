from django.urls import path

from apps.views import ProductListCreate, CategoryListView, UserListCreateAPIView, GenreListCreateAPIView, \
    FilmListCreateAPIView

urlpatterns = [
    path('product/', ProductListCreate.as_view()),
    path('category/', CategoryListView.as_view()),
    path('user/', UserListCreateAPIView.as_view()),
    path('genre/', GenreListCreateAPIView.as_view()),
    path('film/', FilmListCreateAPIView.as_view()),

]
