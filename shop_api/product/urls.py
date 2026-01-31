from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryDetailView,
    ProductListCreateView,
    ProductDetailView,
    ReviewListCreateView,
    ReviewDetailView,
    RegisterView,
    ConfirmView,
    LoginView
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view()),
    path('categories/<int:id>/', CategoryDetailView.as_view()),

    path('products/', ProductListCreateView.as_view()),
    path('products/<int:id>/', ProductDetailView.as_view()),

    path('reviews/', ReviewListCreateView.as_view()),
    path('reviews/<int:id>/', ReviewDetailView.as_view()),

    path('accounts/register/', RegisterView.as_view()),
    path('accounts/confirm/', ConfirmView.as_view()),
    path('accounts/login/', LoginView.as_view()),
]
