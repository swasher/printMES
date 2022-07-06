from django.urls import path
from warehouse import views


urlpatterns = [
    path('customers_list', views.CustomerList.as_view(), name='customers_list'),
    path('maquette_list/<int:customerpk>', views.Maquette_list.as_view(), name='maquette_list'),
    path('maquette_detail/<int:pk>', views.Maquette_detail.as_view(), name='maquette_detail'),
    path('scan/<int:customerpk>', views.scan, name='scan'),
]