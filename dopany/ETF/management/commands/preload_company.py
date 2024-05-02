from django.core.management.base import BaseCommand
import pandas as pd
from ETF.mapper.preprocessor import LoadPreprocessor
from ETF.mapper.loader import DataLoader
from ETF.mapper.constants import *

class Command(BaseCommand):
    help = 'Loads data into the system.'

    def handle(self, *args, **options):
        preprocessor = LoadPreprocessor()
        companies_df = preprocessor.add_domain_id_from_name(companies_df)
        companies_df = preprocessor.add_industry_id_with_domain(companies_df)

        loader = DataLoader()
        num_input, num_created, num_updated = loader.load_company_from_df(companies_df)
        
        self.stdout.write(self.style.SUCCESS(f"Number of companies input: {num_input}, Number of companies created: {num_created}, Number of companies updated: {num_updated}"))
