from django.core.management.base import BaseCommand
from Company.mapper.converter import Converter
from Company.mapper.loader import DataLoader
import pandas as pd

class Command(BaseCommand):
    help = 'Loads data into the system.'

    def handle(self, *args, **options):
        converter = Converter()
        news_df_list = converter.convert_news_csv_to_df('Company/mapper/initial_data/news')
        news_df = pd.concat(news_df_list)

        loader = DataLoader()
        num_input = loader.load_news_from_df(news_df)
        
        self.stdout.write(self.style.SUCCESS(f"Number of News input: {num_input}, Number of News created: {num_input}"))
