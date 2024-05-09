from django.db import transaction
from ETF.models import *
from django.db.models import Q
from django.db import transaction

from utils.decorator import singleton


@singleton
class DataLoader:

    def load_domain_from_df(self, domains_df):
        # Convert DataFrame to list of dictionaries
        domain_list = domains_df.to_dict('records')

        # Fetch existing domains from the database for comparison
        existing_domains = Domain.objects.in_bulk(field_name='domain_name')
        existing_domain_names = existing_domains.keys()

        to_update = []
        to_create = []

        # Separate into update and create lists
        for domain_data in domain_list:
            domain_name = domain_data['domain_name']
            if domain_name in existing_domain_names:
                domain = existing_domains[domain_name]
                domain.domain_name = domain_name  # Example of setting updatable fields
                to_update.append(domain)
            else:
                to_create.append(Domain(**domain_data))

        # Using Django's bulk_create and bulk_update methods
        with transaction.atomic():  # Ensuring atomic transaction
            if to_create:
                Domain.objects.bulk_create(to_create)
            if to_update:
                Domain.objects.bulk_update(to_update, ['domain_name'])

        return len(domain_list), len(to_create), len(to_update)  # Return counts of created and updated records for reference
    

    def load_industry_from_df(self, industries_df):
        industries_df = industries_df[['domain_id', 'industry_name']]

        domain_ids = industries_df['domain_id'].unique()
        domains = Domain.objects.filter(domain_id__in=domain_ids).in_bulk(field_name='domain_id')

        existing_industries = Industry.objects.filter(
            industry_name__in=industries_df['industry_name'].tolist()
        ).prefetch_related('domains')
        existing_industry_map = {industry.industry_name: industry for industry in existing_industries}

        to_update = []
        to_create = {}

        with transaction.atomic():  # 시작하는 트랜잭션을 함수 전체로 확장
            for industry_data in industries_df.to_dict('records'):
                industry_name = industry_data['industry_name']
                domain_id = industry_data['domain_id']
                domain = domains.get(domain_id)
                if not domain:
                    continue  # Skip if no matching domain

                industry = existing_industry_map.get(industry_name)
                if industry:
                    industry = existing_industry_map[industry_name]
                    if not industry.domains.filter(domain_id=domain_id).exists():
                        industry.domains.add(domain)
                        to_update.append(industry)  # To signify that domains were updated
                elif industry_name not in to_create:
                    new_industry = Industry(industry_name=industry_name)
                    new_industry.save()  # 먼저 객체를 저장
                    new_industry.domains.add(domain)
                    to_create[industry_name] = new_industry  # 성공적으로 생성된 객체를 저장

        return len(industries_df), len(to_create), len(to_update)
    

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


    def load_etf_product_from_df(self, etf_products_df):
        etf_products_df = etf_products_df[['domain_id', 'etf_product_name']]

        domain_ids = etf_products_df['domain_id'].unique()
        domains = Domain.objects.filter(domain_id__in=domain_ids).in_bulk(field_name='domain_id')
        
        etf_product_list = etf_products_df.to_dict('records')
        existing_etf_products = EtfProduct.objects.in_bulk(field_name='etf_product_name')
        existing_etf_product_names = existing_etf_products.keys()

        to_update = []
        to_create = []

        for etf_product_data in etf_product_list:
            etf_product_name = etf_product_data['etf_product_name']
            domain_id = etf_product_data['domain_id']
            domain = domains.get(domain_id)
            if not domain:
                continue  # Skip if no matching domain

            if etf_product_name in existing_etf_product_names:
                etf_product = existing_etf_products[etf_product_name]
                etf_product.domain = domain
                for key, value in etf_product_data.items():
                    if key not in ['domain_id', 'domain_name']:  # Ignore these fields in updates
                        setattr(etf_product, key, value)
                to_update.append(etf_product)
            else:
                etf_product_data['domain'] = domain
                del etf_product_data['domain_id']  # Remove domain_id as we now have a domain object
                to_create.append(EtfProduct(**etf_product_data))

        with transaction.atomic():
            if to_create:
                EtfProduct.objects.bulk_create(to_create)
            if to_update:
                EtfProduct.objects.bulk_update(to_update, ['domain'])

        return len(etf_product_list), len(to_create), len(to_update)

    def load_etf_price_from_df(self, etf_prices_df):

        etf_prices_df = etf_prices_df[['etf_product_id', 'transaction_date', 'closing_price', 'trading_volume', 'change']]

        etf_product_ids = etf_prices_df['etf_product_id'].unique()
        etf_products = EtfProduct.objects.filter(etf_product_id__in=etf_product_ids).in_bulk(field_name='etf_product_id')

        etf_price_list = etf_prices_df.to_dict('records')

        existing_etf_prices = EtfPrice.objects.filter(
            Q(transaction_date__in=etf_prices_df['transaction_date'].tolist()) &
            Q(etf_product_id__in=etf_product_ids)
        )

        date_str_format = '%Y-%m-%d'
        existing_etf_prices = {(ep.transaction_date.strftime(date_str_format), ep.etf_product_id): ep for ep in existing_etf_prices}

        to_update = []
        to_create = {}

        for etf_price_data in etf_price_list:
            key = (etf_price_data['transaction_date'], etf_price_data['etf_product_id'])
            if key in existing_etf_prices:
                etf_price = existing_etf_prices[key]
                for key, value in etf_price_data.items():
                    setattr(etf_price, key, value)
                to_update.append(etf_price)
            elif key not in to_create:
                etf_product = etf_products.get(etf_price_data['etf_product_id'])
                if etf_product:
                    etf_price_data['etf_product'] = etf_product
                    del etf_price_data['etf_product_id']
                    to_create[key] = EtfPrice(**etf_price_data)

        # Convert dictionary values to list for bulk_create
        unique_to_create = list(to_create.values())
        print(to_create.keys())

        with transaction.atomic():
            if unique_to_create:
                EtfPrice.objects.bulk_create(unique_to_create)
            if to_update:
                EtfPrice.objects.bulk_update(to_update, ['closing_price', 'trading_volume', 'change'])

        return len(etf_price_list), len(unique_to_create), len(to_update)
    
    
    def load_etf_major_company_from_df(self, etf_major_companies_df):
        etf_major_companies_df = etf_major_companies_df[['company_name', 'etf_product_id']]

        etf_product_ids = etf_major_companies_df['etf_product_id'].unique()
        etf_products = EtfProduct.objects.filter(etf_product_id__in=etf_product_ids).in_bulk(field_name='etf_product_id')

        etf_major_company_list = etf_major_companies_df.to_dict('records')

        existing_etf_major_companies = EtfMajorCompany.objects.filter(
            Q(company_name__in=etf_major_companies_df['company_name'].tolist()) &
            Q(etf_product_id__in=etf_product_ids)
        )

        existing_etf_major_companies = {(em.company_name, em.etf_product_id): em for em in existing_etf_major_companies}

        to_update = []
        to_create = {}

        for etf_major_company_data in etf_major_company_list:
            key = (etf_major_company_data['company_name'], etf_major_company_data['etf_product_id'])
            etf_product_id = etf_major_company_data['etf_product_id']
            etf_product = etf_products.get(etf_product_id)
            if not etf_product:
                continue  # Skip if no matching domain
            
            if key in existing_etf_major_companies:
                etf_major_company = existing_etf_major_companies[key]
                etf_major_company.etf_product = etf_product
                for key, value in etf_major_company_data.items():
                    setattr(etf_major_company, key, value)
                to_update.append(etf_major_company)
            elif key not in to_create:
                etf_major_company_data['etf_product'] = etf_product
                del etf_major_company_data['etf_product_id']  # Remove domain_id as we now have a domain object
                to_create[key] = EtfMajorCompany(**etf_major_company_data)

        # Convert dictionary values to list for bulk_create
        unique_to_create = list(to_create.values())
        print(to_create.keys())

        with transaction.atomic():
            if unique_to_create:
                EtfMajorCompany.objects.bulk_create(unique_to_create)
            if to_update:
                EtfMajorCompany.objects.bulk_update(to_update, ['company_name'])

        return len(etf_major_company_list), len(unique_to_create), len(to_update)
