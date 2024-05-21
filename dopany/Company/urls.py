# from django.urls import path
# from Company.views import CompanyInfoAPI

# urlpatterns = [
#     path('', CompanyInfoAPI.as_view()),
# ]

from django.urls import path
from Company.views import CompanyInfoAPI, RecruitmentView
from . import views

urlpatterns = [
    path('' ,CompanyInfoAPI.as_view(), name='api_4'),
    path('recruitment',RecruitmentView.as_view(), name='api_5'),
    # path('company/', views.index, name='company'),
    path('<str:company_name>/', views.index, name='company'),
]
