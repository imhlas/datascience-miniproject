import pandas as pd
from os import path



def get_eurostat_dataset(dataset_name,force_download_flag=False):
    """
    Obtains eurostat datasets, either downloading them or from local folder
    """
    
    filepath=path.join("data/datasets_raw", dataset_name + ".csv")

    if not path.isfile(filepath) or force_download_flag:
        print(f"Downloading dataset {dataset_name}:")
        csv_url = f"https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/{dataset_name}/?format=SDMX-CSV&lang=en&label=label_only"
        data= pd.read_csv(csv_url)
        data.to_csv(filepath,sep=";")
    else:
        print(f"Loading dataset {dataset_name} from folder datasets_raw:")
        data=pd.read_csv(filepath,sep=";")
        
    return data
    

def load_datasets(dataset_name, force_download_flag=False):
    """
    Loads datasets related to alcohol consumption
    """
    
    # Get frequencies by alcohol consumption datasets
    dataset = get_eurostat_dataset(dataset_name,force_download_flag=force_download_flag)

    return dataset
    