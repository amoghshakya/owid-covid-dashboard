import os
import numpy as np
import pandas as pd
import kagglehub


DATA_DIR = "data"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load the data from Kaggle.

    Returns:
        df: The cleaned and pre-processed DataFrame.
        monthly_global: Monthly aggregated global data.
        snapshot: Latest snapshot of each country.
        pivot_cases: Pivot table of new cases by continent and year.
    """
    # check if data dir exists
    if os.path.exists(DATA_DIR):
        print(f"Data directory '{DATA_DIR}' already exists. Loading data from there.")
        # check if the required files are present
        files = [
            "covid_cleaned.csv",
            "covid_monthly_global.csv",
            "covid_country_snapshot.csv",
            "covid_pivot_continent_year.csv",
        ]
        if all(os.path.exists(os.path.join(DATA_DIR, f)) for f in files):
            print("All required files are present. Loading data from local files.")
            df = pd.read_csv(
                os.path.join(DATA_DIR, "covid_cleaned.csv"), parse_dates=["date"]
            )
            monthly_global = pd.read_csv(
                os.path.join(DATA_DIR, "covid_monthly_global" + ".csv")
            )
            snapshot = pd.read_csv(
                os.path.join(DATA_DIR, "covid_country_snapshot" + ".csv")
            )
            pivot_cases = pd.read_csv(
                os.path.join(DATA_DIR, "covid_pivot_continent_year" + ".csv")
            )
            return df, monthly_global, snapshot, pivot_cases
    else:
        # prevent from throwing error
        os.makedirs(DATA_DIR, exist_ok=True)

    # first time run
    print("Missing data files. Downloading dataset from Kaggle...")
    dataset_handle = "caesarmario/our-world-in-data-covid19-dataset"
    try:
        path = kagglehub.dataset_download(dataset_handle)
    except Exception:
        print("No internet connectivity...")
        exit()

    # hard coding the filename here since there's a single file in the dataset
    df = pd.read_csv(os.path.join(path, "owid-covid-data.csv"), parse_dates=["date"])

    # filter data
    # df["date"] = pd.to_datetime(df["date"])

    print("Dataset downloaded. Preprocessing data...")
    df, monthly_global, snapshot, pivot_cases = prepare_date(df)

    return df, monthly_global, snapshot, pivot_cases


def prepare_date(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Pre-processing and cleaning the dataset.
    """
    #
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%b")

    # aggregated_locations = df[df["continent"].isna()]["location"].unique()

    df = df[df["continent"].notna()].copy()

    # protect these columns from being dropped
    # these are essential for analysis
    essential_vars = [
        "stringency_index",
        "people_fully_vaccinated_per_hundred",  # vaccination didn't start until year 2, so a lot of values would be nil
        "icu_patients_per_million",
        "hospital_beds_per_thousand",
    ]

    # set threshold for missing values
    threshold = 0.7  # 70% missing values
    missing_pct = df.isnull().mean()
    cols_to_drop = [
        c for c in missing_pct[missing_pct > threshold].index if c not in essential_vars
    ]

    # NOTE: dropping columns here
    df.drop(columns=cols_to_drop, inplace=True)

    key_columns = [
        "iso_code",
        "continent",
        "location",
        "date",
        "year",
        "month",
        "month_name",
        "total_cases",
        "new_cases",
        "new_cases_smoothed",
        "total_deaths",
        "new_deaths",
        "new_deaths_smoothed",
        "total_cases_per_million",
        "total_deaths_per_million",
        "reproduction_rate",
        "stringency_index",
        "people_fully_vaccinated_per_hundred",
        "icu_patients_per_million",
        "gdp_per_capita",
        "life_expectancy",
        "human_development_index",
        "median_age",
        "population",
        "population_density",
        "diabetes_prevalence",
        "hospital_beds_per_thousand",
        "cardiovasc_death_rate",
    ]

    key_columns = [c for c in key_columns if c in df.columns]
    df = df[key_columns].copy()

    # fill daily cases and deaths with 0, this would likely mean no new cases
    for col in [
        "new_cases",
        "new_deaths",
        "new_cases_smoothed",
        "new_deaths_smoothed",
    ]:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    df.sort_values(["location", "date"], inplace=True)
    for col in [
        "total_cases",
        "total_deaths",
        "total_cases_per_million",
        "total_deaths_per_million",
    ]:
        if col in df.columns:
            df[col] = df.groupby("location")[col].ffill().fillna(0)

    socio_cols = [
        "gdp_per_capita",
        "life_expectancy",
        "human_development_index",
        "median_age",
        "population_density",
        "diabetes_prevalence",
        "hospital_beds_per_thousand",
        "cardiovasc_death_rate",
    ]
    # forward fill and backward fill socio-economic indicators, these are not
    # time series data and should be filled with the same value for each
    # location
    for col in socio_cols:
        if col in df.columns:
            df[col] = df.groupby("location")[col].ffill().bfill()

    # interpolate stringency index and reproduction rate, these are time series data and should be interpolated
    for col in ["stringency_index", "reproduction_rate"]:
        if col in df.columns:
            df[col] = df.groupby("location")[col].transform(
                lambda x: x.interpolate(method="linear").ffill().bfill()
            )

    # remove negative values
    for col in ["new_cases", "new_deaths", "total_cases", "total_deaths"]:
        if col in df.columns:
            df[col] = df[col].clip(lower=0)

    # INFO: Data Engineering
    # case fatality rate
    df["case_fatality_rate"] = np.where(
        df["total_cases"] > 0,
        (df["total_deaths"] / df["total_cases"] * 100).round(4),
        0,
    )

    # Deaths per 100k population
    df["deaths_per_100k"] = np.where(
        df["population"] > 0,
        (df["total_deaths"] / df["population"] * 100000).round(4),
        0,
    )

    # GDP per capita groups
    gdp_bins = [0, 5000, 15000, 40000, float("inf")]
    gdp_labels = ["Low Income", "Lower-Middle", "Upper-Middle", "High Income"]
    df["gdp_group"] = pd.cut(df["gdp_per_capita"], bins=gdp_bins, labels=gdp_labels)

    df["month_year"] = df["date"].dt.to_period("M").astype(str)

    pivot_cases = df.groupby(["continent", "year"])["new_cases"].sum().reset_index()
    pivot_cases = pivot_cases.pivot(
        index="continent", columns="year", values="new_cases"
    )
    pivot_cases.columns.name = None
    pivot_cases = pivot_cases.fillna(0).astype(int)

    monthly_global = (
        df.groupby("month_year")
        .agg(
            total_new_cases=("new_cases", "sum"),
            total_new_deaths=("new_deaths", "sum"),
            avg_reproduction=("reproduction_rate", "mean"),
            avg_stringency=("stringency_index", "mean"),
        )
        .reset_index()
    )

    # Country snapshot (latest record per country)
    snapshot = df.sort_values("date").groupby("location").last().reset_index()

    df.to_csv(f"{DATA_DIR}/covid_cleaned.csv", index=False)
    monthly_global.to_csv(f"{DATA_DIR}/covid_monthly_global.csv", index=False)
    snapshot.to_csv(f"{DATA_DIR}/covid_country_snapshot.csv", index=False)
    pivot_cases.to_csv(f"{DATA_DIR}/covid_pivot_continent_year.csv")

    return df, monthly_global, snapshot, pivot_cases
