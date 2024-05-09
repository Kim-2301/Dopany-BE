from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('get_domain', DomainNameView.as_view(), name='api_1'),
    path('domain-index/', views.index, name='domain-index'),
    # path('company_index/', views.company_index, name='company_index'),
    path('company_index/<str:company_name>/', views.company_index, name='company_index'),
    path('get_ETF',ETFInfoView.as_view(), name='api_2'),
    path('get_company', CompanyInfoView.as_view(), name='api_3'),
    
]