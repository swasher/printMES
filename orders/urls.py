from django.urls import path
from orders import views

app_name = "orders"

urlpatterns = [
    path('', views.orders, name='orders'),
    path('create_new_order', views.create_new_order, name='create_new_order'),
    # path(r'^print_pdf_order/(?P<orderid>\d+)/$', views.print_pdf_order, name='print_pdf_order'),
    path('print_pdf_order/<int:orderid>', views.print_pdf_order, name='print_pdf_order'),
    # path(r'^copy_order/(?P<orderid>\d+)/$', views.copy_order, name='copy_order'),
    path('copy_order/<int:orderid>', views.copy_order, name='copy_order'),
]
