from load_raw_datasets import load_datasets
from clean_datasets import clean_datasets
from classify import classify


def main():
    print("Starting the program...")
    
    freq_education, freq_income, freq_urbanisation = load_datasets()
    freq_education_cleaned, freq_income_cleaned, freq_urbanisation_cleaned = clean_datasets(freq_education,freq_income,freq_urbanisation,write_to_folder=False)
    classify(freq_education_cleaned,freq_income_cleaned,freq_urbanisation_cleaned)
    
    print("Program finished.")

if __name__ == "__main__":
    main()
