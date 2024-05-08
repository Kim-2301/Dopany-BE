from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import EtfPrice, EtfProduct, Domain, Company, Industry, EtfMajorCompany
from django.db.models import Avg
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from datetime import datetime, timedelta


class DomainNameView(APIView):
    @swagger_auto_schema(
        operation_description='도메인 이름 조회',
        responses={200: 'Success', 400: 'Bad Request', 500: 'Internal Server Error'},
    )
    def get(self,request):
        try:
            # 모든 domain_name 가져오기
            domain_names = Domain.objects.values_list('domain_name', flat=True)
            return Response({"domain_names": list(domain_names)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_domain_names(self):
        try:
            # 모든 domain_name 가져오기
            domain_names = Domain.objects.values_list('domain_name', flat=True)
            return list(domain_names), None
        except Exception as e:
            return [], e

class ETFInfoView(APIView):
    @swagger_auto_schema(
        operation_description='시간축 변경 요청',
        responses={200: 'Success', 400: 'Bad Request', 500: 'Internal Server Error'},
        manual_parameters=[
            openapi.Parameter('domain-name', openapi.IN_QUERY, description='Domain name', type=openapi.TYPE_STRING),
            openapi.Parameter('time-unit', openapi.IN_QUERY, description='Time unit (day, week, month)', type=openapi.TYPE_STRING),
        ],
    )
    def get(self, request):
        try:
            # request에서 domain_name과 time_unit get
            domain_name = request.GET.get('domain-name', 'IT').strip()   # default는 IT
            time_unit = request.GET.get('time-unit', 'day').strip()      # default는 day

            # domain_name에 속하는 Etf정보 get
            domain = Domain.objects.get(domain_name=domain_name)

            etf_products = EtfProduct.objects.filter(domain=domain)

            etf_info = []

            for etf_product in etf_products:
                # 해당 ETF의 모든 거래 정보 가져오기
                etf_prices = EtfPrice.objects.filter(etf_product=etf_product)
                
                transaction_dates = []
                closing_prices = []

                for etf_price in etf_prices:
                    transaction_dates.append(etf_price.transaction_date.strftime('%Y-%m-%d'))
                    closing_prices.append(etf_price.closing_price)
                    major_companies = EtfMajorCompany.objects.filter(etf_product=etf_product).values_list('company_name', flat=True)
                    
                if time_unit == 'week':
                    # 주 단위의 평균을 구함
                    etf_avg = etf_prices.extra({'week': "EXTRACT(week FROM transaction_date)"}).values('week').annotate(closing_avg=Avg('closing_price')).order_by('week')
                    # 주의 시작일로 변환하여 date 키에 추가
                    for item in etf_avg:
                        week_number = int(item['week'])
                        # 현재 날짜를 기준으로 주의 시작일 계산
                        week_start_date = (datetime.now() - timedelta(days=datetime.now().weekday(), weeks=week_number - 1)).strftime('%Y-%m-%d')
                        item['date'] = week_start_date
                    # 기존의 week 키를 삭제
                    for item in etf_avg:
                        del item['week']
                elif time_unit == 'month':
                    # 월 단위의 평균을 구함
                    etf_avg = etf_prices.extra({'month': "EXTRACT(month FROM transaction_date)"}).values('month').annotate(closing_avg=Avg('closing_price')).order_by('month')
                    # 월의 시작일로 변환하여 date 키에 추가
                    for item in etf_avg:
                        month_number = int(item['month'])
                        # 현재 날짜를 기준으로 월의 시작일 계산
                        month_start_date = datetime(datetime.now().year, month_number, 1).strftime('%Y-%m-%d')
                        item['date'] = month_start_date
                    # 기존의 month 키를 삭제
                    for item in etf_avg:
                        del item['month']
                else:
                    etf_avg = None

                
                
                    
                # ETF 정보를 딕셔너리로 저장하고 리스트에 추가
                etf_info.append({
                    "etf_name": etf_product.etf_product_name,
                    "etf_major_company": list(major_companies),
                    "transaction_date": transaction_dates,
                    "closing_price": closing_prices,
                    "closing_prices_avg" : etf_avg
                })
                

            response_data = {
                "etf_info": etf_info,
                "time_unit": time_unit,
            }
            
            return Response(response_data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({"message": "해당 시간축에 대한 지표 정보를 불러오는 데 실패했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
            domain_name = request.GET.get('domain-name','IT').strip()

            domain= Domain.objects.get(domain_name=domain_name)

            industries = Industry.objects.filter(domains=domain)
 
            domain_companies_info = []
            
            for industry in industries:
                companies = Company.objects.filter(industries=industry)
                company_info_list = []
                
                for company in companies:
                    company_info_list.append({
                        "company_name": company.company_name,
                        "company_size": company.company_size,
                        "company_sales": company.company_sales,
                        "company_img_url" : company.company_img_url,
                        "industry_name": industry.industry_name,
                    })
                
                domain_companies_info.extend(company_info_list)
            
            response_data = {
                "domain_companies_info": domain_companies_info
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except ObjectDoesNotExist:
            return Response({"message": "해당 도메인에 속한 기업 정보를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def index(request):
    domain_view = DomainNameView()
    domains, _ = domain_view.get_domain_names()  # Retrieve domains internally

    return render(request, 'ETF/domain_index.html', {
        'etf_container': 'ETF/etf_container.html',
        'company_container': 'ETF/company_container.html',
        'domains': domains
    })
