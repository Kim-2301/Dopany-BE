from django.core.management.base import BaseCommand
from Company.mapper.converter import Converter
from Company.mapper.loader import DataLoader

class Command(BaseCommand):
    help = 'Loads data into the system.'

    def handle(self, *args, **options):
        converter = Converter()
        skills_df = converter.convert_csv_to_df('Company/mapper/initial_data/skill.csv')

        loader = DataLoader()
        num_input, num_created, num_updated = loader.load_skill_from_df(skills_df)
        
        self.stdout.write(self.style.SUCCESS(f"Number of Skills input: {num_input}, Number of Skills created: {num_created}, Number of Skills updated: {num_updated}"))
