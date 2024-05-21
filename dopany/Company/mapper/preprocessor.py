from django.core.exceptions import ObjectDoesNotExist
from Company.models import *

from utils.decorator import singleton

@singleton
class LoadPreprocessor:
    def add_company_id_from_name(self, raw_df):
        """
        Directly maps company_name to company_id using the Company model and updates
        raw_df with the corresponding company_id.

        Parameters:
        - raw_df (DataFrame): DataFrame including 'company_name'.

        Returns:
        - DataFrame: Updated DataFrame with 'company_id' added.
        """
        # Function to fetch stock_id based on stock_name
        def get_company_id(company_name):
            try:
                return Company.objects.get(company_name=company_name).company_id
            except ObjectDoesNotExist:
                return None

        # Apply the function to each row in the DataFrame
        raw_df['company_id'] = raw_df['company_name'].apply(get_company_id)

        # Check if there are any rows where 'stock_id' couldn't be found
        if raw_df['company_id'].isnull().any():
            missing_names = raw_df[raw_df['company_id'].isnull()]['company_name'].unique().tolist()
            # raise ValueError(f"No matching company_id found for company_names: {', '.join(missing_names)} -> total : {len(raw_df['company_name'].unique())}/{len(missing_names)}")
            print(f"No matching company_id found for company_names: {', '.join(missing_names)} -> total : {len(raw_df['company_name'].unique())}/{len(missing_names)}")

        raw_df_clean = raw_df.dropna(subset=['company_id'])

        return raw_df_clean