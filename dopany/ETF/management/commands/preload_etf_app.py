from django.core.management.base import BaseCommand
import pandas as pd
from ETF.mapper.loader import DataLoader
from ETF.mapper.constants import *
from ETF.mapper.converter import Converter
from ETF.mapper.preprocessor import LoadPreprocessor

class Command(BaseCommand):
    help = 'Loads data into the system.'

    def handle(self, *args, **options):
        converter = Converter()
        loader = DataLoader()
        preprocessor = LoadPreprocessor()

        # load domain
        domains_df = pd.DataFrame(domain_list)
        num_input, num_created, num_updated = loader.load_domain_from_df(domains_df)
        self.stdout.write(self.style.SUCCESS(f"Number of domains input: {num_input}, Number of domains created: {num_created}, Number of domains updated: {num_updated}"))

        # load industry
        industries_df = converter.convert_csv_to_df('ETF/mapper/initial_data/domain_industry_name_map.csv')
        industries_df = preprocessor.add_domain_id_from_name(industries_df)
        num_input, num_created, num_updated = loader.load_industry_from_df(industries_df)
        self.stdout.write(self.style.SUCCESS(f"Number of industries input: {num_input}, Number of industries created: {num_created}, Number of industries updated: {num_updated}"))
        
        # load etf_product
        etf_products_df = converter.convert_csv_to_df('ETF/mapper/initial_data/domain_etf_name_map.csv')
        etf_products_df = preprocessor.add_domain_id_from_name(etf_products_df)
        num_input, num_created, num_updated = loader.load_etf_product_from_df(etf_products_df)
        self.stdout.write(self.style.SUCCESS(f"Number of ETF Product input: {num_input}, Number of ETF Product created: {num_created}, Number of ETF Product updated: {num_updated}"))

        # load etf_price
        etf_prices_df_list = converter.convert_etfs_csv_to_df('ETF/mapper/initial_data/etfs')
        etf_prices_df = pd.concat(etf_prices_df_list)
        etf_prices_df = preprocessor.add_etf_product_id_from_name(etf_prices_df)
        num_input, num_created, num_updated = loader.load_etf_price_from_df(etf_prices_df)
        self.stdout.write(self.style.SUCCESS(f"Number of ETF Price input: {num_input}, Number of ETF Price created: {num_created}, Number of ETF Price updated: {num_updated}"))

        # load etf_major
        etf_major_companies_df = converter.convert_csv_to_df('ETF/mapper/initial_data/domain_etf_company_name_map.csv')
        etf_major_companies_df = preprocessor.add_etf_product_id_from_name(etf_major_companies_df)
        num_input, num_created, num_updated = loader.load_etf_major_company_from_df(etf_major_companies_df)
        self.stdout.write(self.style.SUCCESS(f"Number of domains input: {num_input}, Number of domains created: {num_created}, Number of domains updated: {num_updated}"))
