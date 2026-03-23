import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def create_deaths_per_mill_map(data: pd.DataFrame):
    peak = data.groupby("location", as_index=False).agg(
        {
            "iso_code": "first",
            "total_deaths": "sum",
            "life_expectancy": "first",
        }
    )

    fig = go.Figure()

    fig.add_trace(
        go.Choropleth(
            locations=peak["iso_code"],
            z=peak["total_deaths"],
            text=peak["location"],
            colorscale="YlOrRd",
            colorbar_title="Total Deaths",
            visible=True,
        )
    )

    fig.add_trace(
        go.Choropleth(
            locations=peak["iso_code"],
            z=peak["life_expectancy"],
            text=peak["location"],
            colorscale="Viridis",
            colorbar_title="Life Expectancy",
            visible=False,
        )
    )

    fig.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        label="Total Deaths",
                        method="update",
                        args=[{"visible": [True, False]}],
                    ),
                    dict(
                        label="Life Expectancy",
                        method="update",
                        args=[{"visible": [False, True]}],
                    ),
                ],
                direction="down",
                showactive=True,
            )
        ],
        margin=dict(l=0, r=0, t=50, b=0),
    )

    return fig
