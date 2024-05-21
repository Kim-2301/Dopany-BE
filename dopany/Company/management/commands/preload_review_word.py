from django.core.management.base import BaseCommand
from Company.mapper.loader import DataLoader

class Command(BaseCommand):
    help = 'Loads data into the system.'

    def handle(self, *args, **options):
        loader = DataLoader()
        pros_num_input = loader.load_pros_review_word_from_db()
        cons_num_input = loader.load_cons_review_word_from_db()

        self.stdout.write(self.style.SUCCESS(f"Number of Pros Review Words input: {pros_num_input}, Cons Review Words input: {cons_num_input}"))
