from django.urls import path
from .views import *
urlpatterns = [
    path('reqo_report/', reqo_report, name='reqo_report'), 
    path('shipping_report/', shipping_report, name='shipping_report'), 
    path('analytics_data/', analytics_data, name='analytics_data'),
    path('recent_orders/', recent_orders, name='recent_orders'),
    path('recent_req_orders/', recent_req_orders, name='recent_req_orders'),
    path('recent_shipping_orders/', recent_shipping_orders, name='recent_shipping_orders'),
    path('recent_orders_delivery/', recent_orders_delivery, name='recent_orders_delivery'),
    path('recent_req_orders_delivery/', recent_req_orders_delivery, name='recent_req_orders_delivery'),
    path('shipping_orders_delivery/', shipping_orders_delivery, name='shipping_orders_delivery'),
    path('req_partial_payment/', req_partial_payment, name='req_partial_payment'),
    path('order_partial_payment/', order_partial_payment, name='order_partial_payment'),
    path('order_partial_payment_table/', order_partial_payment_table, name='order_partial_payment_table'),

]
