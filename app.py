from components.histograms import create_reproduction_dist
from components.bar_plots import (
    create_country_completeness_bar,
    create_top_countries_death,
)
from components.heatmaps import create_correlation_heatmap
from components.box_plots import create_hospital_capacity_boxplot
from components.scatter_plots import (
    create_gdp_mortality_bubble,
)
from components.choropleths import create_deaths_per_mill_map
from components.line_graphs import (
    create_policy_vax_mortality_chart,
    create_cases_death_chart,
    create_continent_stacked_area,
)
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd

from utils.data_engine import load_data

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
df, monthly_global, snapshot, pivot_cases = load_data()

# static graphs that don't need interactivity
top_deaths = create_top_countries_death(snapshot)

app.layout = dbc.Container(
    [
        # Header with subtitle
        dbc.Row(
            dbc.Col(
                [
                    html.H1(
                        "COVID-19 Global Health Resilience",
                        className="text-center mt-4 mb-2",
                        style={"fontWeight": "700", "color": "#2c3e50"},
                    ),
                    html.P(
                        "Interactive dashboard for tracking pandemic trends and health system resilience",
                        className="text-center text-muted mb-4",
                    ),
                ]
            )
        ),
        # Country Selector Card
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.Label(
                                    "Select Country:",
                                    className="fw-bold mb-2",
                                    style={"fontSize": "16px"},
                                ),
                                dcc.Dropdown(
                                    df["location"].unique(),
                                    "Nepal",
                                    id="country-dropdown",
                                    style={"fontSize": "14px"},
                                    clearable=False,
                                ),
                            ]
                        )
                    ],
                    className="shadow-sm mb-4",
                ),
                width=12,
            )
        ),
        # KPIs Row
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6(
                                    "Case Fatality Rate", className="text-white-50 mb-2"
                                ),
                                html.H2(id="cfr-kpi", className="mb-0 fw-bold"),
                            ]
                        ),
                        color="danger",
                        inverse=True,
                        className="shadow-sm text-center h-100",
                    ),
                    width=12,
                    lg=4,
                    className="mb-3 mb-lg-0",
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6(
                                    "Vaccination Coverage",
                                    className="text-white-50 mb-2",
                                ),
                                html.H2(id="vax-kpi", className="mb-0 fw-bold"),
                            ]
                        ),
                        color="success",
                        inverse=True,
                        className="shadow-sm text-center h-100",
                    ),
                    width=12,
                    lg=4,
                    className="mb-3 mb-lg-0",
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6(
                                    "Hospital Stress", className="text-white-50 mb-2"
                                ),
                                html.H2(id="stress-kpi", className="mb-0 fw-bold"),
                            ]
                        ),
                        color="warning",
                        inverse=True,
                        className="shadow-sm text-center h-100",
                    ),
                    width=12,
                    lg=4,
                    className="mb-3 mb-lg-0",
                ),
            ],
            className="mb-5",
        ),
        # Country-Level Analysis Section
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H4(
                            "Country-Level Analysis",
                            className="mb-3",
                            style={"fontWeight": "600", "color": "#2c3e50"},
                        ),
                        html.Hr(className="mb-4"),
                    ]
                )
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Graph(
                                id="covid-graph",
                                config={"displayModeBar": False},
                                style={"height": "400px"},
                            )
                        ),
                        className="shadow-sm",
                    ),
                    width=12,
                    lg=6,
                    className="mb-4",
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Graph(
                                id="policy-vax-mortality-graph",
                                config={"displayModeBar": False},
                                style={"height": "400px"},
                            )
                        ),
                        className="shadow-sm",
                    ),
                    width=12,
                    lg=6,
                    className="mb-4",
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(
                            id="reproduction-dist",
                            config={"displayModeBar": False},
                            style={"height": "400px"},
                        )
                    ),
                    className="shadow-sm",
                ),
                width=12,
                className="mb-5",
            )
        ),
        # Global Insights Section
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H4(
                            "Global Insights",
                            className="mb-3",
                            style={"fontWeight": "600", "color": "#2c3e50"},
                        ),
                        html.Hr(className="mb-4"),
                    ]
                )
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Graph(
                                figure=top_deaths,
                                config={"displayModeBar": False},
                                style={"height": "400px"},
                            )
                        ),
                        className="shadow-sm",
                    ),
                    width=12,
                    lg=6,
                    className="mb-4",
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Graph(
                                figure=create_correlation_heatmap(snapshot),
                                config={"displayModeBar": False},
                                style={"height": "400px"},
                            )
                        ),
                        className="shadow-sm",
                    ),
                    width=12,
                    lg=6,
                    className="mb-4",
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(
                            figure=create_gdp_mortality_bubble(snapshot),
                            config={"displayModeBar": False},
                            style={"height": "500px"},
                        )
                    ),
                    className="shadow-sm",
                ),
                width=12,
                className="mb-4",
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(
                            figure=create_continent_stacked_area(df),
                            config={"displayModeBar": False},
                            style={"height": "450px"},
                        )
                    ),
                    className="shadow-sm",
                ),
                width=12,
                className="mb-5",
            )
        ),
        # Footer
        dbc.Row(
            dbc.Col(
                html.Div(
                    html.P(
                        "Data source: Our World in Data | Dashboard built with Plotly Dash",
                        className="text-center text-muted small mb-4",
                    )
                )
            )
        ),
    ],
    fluid=True,
    style={"maxWidth": "1400px", "backgroundColor": "#f8f9fa", "padding": "20px"},
)


@callback(
    [
        Output("covid-graph", "figure"),
        Output("policy-vax-mortality-graph", "figure"),
        Output("reproduction-dist", "figure"),
        Output("cfr-kpi", "children"),
        Output("vax-kpi", "children"),
        Output("stress-kpi", "children"),
    ],
    Input("country-dropdown", "value"),
)
def update_country_charts(selected_country):
    filtered_data = df[df["location"] == selected_country]

    # Graphs
    fig1 = create_cases_death_chart(filtered_data, selected_country)
    fig2 = create_policy_vax_mortality_chart(filtered_data, selected_country)
    fig3 = create_reproduction_dist(filtered_data, selected_country)

    latest = filtered_data.dropna(subset=["total_cases", "total_deaths"]).iloc[-1]

    cfr = f"{latest['case_fatality_rate']:.2f}%"

    vax_val = filtered_data["people_fully_vaccinated_per_hundred"].dropna()
    vax = f"{vax_val.iloc[-1]:.1f}%" if len(vax_val) > 0 else "N/A"

    stress_val = filtered_data.get("icu_patients_per_million")
    if stress_val is not None:
        stress_val_clean = stress_val.dropna()
        stress = (
            f"{stress_val_clean.iloc[-1]:.1f}" if len(stress_val_clean) > 0 else "N/A"
        )
    else:
        stress = "N/A"

    return fig1, fig2, fig3, cfr, vax, stress


if __name__ == "__main__":
    app.run(debug=True)
