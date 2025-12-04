from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Order endpoints
    path('orders/', views.order_list, name='order-list'),
    path('orders/<int:order_id>/', views.order_detail, name='order-detail'),
    path('orders/search/', views.order_search, name='order-search'),
    path('orders/statistics/', views.order_statistics, name='order-statistics'),


]

