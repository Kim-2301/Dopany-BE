from django.core.management.base import BaseCommand
import pandas as pd
from Company.mapper.loader import DataLoader
from Company.mapper.converter import Converter
from Company.mapper.preprocessor import LoadPreprocessor

class Command(BaseCommand):
    help = 'Loads data into the system.'

    def handle(self, *args, **options):
        converter = Converter()
        loader = DataLoader()
        preprocessor = LoadPreprocessor()

        # load company
        companies_df_list = converter.convert_companies_csv_to_df('Company/mapper/initial_data/companies')
        companies_df = pd.concat(companies_df_list)
        num_input, num_created, num_updated = loader.load_company_from_df(companies_df)
        self.stdout.write(self.style.SUCCESS(f"Number of companies input: {num_input}, Number of companies created: {num_created}, Number of companies updated: {num_updated}"))
        
        # load stock
        stocks_df_list = converter.convert_stocks_csv_to_df('Company/mapper/initial_data/stocks')
        stocks_df = pd.concat(stocks_df_list)
        stocks_df = preprocessor.add_company_id_from_name(stocks_df)
        num_input, num_created, num_updated = loader.load_stock_from_df(stocks_df)
        self.stdout.write(self.style.SUCCESS(f"Number of Stock input: {num_input}, Number of Stock created: {num_created}, Number of Stock updated: {num_updated}"))
        
        # load job
        jobs_df = converter.convert_csv_to_df('Company/mapper/initial_data/job.csv')
        num_input, num_created, num_updated = loader.load_job_from_df(jobs_df)
        self.stdout.write(self.style.SUCCESS(f"Number of Jobs input: {num_input}, Number of Jobs created: {num_created}, Number of Jobs updated: {num_updated}"))

        # load skill
        skills_df = converter.convert_csv_to_df('Company/mapper/initial_data/skill.csv')
        num_input, num_created, num_updated = loader.load_skill_from_df(skills_df)
        self.stdout.write(self.style.SUCCESS(f"Number of Skills input: {num_input}, Number of Skills created: {num_created}, Number of Skills updated: {num_updated}"))

        # load recruitment
        recruitments_df = converter.convert_csv_to_df('Company/mapper/initial_data/existing_companies_recruitments.csv')
        recruitments_df = preprocessor.add_company_id_from_name(recruitments_df)
        num_input, num_created, num_updated = loader.load_recruitment_from_df(recruitments_df)
        self.stdout.write(self.style.SUCCESS(f"Number of Recruitments input: {num_input}, Number of Recruitments created: {num_created}, Number of Recruitments updated: {num_updated}"))

        # load news
        news_df_list = converter.convert_news_csv_to_df('Company/mapper/initial_data/news')
        news_df = pd.concat(news_df_list)
        num_input = loader.load_news_from_df(news_df)
        self.stdout.write(self.style.SUCCESS(f"Number of News input: {num_input}, Number of News created: {num_input}"))

        # load reviews
        reviews_df_list = converter.convert_reviews_csv_to_df('Company/mapper/initial_data/reviews/cons')
        reviews_df = pd.concat(reviews_df_list)
        num_input = loader.load_cons_review_from_df(reviews_df)
        self.stdout.write(self.style.SUCCESS(f"Number of Cons Reviews input: {num_input}"))

        reviews_df_list = converter.convert_reviews_csv_to_df('Company/mapper/initial_data/reviews/pros')
        reviews_df = pd.concat(reviews_df_list)
        num_input = loader.load_pros_review_from_df(reviews_df)
        self.stdout.write(self.style.SUCCESS(f"Number of Pros Reviews input: {num_input}"))

        # load review words
        pros_num_input = loader.load_pros_review_word_from_db()
        cons_num_input = loader.load_cons_review_word_from_db()
        self.stdout.write(self.style.SUCCESS(f"Number of Pros Review Words input: {pros_num_input}, Cons Review Words input: {cons_num_input}"))