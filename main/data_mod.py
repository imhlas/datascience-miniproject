import pandas as pd

class AlcoholDataset:
    def __init__(self, dataset_name, dataset_group, ages = None, frequences = None, feature_reduction = False) -> pd.DataFrame:
        self.dataset_group = dataset_group
        self.dataset_name = dataset_name
        self.invalid_geo = [
            'European Union - 27 countries (from 2020)',
            'European Union - 28 countries (2013-2020)',
            'Italy'
        ]
        self.feature_reduction = feature_reduction

        # Default value for ages
        if ages == None:
            self.ages = [
                'From 15 to 24 years',
                'From 25 to 34 years',
                'From 35 to 44 years',
                'From 45 to 54 years',
                'From 55 to 64 years',
                'From 65 to 74 years',
                '75 years or over'
            ]
        else:
            self.ages = ages
        
        # Default value for frequences
        if frequences == None:
            self.frequences = ['Every day',
                                'Every month',
                                'Every week',
                                'Less than once a month',
                                'Never or not in the last 12 months']
        else:
            self.frequences = frequences

 
        self.raw_data = self.get_eurostat_datasets(dataset_name)
        self.cleaned_data = self.clean_data()
        self.filtered_data = self.data_filtering(self.cleaned_data)
        
        if feature_reduction:
            self.apply_feature_reduction()
            
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
        
        condition = None
        if self.dataset_group == 'education':
            condition = (dataset['isced11'] != 'All ISCED 2011 levels')
        elif self.dataset_group == 'income':
            condition = (dataset['quant_inc'] != 'Total')
        
        dataset = dataset[
                    (dataset['age'].isin(self.ages))
                    & (~dataset['geo'].isin(self.invalid_geo))
                    & (dataset['sex'] != 'Total')
                    & (dataset['frequenc'].isin(self.frequences))
                    & condition
                    ]

        return dataset
        
    def freq_to_columns(self, dataset):
        
        index_list = ['age', 'geo','sex', 'TIME_PERIOD']
        if self.dataset_group == 'education':
            index_list.append('isced11')
        elif self.dataset_group == 'income':
            index_list.append('quant_inc')
        
        self.filtered_data = dataset.pivot_table(index=index_list, 
                                                  columns='frequenc',           
                                                  values='OBS_VALUE',                
                                                  aggfunc='sum')              

        return self.filtered_data.reset_index()

    def get_dataset(self):
        return self.pivot_dataset
    
