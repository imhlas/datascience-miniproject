import data_load
import data_mod
import clustering
from os import path

def write_dataset(data, folder, dataset_name):
    filepath=path.join(folder, dataset_name + ".csv")
    data.to_csv(filepath,sep=";")
    print("Writing ",dataset_name, " to ", filepath)
    
    
def main(force_download_flag=False, rewrite_clean_datasets=True, rewrite_clusters=True):
    print("Starting the processing...")
    
    
    # Load datasets to memory
    freq_education, freq_income, freq_urbanisation = data_load.load_datasets(force_download_flag=force_download_flag)
    

    # Clean datasets and filter using AlcoholDataset module
    print("Cleaning education dataset:")
    freq_education_cleaned = data_mod.AlcoholDataset(dataset_name='hlth_ehis_al1e', raw_data=freq_education, dataset_group='education').get_dataset()
    freq_education_cleaned = freq_education_cleaned[freq_education_cleaned['TIME_PERIOD'] == 2014].drop(['TIME_PERIOD'], axis=1)
        
    print("Cleaning income dataset:")
    freq_income_cleaned = data_mod.AlcoholDataset(dataset_name='hlth_ehis_al1i', raw_data=freq_income, dataset_group='income').get_dataset()
    freq_income_cleaned = freq_income_cleaned[freq_income_cleaned['TIME_PERIOD'] == 2014].drop(['TIME_PERIOD'], axis=1)

    print("Cleaning urbanisation dataset:")
    freq_urbanisation_cleaned = data_mod.AlcoholDataset(dataset_name='hlth_ehis_al1u', raw_data=freq_urbanisation, dataset_group='urbanisation').get_dataset()
    freq_urbanisation_cleaned = freq_urbanisation_cleaned[freq_urbanisation_cleaned['TIME_PERIOD'] == 2014].drop(['TIME_PERIOD'], axis=1)
    
    # WARNING, freq_x_cleaned.csv files were different before, because the cleanup did not use the AlcoholDataset module
    if rewrite_clean_datasets:
        write_dataset(freq_education_cleaned,"data/datasets_clean", "freq_education_cleaned")
        write_dataset(freq_income_cleaned,"data/datasets_clean", "freq_income_cleaned")
        write_dataset(freq_urbanisation_cleaned,"data/datasets_clean", "freq_urbanisation_cleaned")
        
    
    # Perform clustering
    print("Clustering education data:")
    edu_clusters, edu_K=clustering.cluster(freq_education_cleaned,cat=[0,1,2,3])
    print("Clustering income data:")
    inc_clusters, inc_K=clustering.cluster(freq_income_cleaned,cat=[0,1,2,3])
    print("Clustering urbanisation data:")
    urb_clusters, urb_K=clustering.cluster(freq_urbanisation_cleaned,cat=[0,1,2,3])
    
    if rewrite_clusters:
        for i in range(edu_K):
            write_dataset(edu_clusters[edu_clusters['clusters']==i],"data/clusters", "edu_clu_"+str(i))
        for i in range(inc_K):
            write_dataset(inc_clusters[inc_clusters['clusters']==i],"data/clusters", "inc_clu_"+str(i))
        for i in range(urb_K):
            write_dataset(urb_clusters[urb_clusters['clusters']==i],"data/clusters", "urb_clu_"+str(i))
        
    print("Data processing finished.")

if __name__ == "__main__":
    main()
