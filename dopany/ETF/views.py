from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import EtfPrice, EtfProduct, Domain, EtfMajorCompany
from django.db.models import Avg
from django.core.exceptions import ObjectDoesNotExist
import logging

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
            domain_name = request.GET.get('domain-name', 'IT')   # default는 IT
            time_unit = request.GET.get('time-unit', 'day')      # default는 day
            
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
                    etf_avg = etf_prices.extra({'week': "EXTRACT(week FROM transaction_date)"}).values('week').annotate(time_avg=Avg('closing_price')).order_by('week')
                elif time_unit == 'month':
                    etf_avg = etf_prices.extra({'month': "EXTRACT(month FROM transaction_date)"}).values('month').annotate(time_avg=Avg('closing_price')).order_by('month')
                else:
                    etf_avg = None
                    
                # ETF 정보를 딕셔너리로 저장하고 리스트에 추가
                etf_info.append({
                    "etf_name": etf_product.etf_product_name,
                    "etf_major_company": list(major_companies),
                    "transaction_dates": transaction_dates,
                    "closing_prices": closing_prices,
                    "time_avg" : etf_avg
                })
                

            response_data = {
                "etf_info": etf_info,
                "time_unit": time_unit,
            }
            
            return Response(response_data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({"message": "해당 시간축에 대한 지표 정보를 불러오는 데 실패했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message": "존재하지 않는 데이터입니다."}, status=status.HTTP_400_BAD_REQUEST)
