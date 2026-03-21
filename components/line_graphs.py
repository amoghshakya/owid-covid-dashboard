# modularize the figures

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_cases_death_chart(filtered_data: pd.DataFrame, country_name: str):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=filtered_data["date"],
            y=filtered_data["new_cases_smoothed"],
            name="New Cases (7-day avg)",
            line=dict(color="steelblue", width=2),
            fill="tozeroy",
            fillcolor="rgba(70, 130, 180, 0.2)",
            legendgroup="cases",
        )
    )

    # 2. New Deaths (Secondary visual on same axis)
    fig.add_trace(
        go.Scatter(
            x=filtered_data["date"],
            y=filtered_data["new_deaths_smoothed"],
            name="New Deaths (7-day avg)",
            line=dict(color="#d62728", width=1.5),
        )
    )

    # dynamic wave annotations

    omicron_period = filtered_data[
        (filtered_data["date"].dt.year == 2022)
        & (filtered_data["new_cases_smoothed"] > 0)
    ]

    if not omicron_period.empty and omicron_period["new_cases_smoothed"].max() > 0:
        peak_row = omicron_period.loc[omicron_period["new_cases_smoothed"].idxmax()]

        fig.add_trace(
            go.Scatter(
                x=[peak_row["date"]],
                y=[peak_row["new_cases_smoothed"]],
                mode="markers+text",
                marker=dict(size=0),
                text=["Omicron Peak"],
                textposition="top center",
                textfont=dict(size=12),
                showlegend=False,
                legendgroup="cases",
                hoverinfo="skip",
            )
        )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Count (7-day avg)",
        title=f"<b>COVID-19 Trends: {country_name}</b>",
        template="plotly_white",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    fig.update_yaxes(ticksuffix=" ", exponentformat="SI")

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
            connectgaps=True,
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
        title_text=f"<b>Policy & Vaccination vs. Mortality: {country_name}</b>",
        template="plotly_white",
        legend=dict(orientation="v", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
    )

    fig.update_yaxes(title_text="Policy & Vax (%)", secondary_y=False)
    fig.update_yaxes(title_text="Daily Deaths", secondary_y=True)

    return fig


def create_continent_stacked_area(df: pd.DataFrame):
    continent_monthly = (
        df.groupby(["month_year", "continent"])["new_cases_smoothed"]
        .sum()
        .reset_index()
    )
    continent_monthly["date"] = pd.to_datetime(continent_monthly["month_year"])
    continent_monthly = continent_monthly.sort_values("date")

    # a consistent color map for continents
    continent_colors = {
        "North America": "#e74c3c",
        "South America": "#e67e22",
        "Europe": "#3498db",
        "Asia": "#2ecc71",
        "Africa": "#9b59b6",
        "Oceania": "#1abc9c",
    }

    fig = px.area(
        continent_monthly,
        x="date",
        y="new_cases_smoothed",
        color="continent",
        color_discrete_map=continent_colors,
        title="<b>Daily New COVID-19 Cases by Continent (Stacked Area)</b>",
        labels={
            "new_cases_smoothed": "New Cases",
            "date": "Date",
            "continent": "Continent",
        },
        template="plotly_white",
        category_orders={
            "continent": [
                "Asia",
                "Europe",
                "North America",
                "South America",
                "Africa",
                "Oceania",
            ]
        },
    )

    fig.update_layout(
        hovermode="x unified",  # Vital for stacked charts: shows all continent values at once
        xaxis_title="Date",
        yaxis_title="New Cases (Millions)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=50, r=50, t=100, b=50),
        height=600,
    )

    # Format Y-axis to show Millions (M)
    fig.update_yaxes(tickformat=".0s", ticksuffix="M")

    return fig


def create_cfr_trend_chart(filtered_data: pd.DataFrame, country_name: str):
    """Case Fatality Rate trend over time with global average reference"""
    fig = go.Figure()
    
    # Calculate global average CFR for reference
    global_avg_cfr = filtered_data["case_fatality_rate"].mean()
    
    fig.add_trace(
        go.Scatter(
            x=filtered_data["date"],
            y=filtered_data["case_fatality_rate"],
            name="Case Fatality Rate",
            line=dict(color="#e74c3c", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(231, 76, 60, 0.1)",
        )
    )
    
    # Add reference line for average
    fig.add_hline(
        y=global_avg_cfr,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Country Avg: {global_avg_cfr:.2f}%",
        annotation_position="right",
    )
    
    fig.update_layout(
        title=f"<b>Case Fatality Rate Trend: {country_name}</b>",
        xaxis_title="Date",
        yaxis_title="Case Fatality Rate (%)",
        template="plotly_white",
        hovermode="x unified",
        showlegend=False,
    )
    
    fig.update_yaxes(ticksuffix="%")
    
    return fig


def create_cumulative_cases_deaths_chart(filtered_data: pd.DataFrame, country_name: str):
    """Cumulative cases and deaths on dual-axis chart"""
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(
            x=filtered_data["date"],
            y=filtered_data["total_cases"],
            name="Total Cases",
            line=dict(color="#3498db", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(52, 152, 219, 0.1)",
        ),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(
            x=filtered_data["date"],
            y=filtered_data["total_deaths"],
            name="Total Deaths",
            line=dict(color="#e74c3c", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(231, 76, 60, 0.1)",
        ),
        secondary_y=True,
    )
    
    fig.update_layout(
        title=f"<b>Cumulative Pandemic Burden: {country_name}</b>",
        template="plotly_white",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Total Cases", secondary_y=False, tickformat=".2s")
    fig.update_yaxes(title_text="Total Deaths", secondary_y=True, tickformat=".2s")
    
    return fig
