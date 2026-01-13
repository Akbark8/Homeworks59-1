from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryDetailView,
    ProductListCreateView,
    ProductDetailView,
    ReviewListCreateView,
    ReviewDetailView, RegisterView, ConfirmView, LoginView
)

urlpatterns = [
    # Categories
    path('categories/', CategoryListCreateView.as_view()),
    path('categories/<int:id>/', CategoryDetailView.as_view()),

    # Products
    path('products/', ProductListCreateView.as_view()),
    path('products/<int:id>/', ProductDetailView.as_view()),

    # Reviews
    path('reviews/', ReviewListCreateView.as_view()),
    path('reviews/<int:id>/', ReviewDetailView.as_view()),

    path('users/register/', RegisterView.as_view()),
    path('users/confirm/', ConfirmView.as_view()),
    path('users/login/', LoginView.as_view()),
]


