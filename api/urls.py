from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.clients_list),
    path('clients/<int:pk>/', views.clients_detail),
    path('credits/stat/', views.get_stat_data),
    path('credits/geos/', views.get_gdp_data),
    path('credits/kprbymonth/<str:type>', views.get_krp_by_month),
    path('credits/get_data_subjects/', views.get_data_subjects, name='get_data_subjects'),
    path('credits/get_data_branches/', views.get_data_branches, name='get_data_branches'),
    path('credits/get_data_branches/', views.get_data_branches, name='get_data_branches'),
    path('credits/get_data_average/', views.get_data_average, name='get_data_average'),
    path('credits/get_data_average_juridical/', views.get_data_average_juridical, name='get_data_average_juridical'),
]