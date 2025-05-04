from django.urls import path
from . import views
from quiz.views import quiz_view

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('create_product/', views.create_product, name='create_product'),
    path('update_product/<int:id>', views.update_product, name='update_product'),
    path('delete_product/<int:id>', views.delete_product, name='delete_product'),
    path('quiz/', quiz_view, name='quiz')
]