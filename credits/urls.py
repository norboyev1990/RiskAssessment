from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('general_info', views.general_info, name='general_info'),
    path('npl_clients', views.npl_clients, name='npl_clients'),
    path('toxic_loans', views.toxic_loans, name='toxic_loans'),
    path('overdue_loans', views.overdue_loans, name='overdue_loans'),
    path('by_terms', views.by_terms, name='by_terms'),
    path('by_subjects', views.by_subjects, name='by_subjects'),
    path('by_segments', views.by_segments, name='by_segments'),
    path('by_currency', views.by_currency, name='by_currency'),
    path('by_branches', views.by_branches, name='by_branches'),
    path('by_products', views.by_products, name='by_products'),
    path('by_percents/<str:sts>/', views.by_percents, name='by_percents'),
    path('by_averages/<str:sts>/', views.by_averages, name='by_averages'),
    path('issued_overdues/', views.issued_overdues, name='issued_overdues'),
    path('export_doklad_excel/', views.export_all_tables, name='export_doklad_word'),
    path('export_doklad_word/', views.export_all_docx, name='export_doklad_excel'),
]