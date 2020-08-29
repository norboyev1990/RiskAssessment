from django.urls import path
from . import views

urlpatterns = [
    path('credits/', views.credits, name='upload_credits'),
    path('repayment/', views.repayment, name='upload_repayment'),
    path('issuances/', views.issuances, name='upload_issuances'),
    path('overdues/', views.overdues, name='upload_overdues'),
    path('success/', views.success, name='upload_success')
]