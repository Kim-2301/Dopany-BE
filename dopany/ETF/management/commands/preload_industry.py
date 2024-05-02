from django.core.management.base import BaseCommand
import pandas as pd
from ETF.mapper.preprocessor import LoadPreprocessor
from ETF.mapper.loader import DataLoader
from ETF.mapper.constants import *

class Command(BaseCommand):
    help = 'Loads data into the system.'

    def handle(self, *args, **options):
        industries_df = pd.DataFrame(industry_list)
        
        preprocessor = LoadPreprocessor()
        industries_df = preprocessor.add_domain_id_from_name(industries_df)

        loader = DataLoader()
        num_input, num_created, num_updated = loader.load_industry_from_df(industries_df)

        self.stdout.write(self.style.SUCCESS(f"Number of industries input: {num_input}, Number of industries created: {num_created}, Number of industries updated: {num_updated}"))
