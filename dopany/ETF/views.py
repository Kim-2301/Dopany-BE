from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Domain, Company, Industry
from django.core.exceptions import ObjectDoesNotExist

class CompanyInfoView(APIView):
    @swagger_auto_schema(
        operation_description='도메인에 속한 기업 정보 조회',
        responses={200: 'Success', 400: 'Bad Request', 500: 'Internal Server Error'},
        manual_parameters=[
            openapi.Parameter('domain-name', openapi.IN_QUERY, description='Domain name', type=openapi.TYPE_STRING),
        ],
    )
    def get(self, request):
        try:
            # request에서 domain_name get
            domain_name = request.GET.get('domain-name','IT')
            
            # domain_name에 해당하는 industry 조회
            industry = Industry.objects.get(domain_name=domain_name)
            
            # 해당 industry에 속하는 모든 기업 정보 조회
            companies = Company.objects.filter(industry=industry)
            
            # 기업 정보를 리스트로 만들기
            domain_companies_info = []
            for company in companies:
                domain_companies_info.append({
                    "company_name": company.company_name,
                    "company_size": company.company_size,
                    "company_sales": company.company_sales,
                    "industry_name": industry.industry_name,
                })
            
            response_data = {
                "domain_companies_info": domain_companies_info
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except ObjectDoesNotExist:
            return Response({"message": "해당 도메인에 속한 기업 정보를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
