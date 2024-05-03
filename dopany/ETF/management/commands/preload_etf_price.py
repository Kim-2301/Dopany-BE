from django.core.management.base import BaseCommand
import pandas as pd
from ETF.mapper.preprocessor import LoadPreprocessor
from ETF.mapper.loader import DataLoader
from ETF.mapper.constants import *
from ETF.mapper.converter import Converter

class Command(BaseCommand):
    help = 'Loads data into the system.'

    def handle(self, *args, **options):
        converter = Converter()
        etf_prices_df_list = converter.convert_etfs_csv_to_df('ETF/mapper/initial_data/etfs')
        etf_prices_df = pd.concat(etf_prices_df_list)

        preprocessor = LoadPreprocessor()
        etf_prices_df = preprocessor.add_etf_product_id_from_name(etf_prices_df)

        loader = DataLoader()
        num_input, num_created, num_updated = loader.load_etf_price_from_df(etf_prices_df)

        self.stdout.write(self.style.SUCCESS(f"Number of ETF Price input: {num_input}, Number of ETF Price created: {num_created}, Number of ETF Price updated: {num_updated}"))
