import os
import pandas as pd
import kagglehub


def load_data() -> pd.DataFrame:
    """
    Load the data from Kaggle.
    """
    dataset_handle = "caesarmario/our-world-in-data-covid19-dataset"
    path = kagglehub.dataset_download(dataset_handle)

    # hard coding the filename here since there's a single file in the dataset
    df = pd.read_csv(os.path.join(path, "owid-covid-data.csv"))

    # filter data
    df["date"] = pd.to_datetime(df["date"])
    df_countries = df[~df["iso_code"].str.startswith("OWID_")]

    # TODO: add some data cleaning steps here

    return df_countries
