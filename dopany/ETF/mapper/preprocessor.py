from django.core.exceptions import ObjectDoesNotExist
from ETF.models import *

from utils.decorator import singleton

@singleton
class LoadPreprocessor:
    def add_domain_id_from_name(self, raw_df):
        """
        Maps domain_name to domain_id using the Domain model and updates
        raw_df with the corresponding domain_id.

        Parameters:
        - raw_df (DataFrame): DataFrame including 'domain_name'.

        Returns:
        - DataFrame: Updated DataFrame with 'domain_id' added.
        """
        def get_domain_id(domain_name):
            try:
                return Domain.objects.get(domain_name=domain_name).domain_id
            except ObjectDoesNotExist:
                return None

        raw_df['domain_id'] = raw_df['domain_name'].apply(get_domain_id)

        if raw_df['domain_id'].isnull().any():
            missing_names = raw_df[raw_df['domain_id'].isnull()]['domain_name'].tolist()
            raise ValueError(f"No matching domain_id found for domain_names: {', '.join(missing_names)}")

        return raw_df

    def add_etf_product_id_from_name(self, raw_df):
        """
        Directly maps etf_product_name to etf_product_id using the EtfProduct model and updates
        raw_df with the corresponding etf_product_id.

        Parameters:
        - raw_df (DataFrame): DataFrame including 'etf_product_name'.

        Returns:
        - DataFrame: Updated DataFrame with 'etf_product_id' added.
        """
        # Function to fetch etf_product_id based on etf_product_name
        def get_etf_product_id(product_name):
            try:
                return EtfProduct.objects.get(etf_product_name=product_name).etf_product_id
            except ObjectDoesNotExist:
                return None

        # Apply the function to each row in the DataFrame
        raw_df['etf_product_id'] = raw_df['etf_product_name'].apply(get_etf_product_id)

        # Check if there are any rows where 'etf_product_id' couldn't be found
        if raw_df['etf_product_id'].isnull().any():
            missing_names = raw_df[raw_df['etf_product_id'].isnull()]['etf_product_name'].tolist()
            raise ValueError(f"No matching etf_product_id found for etf_product_names: {', '.join(missing_names)}")

        return raw_df

    def add_industry_id_with_domain(self, raw_df):
        """
        Updates raw_df with industry_id based on industry_name and domain_name.

        Parameters:
        - raw_df (DataFrame): DataFrame including 'industry_name' and 'domain_name'.

        Returns:
        - DataFrame: Updated DataFrame with 'industry_id' added.
        """
        # Fetch all domain_ids based on domain_name
        domains = Domain.objects.in_bulk(field_name='domain_name')
        domain_map = {domain.domain_name: domain.domain_id for domain in domains.values()}

        # Fetch all industries
        industries = Industry.objects.all()
        industry_map = {(ind.industry_name, ind.domain_id): ind.industry_id for ind in industries}

        # Resolve domain_id from domain_name
        raw_df['domain_id'] = raw_df['domain_name'].apply(lambda x: domain_map.get(x, None))

        # Map industry_name and domain_id to industry_id
        raw_df['industry_id'] = raw_df.apply(lambda row: industry_map.get((row['industry_name'], row['domain_id']), None), axis=1)

        # Error checking
        if raw_df['industry_id'].isnull().any():
            missing_data = raw_df[raw_df['industry_id'].isnull()][['industry_name', 'domain_name']]
            error_message = "No matching industry_id found for given industry and domain combinations:\n"
            error_message += "\n".join([f"{row['industry_name']} in {row['domain_name']}" for _, row in missing_data.iterrows()])
            raise ValueError(error_message)

        return raw_df

    def add_industry_from_name(self, raw_df):
        """
        Directly maps industry_name to industry using the Industry model and updates
        raw_df with the corresponding industry.

        Parameters:
        - raw_df (DataFrame): DataFrame including 'industry_name'.

        Returns:
        - DataFrame: Updated DataFrame with 'industry' added.
        """
        # Function to fetch etf_product_id based on etf_product_name
        def get_industry(industry_name):
            try:
                return Industry.objects.get(industry_name=industry_name)
            except ObjectDoesNotExist:
                return None

        # Apply the function to each row in the DataFrame
        raw_df['industry'] = raw_df['industry_name'].apply(get_industry)

        # Check if there are any rows where 'etf_product_id' couldn't be found
        if raw_df['industry'].isnull().any():
            missing_names = raw_df[raw_df['industry'].isnull()]['industry_name'].tolist()
            raise ValueError(f"No matching industry found for industry_names: {', '.join(missing_names)}")

        return raw_df