from django.core.management.base import BaseCommand
import pandas as pd
from ETF.mapper.preprocessor import LoadPreprocessor
from ETF.mapper.loader import DataLoader
from ETF.mapper.constants import *

class Command(BaseCommand):
    help = 'Loads data into the system.'

    def handle(self, *args, **options):
        preprocessor = LoadPreprocessor()
        etf_major_companies_df = preprocessor.add_etf_product_id_from_name(etf_major_companies_df)

        loader = DataLoader()
        num_input, num_created, num_updated = loader.load_etf_major_company_from_df(etf_major_companies_df)

        self.stdout.write(self.style.SUCCESS(f"Number of domains input: {num_input}, Number of domains created: {num_created}, Number of domains updated: {num_updated}"))
