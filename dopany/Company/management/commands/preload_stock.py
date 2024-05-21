from django.core.management.base import BaseCommand
import pandas as pd
from Company.mapper.preprocessor import LoadPreprocessor
from Company.mapper.loader import DataLoader
from Company.mapper.converter import Converter

class Command(BaseCommand):
    help = 'Loads data into the system.'

    def handle(self, *args, **options):
        converter = Converter()
        stocks_df_list = converter.convert_stocks_csv_to_df('Company/mapper/initial_data/stocks')
        stocks_df = pd.concat(stocks_df_list)

        preprocessor = LoadPreprocessor()
        stocks_df = preprocessor.add_company_id_from_name(stocks_df)

        loader = DataLoader()
        num_input, num_created, num_updated = loader.load_stock_from_df(stocks_df)

        self.stdout.write(self.style.SUCCESS(f"Number of Stock input: {num_input}, Number of Stock created: {num_created}, Number of Stock updated: {num_updated}"))
