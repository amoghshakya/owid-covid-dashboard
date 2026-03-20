import os
import pandas as pd
import kagglehub


def load_data() -> pd.DataFrame:
    """
    Load the data from Kaggle.
    """
    dataset_handle = "caesarmario/our-world-in-data-covid19-dataset"
    try:
        path = kagglehub.dataset_download(dataset_handle)
    except Exception:
        print("No internet connectivity...")
        exit()

    # hard coding the filename here since there's a single file in the dataset
    df = pd.read_csv(os.path.join(path, "owid-covid-data.csv"))

    # filter data
    df["date"] = pd.to_datetime(df["date"])

    # TODO: add some data cleaning steps here
    cols_to_fix = [
        "people_fully_vaccinated_per_hundred",
        "icu_patients_per_million",
        "hosp_patients",
        "stringency_index",
    ]
    df[cols_to_fix] = df.groupby("location")[cols_to_fix].ffill()

    df_countries = df[~df["iso_code"].str.startswith("OWID_")]
    return df_countries
