from django.shortcuts import render
from rest_framework.response import Response
# from .models import Company, Stock, ProsReview, ProsWord, ConsReview, ConsWord, News
from rest_framework.views import APIView 
from django.http import JsonResponse, HttpResponse
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction
from drf_yasg import openapi
import json
from rest_framework import status

# class CompanyInfoAPI(APIView):
#     company_name = openapi.Parameter('company_name', openapi.IN_QUERY, description='company_name', required=True, type=openapi.TYPE_STRING)
#     @swagger_auto_schema(operation_description="회사 정보 API", manual_parameters=[company_name], tags=['메인_회사정보'], reponses={200: 'Success'})
#     def get(self, request):
#         company_insert_name = request.GET.get('company_name')

#         if not company_insert_name:
#             return JsonResponse({"message": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             company_result = Company.objects.get(company_name=company_insert_name)
#             company_id = company_result.company_id
            
#             stock_result = Stock.objects.filter(company_id=company_id)
#             stock_info = {
#                 "transaction_date": [],
#                 "closing_price": [],
#             }
#             for i in stock_result:
#                 stock_info["transaction_date"].append(i.transaction_date)
#                 stock_info["closing_price"].append(i.closing_price)
            
#             mood_words = {}

#             pros_reviews = ProsReview.objects.filter(company_id=company_id)
#             for pros in pros_reviews:
#                 for i in ProsWord.objects.filter(pros_id=pros.pros_id):
#                     if i.word_text in mood_words:
#                         mood_words[i.word_text][1] += 1
#                     else:
#                         mood_words[i.word_text] = [True, 0]

#             cons_reviews = ConsReview.objects.filter(company_id=company_id)
#             for cons in cons_reviews:
#                 for i in ConsWord.objects.filter(cons_id=cons.cons_id):
#                     if i.word_text in mood_words:
#                         mood_words[i.word_text][1] += 1
#                     else:
#                         mood_words[i.word_text] = [False, 0]
            
#             news_result = News.objects.filter(company_id=company_id)
#             company_news = []
#             for news in news_result:
#                 company_news.append({news.news_id : {
#                     "news_title" : news.news_title,
#                     "news_text" : news.news_text
#                 }})
            
#             company_info = {
#                 "stock_info" : stock_info,
#                 "company": {
#                     "company_name": company_result.company_name,
#                     "company_size": company_result.company_size,
#                     "company_introduction": company_result.company_introduction,
#                 },
#                 "mood_words": mood_words,
#                 "company_news": company_news
#             }
            
#             return JsonResponse({'data': company_info}, json_dumps_params={'ensure_ascii': False}, status=status.HTTP_200_OK)
#         except Company.DoesNotExist:
#             return JsonResponse({"message": "등록된 기업 정보가 없습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# def company_index(request):
#     return render(request, 'Company/company_index.html', {
#         'company_detail': 'Company/company_detail.html',
#         'company_recruit': 'Company/company_recruit.html'
#     })

from django.shortcuts import get_object_or_404
def index(request, company_name):
    print(company_name)
    company = get_object_or_404(Company, company_name=company_name)
    return render(request, 'Company/company_index.html', {
        'company_detail': 'Company/company_detail.html',
        'company_recruit': 'Company/company_recruit.html',
        'company_info': company
    })
