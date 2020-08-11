from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload, name='issuance_upload'),
    path('success/', views.success, name='issuance_success')
]