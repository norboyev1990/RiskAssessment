from django.urls import path
from . import views

urlpatterns = [
    path('credits/', views.credits, name='upload_credits'),
    path('issuances/', views.issuances, name='upload_issuances'),
    path('success/', views.success, name='upload_success')
]