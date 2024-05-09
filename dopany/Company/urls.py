# from django.urls import path
# from Company.views import CompanyInfoAPI

# urlpatterns = [
#     path('', CompanyInfoAPI.as_view()),
# ]

from django.urls import path
from Company.views import CompanyInfoAPI

urlpatterns = [
    path('' ,CompanyInfoAPI.as_view()),
]
