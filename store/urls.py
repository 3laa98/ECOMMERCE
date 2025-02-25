from django.urls import path

from store import views

urlpatterns = [
    path('', views.store, name='store'),
    path('products/', views.product_list, name='product-list'),
    path('product/<slug:product_slug>/', views.product_info, name='product-info'),
    path('add-product/', views.add_product, name='add-product'),
    path('delete-product/<int:product_id>/', views.del_product, name='delete-product'),
]
