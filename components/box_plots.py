import plotly.express as px
import pandas as pd


def create_hospital_capacity_boxplot(data: pd.DataFrame):
    latest_data = data.groupby("location").tail(1)

    latest_data = latest_data.dropna(subset=["hospital_beds_per_thousand", "continent"])

    fig = px.box(
        latest_data,
        x="continent",
        y="hospital_beds_per_thousand",
        color="continent",
        points="all",
        hover_name="location",
        title="Healthcare Resilience: Hospital Bed Capacity",
        labels={
            "hospital_beds_per_thousand": "Beds per 1,000 People",
            "continent": "Region",
        },
        category_orders={
            "continent": [
                "Africa",
                "Asia",
                "Europe",
                "North America",
                "South America",
                "Oceania",
            ]
        },
    )

    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        yaxis_title="Hospital Beds (per 1,000)",
        xaxis_title="Continent",
        margin=dict(l=40, r=40, t=60, b=40),
    )

    return fig
