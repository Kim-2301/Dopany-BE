import pandas as pd
from datetime import datetime
from django.db import transaction
from ETF.models import *
from django.db.models import F
from django.db import transaction

from ETF.utils.decorator import singleton


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
        industry_list = industries_df.to_dict('records')
        existing_industries = Industry.objects.in_bulk(field_name='industry_name')
        existing_industry_names = existing_industries.keys()

        to_update = []
        to_create = []

        for industry_data in industry_list:
            industry_name = industry_data['industry_name']
            if industry_name in existing_industry_names:
                industry = existing_industries[industry_name]
                for key, value in industry_data.items():
                    setattr(industry, key, value)
                to_update.append(industry)
            else:
                to_create.append(Industry(**industry_data))

        with transaction.atomic():
            if to_create:
                Industry.objects.bulk_create(to_create)
            if to_update:
                Industry.objects.bulk_update(to_update, ['domain_id'])

        return len(industry_list), len(to_create), len(to_update)
    
    # def load_company_from_df(self, companies_df):
    #     company_list = companies_df.to_dict('records')
    #     existing_companies = Company.objects.in_bulk(field_name='company_name')
    #     existing_company_names = existing_companies.keys()

    #     to_update = []
    #     to_create = []

    #     for company_data in company_list:
    #         company_name = company_data['company_name']
    #         if company_name in existing_company_names:
    #             company = existing_companies[company_name]
    #             for key, value in company_data.items():
    #                 setattr(company, key, value)
    #             to_update.append(company)
    #         else:
    #             to_create.append(Company(**company_data))

    #     with transaction.atomic():
    #         if to_create:
    #             Company.objects.bulk_create(to_create)
    #         if to_update:
    #             Company.objects.bulk_update(to_update, ['company_name', 'company_size', 'company_introduction', 
    #                                                     'company_sales', 'company_url', 'company_img_url', 'industry_id'])

    #     return len(company_list), len(to_create), len(to_update)

    def load_company_from_df(self, companies_df):
        """
        Inserts new and updates existing Company records from a DataFrame.

        Parameters:
        - company_df (DataFrame): DataFrame with company data.

        Assumes company_df columns include:
        - company_name (unique)
        - company_size
        - company_introduction
        - company_sales
        - company_url
        - company_img_url
        - industry_id (already mapped)
        """
        existing_companies = Company.objects.in_bulk(field_name='company_name')
        existing_company_names = existing_companies.keys()

        to_create = []
        to_update = []

        for _, row in companies_df.iterrows():
            company_name = row['company_name']
            company_data = {
                'company_name': company_name,
                'company_size': row['company_size'],
                'company_introduction': row['company_introduction'],
                'company_sales': row['company_sales'],
                'company_url': row['company_url'],
                'company_img_url': row['company_img_url'],
                'industry_id': row['industry_id']
            }
            if company_name in existing_company_names:
                company = existing_companies[company_name]
                for key, value in company_data.items():
                    setattr(company, key, value)
                to_update.append(company)
            else:
                to_create.append(Company(**company_data))

        with transaction.atomic():
            if to_create:
                Company.objects.bulk_create(to_create)
            if to_update:
                # Specify the fields to be updated to avoid updating unchanged fields
                Company.objects.bulk_update(to_update, ['company_size', 'company_introduction', 'company_sales', 'company_url', 'company_img_url', 'industry_id'])

        return len(to_create), len(to_update)


    def load_etf_product_from_df(self, etf_products_df):
        etf_product_list = etf_products_df.to_dict('records')
        existing_etf_products = EtfProduct.objects.in_bulk(field_name='etf_product_name')
        existing_etf_product_names = existing_etf_products.keys()

        to_update = []
        to_create = []

        for etf_product_data in etf_product_list:
            etf_product_name = etf_product_data['etf_product_name']
            if etf_product_name in existing_etf_product_names:
                etf_product = existing_etf_products[etf_product_name]
                for key, value in etf_product_data.items():
                    setattr(etf_product, key, value)
                to_update.append(etf_product)
            else:
                to_create.append(EtfProduct(**etf_product_data))

        with transaction.atomic():
            if to_create:
                EtfProduct.objects.bulk_create(to_create)
            if to_update:
                EtfProduct.objects.bulk_update(to_update, ['domain_id'])

        return len(etf_product_list), len(to_create), len(to_update)

    def load_etf_price_from_df(self, etf_prices_df):
        etf_price_list = etf_prices_df.to_dict('records')
        # Assuming we can identify EtfPrice records uniquely by a combination of `transaction_date` and `etf_product_id`
        existing_etf_prices = { (ep.transaction_date, ep.etf_product_id): ep for ep in EtfPrice.objects.all() }

        to_update = []
        to_create = []

        for etf_price_data in etf_price_list:
            key = (etf_price_data['transaction_date'], etf_price_data['etf_product_id'])
            if key in existing_etf_prices:
                etf_price = existing_etf_prices[key]
                for key, value in etf_price_data.items():
                    setattr(etf_price, key, value)
                to_update.append(etf_price)
            else:
                to_create.append(EtfPrice(**etf_price_data))

        with transaction.atomic():
            if to_create:
                EtfPrice.objects.bulk_create(to_create)
            if to_update:
                EtfPrice.objects.bulk_update(to_update, ['closing_price', 'trading_volume', 'change'])

        return len(etf_price_list), len(to_create), len(to_update)
    
    def load_etf_major_company_from_df(self, etf_major_companies_df):
        # Check for required columns
        required_columns = {'etf_product_id', 'company_name'}
        if not required_columns.issubset(etf_major_companies_df.columns):
            missing_cols = required_columns - set(etf_major_companies_df.columns)
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")

        etf_major_company_list = etf_major_companies_df.to_dict('records')
        existing_etf_major_companies = { (emc.etf_product_id, emc.company_name): emc for emc in EtfMajorCompany.objects.all() }

        to_update = []
        to_create = []

        for etf_major_company_data in etf_major_company_list:
            key = (etf_major_company_data['etf_product_id'], etf_major_company_data['company_name'])
            if key in existing_etf_major_companies:
                etf_major_company = existing_etf_major_companies[key]
                for key, value in etf_major_company_data.items():
                    setattr(etf_major_company, key, value)
                to_update.append(etf_major_company)
            else:
                to_create.append(EtfMajorCompany(**etf_major_company_data))

        with transaction.atomic():
            if to_create:
                EtfMajorCompany.objects.bulk_create(to_create)
            if to_update:
                EtfMajorCompany.objects.bulk_update(to_update, ['company_name'])

        return len(etf_major_company_list), len(to_create), len(to_update)
