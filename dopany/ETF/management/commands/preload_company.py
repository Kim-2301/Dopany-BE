from django.core.management.base import BaseCommand
import pandas as pd
from ETF.mapper.loader import DataLoader
from ETF.mapper.constants import *
from ETF.mapper.converter import Converter

class Command(BaseCommand):
    help = 'Loads data into the system.'

    def handle(self, *args, **options):
        converter = Converter()
        companies_df_list = converter.convert_companies_csv_to_df('ETF/mapper/initial_data/companies')
        companies_df = pd.concat(companies_df_list)

        loader = DataLoader()
        num_input, num_created, num_updated = loader.load_company_from_df(companies_df)
        
        self.stdout.write(self.style.SUCCESS(f"Number of companies input: {num_input}, Number of companies created: {num_created}, Number of companies updated: {num_updated}"))
