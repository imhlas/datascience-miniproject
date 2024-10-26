import data_load
import data_mod
import clustering
from os import path

def write_dataset(data, folder, dataset_name):
    """
    Helper function to write datasets from memory to folders.
    
    Parameters:
    - data (Pandas dataframe): The dataframe to save
    - folder (String): Target folder path where the dataframe is saved
    - dataset_name (String): Name for the dataset
    
    Outcome:
    - It creates a file as specified by the parameters
    """
    
    filepath=path.join(folder, dataset_name + ".csv")
    data.to_csv(filepath, sep=";")
    print("Writing ", dataset_name, " to ", filepath)

def get_clusters(dataset_name, dataset_group, force_download_flag=False, rewrite_clean_datasets=True, rewrite_clusters=True):
    """
    Function that loads data using the data_load.py file, cleans the data using the data_mod.py file, and performs the clustering using the clustering.py file.
    
    Parameters:
    - dataset_name (String): It is "hlth_ehis_al1e", "hlth_ehis_al1i" or "hlth_ehis_al1u".
    - dataset_group (String): It is "education", "income" or "urbanisation".
    - force_download_flag (bool): Defaults to False. If True it attempts to load the dataset from the internet instead of from local.
    - rewrite_clean_data (bool): Defaults to True, in that case, any changes done to the data_mod.py file will overwrite the files in datasets_clean
    - rewrite_clusters (bool): Defaults to True, in that case, the clusters are also overwriten
    
    Outcome:
    - Prints the status in console, and saves the files to folders according to the flags.
    """
    
    print("Starting the processing...")
    data = data_load.load_datasets(dataset_name = dataset_name, force_download_flag=force_download_flag)

    # Clean datasets and filter using AlcoholDataset module
    print(f"Cleaning {dataset_group} dataset:")
    data_cleaned = data_mod.AlcoholDataset(dataset_name= dataset_name,
                                                    raw_data=data,
                                                    dataset_group=dataset_group,
                                                    frequency_reduction=True).get_dataset()
    
    data_cleaned = data_cleaned[data_cleaned['TIME_PERIOD'] == 2014].drop(['TIME_PERIOD'], axis=1)

    if rewrite_clean_datasets:
        write_dataset(data_cleaned,"data/datasets_clean", f"freq_{dataset_group}_cleaned")

    clusters, _  = clustering.cluster(data_cleaned,cat=[0,1,2,3])

    print(f"Clustering {dataset_group} data:")
    if rewrite_clusters:
            write_dataset(clusters, "data/clusters", f"{dataset_group}_clusters")

    print("Data processing finished.")


if __name__ == "__main__":
    """
    Calls the get_clusters() function to obtain the education, income and urbanisation clusters and output them to a folder
    """
    get_clusters(dataset_name='hlth_ehis_al1e', dataset_group='education')
    get_clusters(dataset_name='hlth_ehis_al1i', dataset_group='income')
    get_clusters(dataset_name='hlth_ehis_al1u', dataset_group='urbanisation')