import plotly.express as px
import pandas as pd


def create_country_completeness_bar(filtered_data: pd.DataFrame, country_name: str):
    key_vars = [
        "total_deaths_per_million",
        "stringency_index",
        "icu_patients_per_million",
        "people_fully_vaccinated_per_hundred",
        "hospital_beds_per_thousand",
    ]

    completeness = (filtered_data[key_vars].notnull().mean() * 100).reset_index()
    completeness.columns = ["Variable", "Completeness"]

    fig = px.bar(
        completeness,
        x="Completeness",
        y="Variable",
        orientation="h",
        text_auto=".1f",
        title=f"Data Reporting Reliability: {country_name}",
        color="Completeness",
        color_continuous_scale="RdYlGn",
        range_x=[0, 100],
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Data Presence (%)",
        yaxis_title="",
        showlegend=False,
    )

    return fig
