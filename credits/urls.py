from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='dashboard'),
    path('general_info', general_info, name='general_info'),
    path('npl_clients', npl_clients, name='npl_clients'),
    path('toxic_loans', toxic_loans, name='toxic_loans'),
    path('overdue_loans', overdue_loans, name='overdue_loans'),
    path('overdue_percents', overdue_percents, name='overdue_percents'),
    path('by_terms', by_terms, name='by_terms'),
    path('by_subjects', by_subjects, name='by_subjects'),
    path('by_segments', by_segments, name='by_segments'),
    path('by_currency', by_currency, name='by_currency'),
    path('by_branches', by_branches, name='by_branches'),
    path('by_industry', by_industry, name='by_industry'),
    path('by_sphere', by_sphere, name='by_sphere'),
    path('by_products', by_products, name='by_products'),
    path('by_percents/<str:sts>/', by_percents, name='by_percents'),
    path('by_averages/<str:sts>/', by_averages, name='by_averages'),
    path('issued_overdues/', issued_overdues, name='issued_overdues'),
    path('export_doklad_excel/', export_all_tables, name='export_doklad_word'),
    path('export_doklad_word/', export_all_docx, name='export_doklad_excel'),
    path('test', user_check),

    # generate
    path('generate_word', GenerateWord.as_view(), name='generate_word_url')
]