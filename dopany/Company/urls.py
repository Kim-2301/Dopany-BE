# from django.urls import path
# from Company.views import CompanyInfoAPI

# urlpatterns = [
#     path('', CompanyInfoAPI.as_view()),
# ]

from django.urls import path
from .views import CompanyInfoAPI, RecruitmentView

urlpatterns = [
    path('' ,CompanyInfoAPI.as_view()),
    path('recruitment',RecruitmentView.as_view(), name='api_5')
]
