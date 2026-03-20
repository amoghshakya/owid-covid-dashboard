from components.bar_plots import create_country_completeness_bar
from components.heatmaps import create_correlation_heatmap
from components.box_plots import create_hospital_capacity_boxplot
from components.scatter_plots import create_global_resilience_scatter
from components.choropleths import create_deaths_per_mill_map
from components.line_graphs import (
    create_policy_vax_mortality_chart,
    create_cases_death_chart,
)
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd

from utils.data_engine import load_data

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
data = load_data()

# static graphs that don't need interactivity
fig_map = create_deaths_per_mill_map(data)
fig_scatter = create_global_resilience_scatter(data)
fig_heatmap = create_correlation_heatmap(data)

app.layout = dbc.Container(
    [
        # Header
        dbc.Row(
            dbc.Col(
                html.H1(
                    "COVID-19 Global Health Resilience", className="text-center my-4"
                )
            )
        ),
        # kpis
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [html.H5("Case Fatality Rate"), html.H3(id="cfr-kpi")]
                        ),
                        color="danger",
                        inverse=True,
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([html.H5("Vax Coverage"), html.H3(id="vax-kpi")]),
                        color="success",
                        inverse=True,
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [html.H5("Hospital Stress"), html.H3(id="stress-kpi")]
                        ),
                        color="warning",
                        inverse=True,
                    )
                ),
            ],
            className="mb-4",
        ),
        # visualizations begin here
        dbc.Row(
            [
                html.Label("Select Country Analysis:"),
                dcc.Dropdown(data["location"].unique(), "Nepal", id="country-dropdown"),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id="covid-graph"),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="pol-vax-death-graph"),
                    ],
                    width=6,
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig_scatter), width=6),  # Static
                dbc.Col(
                    [dcc.Graph(figure=create_hospital_capacity_boxplot(data))],
                    width=6,
                ),
            ]
        ),
        dcc.Graph(figure=fig_heatmap, id="correlation-heatmap"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Hr(),
                        html.H4("Technical Audit: Global Data Reliability"),
                        dcc.Graph(
                            id="data-completness",
                        ),
                    ],
                    width=12,
                )
            ],
            className="mt-5 mb-5",
        ),
    ],
    fluid=True,
)


@callback(
    [
        Output("covid-graph", "figure"),
        Output("pol-vax-death-graph", "figure"),
        Output("data-completness", "figure"),
        Output("cfr-kpi", "children"),
        Output("vax-kpi", "children"),
        Output("stress-kpi", "children"),
    ],
    Input("country-dropdown", "value"),
)
def update_country_charts(selected_country):
    filtered_data = data[data["location"] == selected_country]

    # Graphs
    fig1 = create_cases_death_chart(filtered_data, selected_country)
    fig2 = create_policy_vax_mortality_chart(filtered_data, selected_country)
    fig3 = create_country_completeness_bar(filtered_data, selected_country)

    latest = filtered_data.dropna(subset=["total_cases", "total_deaths"]).iloc[-1]

    cfr = f"{(latest['total_deaths'] / latest['total_cases']) * 100:.2f}%"

    vax_val = latest.get("people_fully_vaccinated_per_hundred")
    vax = f"{vax_val:.1f}%" if pd.notnull(vax_val) else "N/A"

    stress_val = latest.get("icu_patients_per_million")
    stress = f"{stress_val:.1f}" if pd.notnull(stress_val) else "N/A"

    return fig1, fig2, fig3, cfr, vax, stress


if __name__ == "__main__":
    app.run(debug=True)
