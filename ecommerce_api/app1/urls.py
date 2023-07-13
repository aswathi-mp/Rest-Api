from django.urls import path
from . import views

urlpatterns = [
    path('customer/', views.CustomerView.as_view()),
    path('customer/<int:id>/', views.CustomerView.as_view()),
    path('product/', views.ProductView.as_view()),
    path('product/<int:id>/', views.ProductView.as_view()),
    path('product/active/<int:id>/', views.ActiveProduct.as_view()),
    path('product/inactive/<int:id>/', views.InactiveProduct.as_view()), 
]