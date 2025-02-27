from django.urls import path

from cart import views

urlpatterns = [
    path('', views.cart_detail, name='cart-detail'),
    path('add/', views.cart_add, name='cart-add'),
    path('remove/', views.cart_remove, name='cart-remove'),
]
