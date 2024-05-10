from django.core.management.base import BaseCommand
from Company.mapper.converter import Converter
from Company.mapper.loader import DataLoader

class Command(BaseCommand):
    help = 'Loads data into the system.'

    def handle(self, *args, **options):
        converter = Converter()
        # news_df = converter.convert_csv_to_df('Company/mapper/initial_data/recruitments.csv')

        loader = DataLoader()
        num_input = loader.load_news_from_df(news_df)
        
        self.stdout.write(self.style.SUCCESS(f"Number of News input: {num_input}, Number of News created: {num_input}"))
