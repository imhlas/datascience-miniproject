import pandas as pd

class AlcoholDataset:
    def __init__(self, dataset_name) -> pd.DataFrame:
        self.dataset_name = dataset_name
        self.invalid_geo = [
            'European Union - 27 countries (from 2020)',
            'European Union - 28 countries (2013-2020)',
            'Italy'
        ]
        self.ages = [
            'From 15 to 24 years',
            'From 25 to 34 years',
            'From 35 to 44 years',
            'From 45 to 54 years',
            'From 55 to 64 years',
            'From 65 to 74 years',
            '75 years or over'
        ]
        self.raw_data = self.get_eurostat_datasets(dataset_name)
        self.cleaned_data = self.clean_data()
        self.filtered_data = self.data_filtering(self.cleaned_data)
        self.pivot_dataset = self.freq_to_columns(self.filtered_data)

    def get_eurostat_datasets(self, dataset_name):
        csv_url = f"https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/{dataset_name}/?format=SDMX-CSV&lang=en&label=label_only"
        return pd.read_csv(csv_url)

    def clean_data(self):
        # Drop unnecessary columns
        dataset = self.raw_data.drop(['freq','unit','DATAFLOW', 'LAST UPDATE'], axis=1)

        # Drop rows with missing OBS_VALUE 
        dataset.dropna(subset=['OBS_VALUE'])

        return dataset

    def data_filtering(self, dataset):
        dataset = dataset[
                    (dataset['age'].isin(self.ages))
                    & (~dataset['frequenc'].isin(self.invalid_geo))
                    & (dataset['sex'] != 'Total')
                    & (dataset['isced11'] != 'All ISCED 2011 levels')
                    & (~dataset['frequenc'].isin(['Never', 'Not in the last 12 months']))
                    ]

        return dataset
        
    def freq_to_columns(self, dataset):
        self.filtered_data = dataset.pivot_table(index=['isced11','age', 'geo','sex', 'TIME_PERIOD'],  
                                                  columns='frequenc',           
                                                  values='OBS_VALUE',                
                                                  aggfunc='sum')              

        return self.filtered_data.reset_index()
    