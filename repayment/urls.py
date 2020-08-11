from django.urls import path
from . import views

urlpatterns = [
    path('top/', views.repayments_top, name='repayments_top'),
    path('all/', views.repayments_all, name='repayments_all'),
    path('by_subjects/', views.repayments_by_subjects, name='repayments_by_subjects'),
    path('by_currency/', views.repayments_by_currency, name='repayments_by_currency'),
]