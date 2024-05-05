from django.core.management.base import BaseCommand
import pandas as pd
from ETF.mapper.preprocessor import LoadPreprocessor
from ETF.mapper.loader import DataLoader
from ETF.mapper.constants import *

class Command(BaseCommand):
    help = 'Loads data into the system.'

    def handle(self, *args, **options):
        loader = DataLoader()
        domains_df = pd.DataFrame(domain_list)
        
        num_input, num_created, num_updated = loader.load_domain_from_df(domains_df)
        self.stdout.write(self.style.SUCCESS(f"Number of domains input: {num_input}, Number of domains created: {num_created}, Number of domains updated: {num_updated}"))
