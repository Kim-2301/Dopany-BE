from django.core.management.base import BaseCommand
import pandas as pd
from Company.mapper.preprocessor import LoadPreprocessor
from Company.mapper.loader import DataLoader
from Company.mapper.converter import Converter

class Command(BaseCommand):
    help = 'Loads data into the system.'

    def handle(self, *args, **options):
        converter = Converter()
        reviews_df_list = converter.convert_reviews_csv_to_df('Company/mapper/initial_data/reviews/pros')
        reviews_df = pd.concat(reviews_df_list)

        loader = DataLoader()
        num_input = loader.load_pros_review_from_df(reviews_df)

        self.stdout.write(self.style.SUCCESS(f"Number of Pros Reviews input: {num_input}"))
