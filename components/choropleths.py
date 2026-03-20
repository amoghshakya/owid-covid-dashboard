import plotly.express as px
import pandas as pd


def create_deaths_per_mill_map(data: pd.DataFrame):
    peak = data.groupby("location", as_index=False).agg(
        {
            "iso_code": "first",
            "total_deaths_per_million": "max",
        }
    )
    fig = px.choropleth(
        peak,
        locations="iso_code",
        color="total_deaths_per_million",
        hover_name="location",
        title="Total Deaths per Million by Country",
    )
    fig.update_layout(legend_title_text="Total Deaths per Million")

    return fig
