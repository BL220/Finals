from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.OrderHistoryView.as_view(), name='order_history'),
]
