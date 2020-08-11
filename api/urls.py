from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.clients_list),
    path('clients/<int:pk>/', views.clients_detail),
    path('credits/stat/', views.get_stat_data),
    path('credits/geos/', views.get_gdp_data),
]