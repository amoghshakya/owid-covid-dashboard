# modularize the figures

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_cases_death_chart(filtered_data: pd.DataFrame, country_name: str):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=filtered_data["date"],
            y=filtered_data["new_cases_smoothed"],
            name="New Cases (7-day avg)",
            line=dict(color="blue"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=filtered_data["date"],
            y=filtered_data["new_deaths_smoothed"],
            name="New Deaths (7-day avg)",
            line=dict(color="red"),
        )
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Count (7-day avg)",
        title=f"COVID-19 Trends: {country_name}",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        legend_title_text="Metrics",
    )
    return fig


def create_policy_vax_mortality_chart(filtered_data: pd.DataFrame, country_name: str):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=filtered_data["date"],
            y=filtered_data["people_fully_vaccinated_per_hundred"],
            name="Vax Coverage (%)",
            line=dict(color="green"),
            opacity=0.7,
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=filtered_data["date"],
            y=filtered_data["stringency_index"],
            name="Policy Stringency",
            line=dict(color="orange", dash="dot", width=1),
            fill="tozeroy",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=filtered_data["date"],
            y=filtered_data["new_deaths_smoothed"],
            name="New Deaths (7-day avg)",
            line=dict(color="red"),
        ),
        secondary_y=True,
    )
    fig.update_layout(
        title_text=f"Policy & Vaccination vs. Mortality: {country_name}",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    fig.update_yaxes(title_text="Policy & Vax (%)", secondary_y=False)
    fig.update_yaxes(title_text="Daily Deaths", secondary_y=True)

    return fig
