import pandas as pd
import os

class Converter:
    def convert_csv_to_df(self, csv_path):
        df = pd.read_csv(csv_path)
        print(df)
        return df
    
    def convert_stocks_csv_to_df(self, directory_path):
        dataframes = []

        for filename in os.listdir(directory_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(directory_path, filename)
                df = pd.read_csv(file_path)
                df['company_name'] = filename.split('_')[0]
                
                dataframes.append(df)
        
        return dataframes
    
    def convert_companies_csv_to_df(self, directory_path):
        dataframes = []

        for filename in os.listdir(directory_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(directory_path, filename)
                df = pd.read_csv(file_path)
                df['industry_name'] = f'{filename.split("_")[0]}>{filename.split("_")[1]}'
                
                dataframes.append(df)
        
        return dataframes
