import plotly.express as px


def create_global_resilience_scatter(data):
    # Get the latest data point for EVERY country
    latest_global = data.groupby("location").tail(1)
    latest_global["gdp_per_capita"] = latest_global["gdp_per_capita"].fillna(0)

    latest_global = latest_global.dropna(
        subset=["people_fully_vaccinated_per_hundred", "total_deaths_per_million"]
    )

    fig = px.scatter(
        latest_global,
        x="people_fully_vaccinated_per_hundred",
        y="total_deaths_per_million",
        size="gdp_per_capita",
        color="continent",
        hover_name="location",
        title="Global Resilience: Vaccination vs. Mortality (Weighted by GDP)",
        labels={
            "people_fully_vaccinated_per_hundred": "Vaccination Coverage (%)",
            "total_deaths_per_million": "Total Deaths per Million",
        },
    )

    fig.update_layout(template="plotly_white")
    return fig
