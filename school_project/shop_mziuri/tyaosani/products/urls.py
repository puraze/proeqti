# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/create/', views.create_product, name='create_product'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:id>/update/', views.update_product, name='update_product'),
    path('product/<int:id>/delete/', views.delete_product, name='delete_product'),
]