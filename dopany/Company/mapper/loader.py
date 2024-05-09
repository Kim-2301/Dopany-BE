from ETF.models import Company
from ETF.models import Industry

from utils.decorator import singleton


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