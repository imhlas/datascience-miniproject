import pandas as pd
from os import path

def simplify_frequenc(df):
    df_copy = df.copy() 
    df_copy['frequenc_simplified'] = df_copy['frequenc'].replace({
        'Every day': 'Frequent drinkers',
        'Every week': 'Frequent drinkers',
        'Every month': 'Occasional drinkers',
        'Less than once a month': 'Occasional drinkers',
        'Never': 'Non-drinkers',
        'Not in the last 12 months': 'Non-drinkers',
        'Never or not in the last 12 months': 'Non-drinkers'
    })
    return df_copy

def simplify_age(df):
    df_copy = df.copy()
    df_copy=df_copy[df_copy["age"].isin(["From 15 to 24 years","From 25 to 34 years","From 35 to 44 years","From 45 to 54 years","From 55 to 64 years","65 years or over"])]
    return df_copy


def write_dataset(data, dataset_name):
    filepath=path.join("datasets_clean", dataset_name + ".csv")
    data.to_csv(filepath,sep=";")
    print("Wrinting dataset ",dataset_name, " to folder datasets_clean")
    

def clean_datasets(freq_education, freq_income, freq_urbanisation, write_to_folder=False):
    """
    Cleans the datasets obtained from eurostat
    """
    
    # Drop unnecessary columns
    freq_education = freq_education.drop(['freq','unit','DATAFLOW', 'LAST UPDATE'], axis=1)
    freq_income = freq_income.drop(['freq','unit','DATAFLOW', 'LAST UPDATE'], axis=1)
    freq_urbanisation = freq_urbanisation.drop(['freq','unit','DATAFLOW', 'LAST UPDATE'], axis=1)

    # Drop rows with missing OBS_VALUE
    freq_education_cleaned = freq_education.dropna(subset=['OBS_VALUE'])
    freq_income_cleaned = freq_income.dropna(subset=['OBS_VALUE'])
    freq_urbanisation_cleaned = freq_urbanisation.dropna(subset=['OBS_VALUE'])

    # Simplify frequencies into general categories
    # DOUBT, IIRC there was no overlap, but ask again
    freq_education_cleaned = simplify_frequenc(freq_education_cleaned)
    freq_income_cleaned = simplify_frequenc(freq_income_cleaned)
    freq_urbanisation_cleaned = simplify_frequenc(freq_urbanisation_cleaned)

    # Simplifying age into less categories
    freq_education_cleaned = simplify_age(freq_education_cleaned)
    freq_income_cleaned = simplify_age(freq_income_cleaned)
    freq_urbanisation_cleaned = simplify_age(freq_urbanisation_cleaned)
    
    # Dropping entries from Italy, since their values are non-comparable
    # Dropping entries from European Union, since they are redundant
    freq_education_cleaned = freq_education_cleaned[~freq_education_cleaned["geo"].isin(["Italy","European Union - 27 countries (from 2020)","European Union - 28 countries (2013-2020)"])]
    freq_income_cleaned =  freq_income_cleaned[~freq_income_cleaned["geo"].isin(["Italy","European Union - 27 countries (from 2020)","European Union - 28 countries (2013-2020)"])]
    freq_urbanisation_cleaned =freq_urbanisation_cleaned[~freq_urbanisation_cleaned["geo"].isin(["Italy","European Union - 27 countries (from 2020)","European Union - 28 countries (2013-2020)"])]
    
    # Writing csv files to folder
    if write_to_folder:
        write_dataset(freq_education_cleaned,"freq_education_cleaned")
        write_dataset(freq_income_cleaned,"freq_income_cleaned")
        write_dataset(freq_urbanisation_cleaned,"freq_urbanisation_cleaned")

    return freq_education_cleaned, freq_income_cleaned, freq_urbanisation_cleaned
