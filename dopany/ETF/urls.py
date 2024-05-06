from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('get_domain', ETFInfoView.as_view(), name='api_1'),
    path('domain-index/', views.index, name='domain-index'),
    path('',ETFInfoView.as_view(), name='api_2'),
    path('', CompanyInfoView.as_view(), name='api_3'),
    
]