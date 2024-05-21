from django.core.management.base import BaseCommand
from Company.mapper.converter import Converter
from Company.mapper.loader import DataLoader
from Company.mapper.preprocessor import LoadPreprocessor

class Command(BaseCommand):
    help = 'Loads data into the system.'

    def handle(self, *args, **options):
        converter = Converter()
        recruitments_df = converter.convert_csv_to_df('Company/mapper/initial_data/existing_companies_recruitments.csv')

        preprocessor = LoadPreprocessor()
        recruitments_df = preprocessor.add_company_id_from_name(recruitments_df)

        loader = DataLoader()
        num_input, num_created, num_updated = loader.load_recruitment_from_df(recruitments_df)

        self.stdout.write(self.style.SUCCESS(f"Number of Recruitments input: {num_input}, Number of Recruitments created: {num_created}, Number of Recruitments updated: {num_updated}"))
