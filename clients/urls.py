from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='clients_list'),
    path('<str:client_id>/', views.client_detail, name='client_detail'),
    path('<str:client_id>/contract-<int:contract_id>/', views.contract_detail, name='contract_detail'),
]