import plotly.express as px
import pandas as pd


def create_correlation_heatmap(data: pd.DataFrame):
    latest_data = data.groupby("location").tail(1)

    cols = [
        "total_deaths_per_million",  # Mortality Outcome
        "gdp_per_capita",  # Socioeconomic
        "median_age",  # Demographic
        "stringency_index",  # Policy
        "people_fully_vaccinated_per_hundred",  # Strategy
    ]

    corr_matrix = latest_data[cols].corr()

    fig = px.imshow(
        corr_matrix,
        text_auto=".2f",
        aspect="auto",
        # color_continuous_scale="RdBu_r",
        labels=dict(color="Correlation"),
        title="Interdependent Variables: Mortality, Economy, and Policy",
        x=["Deaths", "GDP", "Age", "Policy", "Vax"],
        y=["Deaths", "GDP", "Age", "Policy", "Vax"],
    )

    fig.update_layout(template="plotly_white")

    return fig
