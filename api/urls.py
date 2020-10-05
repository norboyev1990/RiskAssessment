from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.clients_list, name="api_clients_list"),
    path('clients/<int:pk>/', views.clients_detail, name="api_clients_detail"),
    path('credits/stat/', views.get_stat_data, name='get_stat_data'),
    path('credits/geos/', views.get_gdp_data),
    path('credits/kprbymonth/<str:type>', views.get_krp_by_month),
    path('credits/get_data_subjects/', views.get_data_subjects, name='get_data_subjects'),
    path('credits/get_data_subjects_npl/', views.get_data_subjects_npl, name='get_data_subjects_npl'),
    path('credits/get_data_branches/', views.get_data_branches, name='get_data_branches'),
    path('credits/get_data_branches_npl/', views.get_data_branches_npl, name='get_data_branches_npl'),
    path('credits/get_data_branches/', views.get_data_branches, name='get_data_branches'),
    path('credits/get_data_average/', views.get_data_average, name='get_data_average'),
    path('credits/get_data_products/', views.get_data_products, name='get_data_products'),
    path('credits/get_data_average_juridical/', views.get_data_average_juridical, name='get_data_average_juridical'),
    path('credits/get_data_average_juridical_npl/', views.get_data_average_juridical_npl, name='get_data_average_juridical_npl'),
    path('credits/get_big_data/', views.get_big_data, name='get_big_data')
]