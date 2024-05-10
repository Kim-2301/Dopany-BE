from django.core.management.base import BaseCommand
from Company.mapper.converter import Converter
from Company.mapper.loader import DataLoader

class Command(BaseCommand):
    help = 'Loads data into the system.'

    def handle(self, *args, **options):
        converter = Converter()
        jobs_df = converter.convert_csv_to_df('Company/mapper/initial_data/job.csv')

        loader = DataLoader()
        num_input, num_created, num_updated = loader.load_job_from_df(jobs_df)
        
        self.stdout.write(self.style.SUCCESS(f"Number of Jobs input: {num_input}, Number of Jobs created: {num_created}, Number of Jobs updated: {num_updated}"))
