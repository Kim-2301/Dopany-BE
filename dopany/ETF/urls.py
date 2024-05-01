from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('', CompanyInfoView.as_view(), name='api_3'),
]