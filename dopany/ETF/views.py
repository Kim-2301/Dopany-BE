from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import Domain


class DomainNameView(APIView):
    @swagger_auto_schema(
        operation_description='도메인 이름 조회',
        responses={200: 'Success', 400: 'Bad Request', 500: 'Internal Server Error'},
    )
    def get(self):
        try:
            # 모든 domain_name 가져오기
            domain_names = Domain.objects.values_list('domain_name', flat=True)
            
            return Response({"domain_names": list(domain_names)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
