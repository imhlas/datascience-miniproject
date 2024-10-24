import data_load
import data_mod
import clustering
from os import path

def write_dataset(data, folder, dataset_name):
    filepath=path.join(folder, dataset_name + ".csv")
    data.to_csv(filepath, sep=";")
    print("Writing ", dataset_name, " to ", filepath)

def get_clusters(dataset_name, dataset_group, force_download_flag=False, rewrite_clean_datasets=True, rewrite_clusters=True):
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
    get_clusters(dataset_name='hlth_ehis_al1e', dataset_group='education')
    get_clusters(dataset_name='hlth_ehis_al1i', dataset_group='income')
    get_clusters(dataset_name='hlth_ehis_al1u', dataset_group='urbanisation')