from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('', DomainNameView.as_view(), name='api_1'),
    path('domain-index/', views.index, name='domain-index'),
]