from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('get_domain', DomainNameView.as_view(), name='api_1'),
    path('', views.index, name='domain'),
    path('get_ETF',ETFInfoView.as_view(), name='api_2'),
    path('get_company', CompanyInfoView.as_view(), name='api_3'),
    
]