from ETF.models import Industry
from Company.models import *
from django.db.models import Q
from django.db import transaction

from utils.decorator import singleton
import pandas as pd
import re
from datetime import datetime

@singleton
class DataLoader:

    def load_company_from_df(self, companies_df):
        company_list = companies_df.to_dict('records')
        existing_companies = Company.objects.in_bulk(list(companies_df['company_name']), field_name='company_name')
        existing_company_names = set(existing_companies.keys())

        to_update = []
        new_companies = []

        for company_data in company_list:
            company_name = company_data['company_name']
            industry_name = company_data.pop('industry_name', None)
            company_data = {k: v for k, v in company_data.items() if k in [field.name for field in Company._meta.get_fields()]}

            try:
                industry = Industry.objects.get(industry_name=industry_name)
            except Industry.DoesNotExist:
                raise Industry.DoesNotExist(f"The industry '{industry_name}' does not exist in the database.")

            if company_name in existing_company_names:
                company = existing_companies[company_name]
                if not company.industries.filter(industry_name=industry_name).exists():
                    company.industries.add(industry)
                    to_update.append(company)
            elif company_name not in [c.company_name for c in new_companies]:
                new_companies.append(Company(**company_data))

        # Bulk create new companies
        created_companies = Company.objects.bulk_create(new_companies)
        
        # After creation, map companies to industries
        for company in created_companies:
            company.industries.add(industry)
            print(industry_name)

        for company in created_companies:
            company.industries.add(industry)
            print(f"New company {company.company_name} added with industry {industry_name}")

        return len(company_list), len(new_companies), len(to_update)
    

    def load_stock_from_df(self, stock_df):

        stock_df = stock_df[['company_id', 'transaction_date', 'closing_price', 'trading_volume', 'change']]

        company_ids = stock_df['company_id'].unique()
        companys = Company.objects.filter(company_id__in=company_ids).in_bulk(field_name='company_id')

        stock_list = stock_df.to_dict('records')

        existing_stock = Stock.objects.filter(
            Q(transaction_date__in=stock_df['transaction_date'].tolist()) &
            Q(company_id__in=company_ids)
        )

        date_str_format = '%Y-%m-%d'
        existing_stock = {(ep.transaction_date.strftime(date_str_format), ep.company_id): ep for ep in existing_stock}

        to_update = []
        to_create = {}

        for stock_data in stock_list:
            key = (stock_data['transaction_date'], stock_data['company_id'])
            if key in existing_stock:
                stock = existing_stock[key]
                for key, value in stock_data.items():
                    setattr(stock, key, value)
                to_update.append(stock)
            elif key not in to_create:
                company = companys.get(stock_data['company_id'])
                if company:
                    stock_data['company'] = company
                    del stock_data['company_id']
                    to_create[key] = Stock(**stock_data)

        # Convert dictionary values to list for bulk_create
        unique_to_create = list(to_create.values())
        # print(to_create.keys())

        with transaction.atomic():
            if unique_to_create:
                Stock.objects.bulk_create(unique_to_create)
            if to_update:
                Stock.objects.bulk_update(to_update, ['closing_price', 'trading_volume', 'change'])

        return len(stock_list), len(unique_to_create), len(to_update)
    
    from django.db.models import Q


    def load_recruitment_from_df(self, recruitments_df):
        # 기존 레코드 식별
        existing_recruitments_dict = {rec.recruitment_title: rec for rec in Recruitment.objects.filter(
            recruitment_title__in=recruitments_df['recruitment_title'].tolist()
        )}

        new_recruitments = []
        update_recruitments = []

        job_mapping = {job.job_name: job for job in Job.objects.all()}
        skill_mapping = {skill.skill_name: skill for skill in Skill.objects.all()}

        current_year = datetime.now().year
        for _, row in recruitments_df.iterrows():
            match = re.search(r'(\d{2})/(\d{2})', row['due_date'])
            if match:
                date_formatted = f"{current_year}-{match.group(1)}-{match.group(2)}"
                # datetime 객체로 변환 (연도는 기본값으로 현재 연도 사용)
                date_obj = pd.to_datetime(date_formatted, format='%Y-%m-%d', errors='coerce')
                if pd.notna(date_obj):
                    # PostgreSQL datetime 포맷으로 변환 ('YYYY-MM-DD')
                    due_date = date_obj.strftime('%Y-%m-%d')
            else:
                due_date = None  # 파싱 실패 시 None 반환

            recruitment = existing_recruitments_dict.get(row['recruitment_title'])
            if recruitment:
                # 업데이트할 객체에 기존 기본 키 할당
                recruitment.url = row['url']
                recruitment.career = row['career']
                recruitment.education = row['education']
                recruitment.due_date=due_date
                update_recruitments.append(recruitment)
            else:
                recruitment = Recruitment(
                    recruitment_title=row['recruitment_title'],
                    url=row['url'],
                    career=row['career'],
                    education=row['education'],
                    due_date=due_date,
                )
                new_recruitments.append(recruitment)

        # 신규 레코드 일괄 삽입
        created_recruitments = Recruitment.objects.bulk_create(new_recruitments)

        # 기존 레코드 업데이트
        if update_recruitments:
            Recruitment.objects.bulk_update(
                update_recruitments, ['url', 'career', 'education', 'due_date']
            )

        # 모든 레코드 병합 (신규 + 업데이트)하여 관계 업데이트
        all_recruitments = created_recruitments + update_recruitments

        for recruitment, row in zip(all_recruitments, recruitments_df.itertuples(index=False)):
            jobs_to_add = [
                job_mapping[name.strip()]
                for name in row.jobs.split(',')
                if name.strip() in job_mapping
            ]
            skills_to_add = [
                skill_mapping[name.strip()]
                for name in row.skills.split(',')
                if name.strip() in skill_mapping
            ]

            recruitment.jobs.set(jobs_to_add)
            recruitment.skills.set(skills_to_add)

        return len(recruitments_df), len(new_recruitments), len(update_recruitments)
    

    def load_news_from_df(self, news_df):
        news_df['posted_at'] = pd.to_datetime(news_df['posted_at'], errors='coerce')

        news_objects = []

        # Assuming Company names are unique and already exist in the database
        company_mapping = {company.name: company for company in Company.objects.all()}

        for _, row in news_df.iterrows():
            company = company_mapping.get(row['company_name'])  # Get the Company instance from the mapping

            # Create a Recruitment instance for each row
            news = News(
                news_title=row['news_title'],
                news_url=row['news_url'],
                posted_at=row['posted_at'],
                news_text=row['news_text'],
                company=company  # Assign the foreign key relationship
            )
            news_objects.append(news)

        # Use transaction to ensure all or nothing is saved
        with transaction.atomic():
            # Bulk create all Recruitment instances
            News.objects.bulk_create(news_objects)

        return len(news_df)
    

    def load_job_from_df(self, jobs_df):
        jobs_df = jobs_df[['job_name']]

        jobs_list = jobs_df.to_dict('records')

        existing_jobs = Job.objects.in_bulk(field_name='job_name')
        existing_job_names = existing_jobs.keys()

        to_update = []
        to_create = []

        for job_data in jobs_list:
            job_name = job_data['job_name']
            if job_name in existing_job_names:
                job = existing_jobs[job_name]
                job.job_name = job_name
                to_update.append(job)
            else:
                to_create.append(Job(**job_data))

        with transaction.atomic():
            if to_create:
                Job.objects.bulk_create(to_create)
            if to_update:
                Job.objects.bulk_update(to_update, ['job_name'])

        return len(jobs_list), len(to_create), len(to_update)


    def load_skill_from_df(self, skills_df):
        skills_df = skills_df[['skill_name']]

        skills_list = skills_df.to_dict('records')

        existing_skills = Skill.objects.in_bulk(field_name='skill_name')
        existing_skill_names = existing_skills.keys()

        to_update = []
        to_create = []

        for skill_data in skills_list:
            skill_name = skill_data['skill_name']
            if skill_name in existing_skill_names:
                skill = existing_skills[skill_name]
                skill.skill_name = skill_name
                to_update.append(skill)
            else:
                to_create.append(Skill(**skill_data))

        with transaction.atomic():
            if to_create:
                Skill.objects.bulk_create(to_create)
            if to_update:
                Skill.objects.bulk_update(to_update, ['skill_name'])

        return len(skills_list), len(to_create), len(to_update)
