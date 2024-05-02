from django.core.management.base import BaseCommand
import pandas as pd
from ETF.mapper.preprocessor import LoadPreprocessor
from ETF.mapper.loader import DataLoader
from ETF.mapper.constants import *

class Command(BaseCommand):
    help = 'Loads data into the system.'

    def handle(self, *args, **options):
        preprocessor = LoadPreprocessor()
        etf_products_df = preprocessor.add_domain_id_from_name(etf_list)

        loader = DataLoader()
        num_input, num_created, num_updated = loader.load_etf_product_from_df(etf_products_df)

        self.stdout.write(self.style.SUCCESS(f"Number of ETF Product input: {num_input}, Number of ETF Product created: {num_created}, Number of ETF Product updated: {num_updated}"))
