from django.urls import path
from . import views

urlpatterns = [
    path('general_analytics', views.general_analytics, name='general_analytics'),
    path('diagramm_by_months', views.line_chart_portfolio, name='line_chart_portfolio'),
    path('distributions_by_regions', views.vector_map_portfolio, name='vector_map_portfolio'),
    path('risk_appetita', views.risk_appetita, name='risk_appetita'),
]