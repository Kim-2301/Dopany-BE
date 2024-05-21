from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from rest_framework.views import APIView 
from django.http import JsonResponse, HttpResponse
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from drf_yasg import openapi
import json
from rest_framework import status

class CompanyInfoAPI(APIView):
    company_name = openapi.Parameter('company_name', openapi.IN_QUERY, description='company_name', required=True, type=openapi.TYPE_STRING)
    @swagger_auto_schema(operation_description="회사 정보 API", manual_parameters=[company_name], tags=['company'], reponses={200: 'Success'})
    def get(self, request):
        company_insert_name = request.GET.get('company-name')

        if not company_insert_name:
            return JsonResponse({"message": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            company_result = Company.objects.get(company_name=company_insert_name)
            company_id = company_result.company_id
            
            stock_result = Stock.objects.filter(company_id=company_id)
            stock_info = {
                "transaction_date": [],
                "closing_price": [],
            }
            for i in stock_result:
                stock_info["transaction_date"].append(i.transaction_date)
                stock_info["closing_price"].append(i.closing_price)
            
            mood_words = {}

            pros_reviews = ProsReview.objects.filter(company=company_result)
            for pros in pros_reviews:
                for i in ProsWord.objects.filter(pros_review=pros):
                    if i.word_text in mood_words:
                        mood_words[i.word_text][1] += i.weight
                    else:
                        mood_words[i.word_text] = [True, i.weight]

            cons_reviews = ConsReview.objects.filter(company_id=company_id)
            for cons in cons_reviews:
                for i in ConsWord.objects.filter(cons_review=cons):
                    if i.word_text in mood_words:
                        mood_words[i.word_text][1] += i.weight
                    else:
                        mood_words[i.word_text] = [False, i.weight]
            
            news_result = News.objects.filter(company_id=company_id)
            company_news = []
            for news in news_result:
                company_news.append({news.news_id : {
                    "news_title" : news.news_title,
                    "news_text" : news.news_text,
                    "news_url" : news.news_url,
                    "posted_at" : news.posted_at,
                }})
            
            company_info = {
                "stock_info" : stock_info,
                "company": {
                    "company_name": company_result.company_name,
                    "company_size": company_result.company_size,
                    "company_introduction": company_result.company_introduction,
                },
                "mood_words": mood_words,
                "company_news": company_news
            }
            
            return JsonResponse({'data': company_info}, json_dumps_params={'ensure_ascii': False}, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return JsonResponse({"message": "등록된 기업 정보가 없습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RecruitmentView(APIView):
    @swagger_auto_schema(
        operation_description="회사별 채용 공고 요청",
        reponses={200: 'Success', 400: 'Bad Request', 404: 'Not Found', 500: 'Internal Server Error'},
        manual_parameters=[
            openapi.Parameter(
                'company_name',
                openapi.IN_QUERY,
                description='company_name', required=True, type=openapi.TYPE_STRING
            )
        ],
        tags=['company'],
    )
    def get(self, request):
        request_company_name = request.GET.get('company-name')
        if not request_company_name:
            return Response({"message": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            target_company = Company.objects.get(company_name=request_company_name)
            target_recruitments = Recruitment.objects.filter(company=target_company)
            if not target_recruitments.exists():
                raise Recruitment.DoesNotExist(f"{target_company.company_name}의 채용 공고가 없습니다.")

            company_recruitments = self.make_company_recruitments_nested(target_recruitments)
            return Response(
                data={"company_recruitments": company_recruitments},
                status=status.HTTP_200_OK
            )
        except Company.DoesNotExist:
            return Response(
                data={"message": "기업이 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Recruitment.DoesNotExist:
            # 채용공고 없을 시 에러메시지보다는 채용공고가 없다는 내용의 페이지를 띄우는게 더 나아보임
            return Response(
                data={"message": "기업의 채용공고가 없습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def make_company_recruitments_nested(self, recruitments):
        company_recruitments = []
        for recruitment in recruitments:
            job_names = [job.job_name for job in recruitment.jobs.all()]
            skill_names = [skill.skill_name for skill in recruitment.skills.all()]
            company_recruitments.append(
                {
                    "recruitment_title": recruitment.recruitment_title,
                    "recruitment_url": recruitment.url,
                    "career": recruitment.career,
                    "education": recruitment.education,
                    "due_date": recruitment.due_date,
                    "job_names": job_names,
                    "skill_names": skill_names
                }
            )
        return company_recruitments
    

from django.shortcuts import get_object_or_404
def index(request, company_name):
    print(company_name)
    company = get_object_or_404(Company, company_name=company_name)
    return render(request, 'Company/company_index.html', {
        'company_detail': 'Company/company_detail.html',
        'company_recruit': 'Company/company_recruit.html',
        'company_info': company
    })
