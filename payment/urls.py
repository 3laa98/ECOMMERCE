from django.urls import path

from payment import views

urlpatterns = [
    path(
        'create-payment-intent/',
        views.create_payment_intent,
        name='create-payment-intent',
    ),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]
