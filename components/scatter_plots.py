import plotly.express as px
import pandas as pd


def create_gdp_mortality_bubble(snapshot_data: pd.DataFrame):
    scatter_df = snapshot_data.dropna(
        subset=["gdp_per_capita", "total_deaths_per_million", "continent", "population"]
    ).copy()

    # List of notable countries to always show labels for
    notable = [
        "United States",
        "Brazil",
        "India",
        "Peru",
        "United Kingdom",
        "China",
        "Nepal",
    ]

    scatter_df["display_name"] = scatter_df.apply(
        lambda x: x["location"] if x["location"] in notable else "", axis=1
    )

    fig = px.scatter(
        scatter_df,
        x="gdp_per_capita",
        y="total_deaths_per_million",
        size="population",
        color="continent",
        hover_name="location",
        text="display_name",
        size_max=60,
        title="<b>GDP per Capita vs. Total Deaths per Million</b><br><sup>Bubble size represents total population</sup>",
        labels={
            "gdp_per_capita": "GDP per Capita (USD)",
            "total_deaths_per_million": "Total Deaths per Million",
            "continent": "Continent",
        },
        template="plotly_white",
    )

    fig.update_traces(
        textposition="top right",
        marker=dict(line=dict(width=0.5, color="white")),
        opacity=0.75,
    )

    fig.update_layout(
        xaxis=dict(tickformat="$,.0f", gridcolor="lightgray"),
        yaxis=dict(gridcolor="lightgray"),
        legend=dict(title="Continent", yanchor="top", y=0.99, xanchor="left", x=0.99),
        margin=dict(l=50, r=50, t=100, b=50),
        height=700,
    )

    return fig
