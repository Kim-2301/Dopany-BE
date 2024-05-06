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
            
            domain= Domain.objects.get(domain_name=domain_name)
            industries = Industry.objects.filter(domains=domain)      
            domain_companies_info = []
            
            for industry in industries:
                companies = Company.objects.filter(industries=industry)
                company_names = [company.company_name for company in companies]
                
                domain_companies_info.append({
                    "industry_name": industry.industry_name,
                    "company_names": company_names,
                })
            
            response_data = {
                "domain_companies_info": domain_companies_info
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except ObjectDoesNotExist:
            return Response({"message": "해당 도메인에 속한 기업 정보를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
