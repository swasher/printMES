from django.urls import path
from stanzforms import views

urlpatterns =[
    path('doska_list', views.doska_list, name='doska_list'),
    path('knife_list/<int:doskaid>', views.knife_list, name='knife_list'),
]
