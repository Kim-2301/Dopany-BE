from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Etf, Domain, EtfMajorCompany
from django.db.models import Avg
from django.core.exceptions import ObjectDoesNotExist

class ETFInfoView(APIView):
    @swagger_auto_schema(
        operation_description='시간축 변경 요청',
        responses={200: 'Success', 400: 'Bad Request', 500: 'Internal Server Error'},
        manual_parameters=[
            openapi.Parameter('domain-name', openapi.IN_QUERY, description='Domain name', type=openapi.TYPE_STRING),
            openapi.Parameter('time-unit', openapi.IN_QUERY, description='Time unit (day, month, year)', type=openapi.TYPE_STRING),
        ],
        
    )
    def get(self, request):
        try:
            # request에서 domian_name과 time_unit get
            domain_name = request.GET.get('domain-name')
            time_unit = request.GET.get('time-unit')

            if time_unit not in ['day', 'month', 'year']:
                return Response({"message": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)

            # domain_name에 속하는 Etf정보 get
            domain = Domain.objects.get(domain_name=domain_name)
            etf_data = Etf.objects.filter(domain=domain)

            # time_unit별 closing_price 계산
            # if time_unit == 'day':
            #     etf_info = etf_data.values('transaction_date').annotate(closing_price=Avg('closing_price'))
            # elif time_unit == 'month':
            #     etf_info = etf_data.extra({'month': "EXTRACT(month FROM transaction_date)"}).values('month').annotate(closing_price=Avg('closing_price'))
            # elif time_unit == 'year':
            #     etf_info = etf_data.extra({'year': "EXTRACT(year FROM transaction_date)"}).values('year').annotate(closing_price=Avg('closing_price'))


            # etf_info에 들어갈 요소 처리
            etf_info = []
            for etf in etf_data:
                major_companies = EtfMajorCompany.objects.filter(etf_name=etf.etf_name).values_list('company_name', flat=True)
                etf_info.append({
                    "etf_name": etf.etf_name,
                    "etf_major_company": list(major_companies),
                    "transaction_date": etf.transaction_date.strftime('%Y-%m-%d'),
                    "closing_price": etf.closing_price
                })

            response_data = {
                "etf_info": etf_info,
                "time_unit": time_unit
            }
            
            return Response(response_data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({"message": "해당 시간축에 대한 지표 정보를 불러오는 데 실패했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message": "존재하지 않는 데이터입니다."}, status=status.HTTP_400_BAD_REQUEST)
