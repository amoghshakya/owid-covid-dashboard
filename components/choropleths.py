import plotly.express as px
import pandas as pd


def create_deaths_per_mill_map(data: pd.DataFrame):
    peak = data.groupby("location", as_index=False).agg(
        {
            "iso_code": "first",
            "total_deaths": "sum",
        }
    )
    fig = px.choropleth(
        peak,
        locations="iso_code",
        color="total_deaths",
        color_continuous_scale="YlOrRd",
        hover_name="location",
        title="Total Deaths by Country",
    )
    fig.update_layout(coloraxis_colorbar=dict(title="Total Deaths"))

    return fig
