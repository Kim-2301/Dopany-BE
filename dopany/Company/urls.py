# from django.urls import path
# from Company.views import CompanyInfoAPI

# urlpatterns = [
#     path('', CompanyInfoAPI.as_view()),
# ]

from django.urls import path
from Company.views import CompanyInfoAPI
from . import views

urlpatterns = [
    path('' ,CompanyInfoAPI.as_view()),
    # path('company/', views.index, name='company'),
    path('company/<str:company_name>/', views.index, name='company'),
]
