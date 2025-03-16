from django.urls import path
from order import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('orders', views.get_orders, name='orders'),
]