from utils.kpi import create_kpi_card
from components.histograms import create_reproduction_dist
from components.bar_plots import create_top_countries_death, create_resilience_chart
from components.heatmaps import create_correlation_heatmap
from components.scatter_plots import (
    create_gdp_mortality_bubble,
)
from components.choropleths import create_deaths_per_mill_map
from components.line_graphs import (
    create_policy_vax_mortality_chart,
    create_cases_death_chart,
    create_continent_stacked_area,
    create_cfr_trend_chart,
)
from dash import Dash, html, dcc, callback, Output, Input, callback_context
import dash_bootstrap_components as dbc

from utils.data_engine import load_data

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.LUX,
    ],
    assets_folder="./static",
)
df, monthly_global, snapshot, pivot_cases = load_data()

# static graphs that don't need interactivity
top_deaths = create_top_countries_death(snapshot)

app.layout = dbc.Container(
    [
        # Header with controls
        html.Div(
            [
                dbc.Button(
                    "☰",
                    id="sidebar-toggle",
                    color="light",
                    outline=True,
                    size="sm",
                    style={"fontSize": "20px", "width": "50px", "height": "50px"},
                ),
                html.H1(
                    "COVID-19 Global Dashboard",
                    className="mb-0",
                    style={"fontWeight": "700", "color": "#2c3e50"},
                ),
                dcc.Dropdown(
                    df["location"].unique(),
                    value="Nepal",
                    id="country-dropdown",
                    style={
                        "width": "250px",
                        "fontSize": "14px",
                    },
                    clearable=False,
                    className="shadow-sm",
                    searchable=True,
                    maxHeight=400,
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "padding": "20px 0",
            },
            className="mb-4",
        ),
        dbc.Row(
            [
                # Sidebar
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H5("Navigation", className="mb-4 fw-bold"),
                                        dbc.Nav(
                                            [
                                                dbc.NavLink(
                                                    "Country Analysis",
                                                    href="#",
                                                    id="nav-country",
                                                    active=True,
                                                    className="mb-2",
                                                    style={"fontSize": "16px"},
                                                ),
                                                dbc.NavLink(
                                                    "Global Insights",
                                                    href="#",
                                                    id="nav-global",
                                                    active=False,
                                                    className="mb-2",
                                                    style={"fontSize": "16px"},
                                                ),
                                            ],
                                            vertical=True,
                                            pills=True,
                                        ),
                                    ]
                                )
                            ],
                            className="shadow-sm sticky-top",
                            style={"top": "20px"},
                        ),
                    ],
                    width=12,
                    lg=3,
                    className="mb-4",
                    id="sidebar",
                    style={"display": "none"},
                ),
                # Main Content Area
                dbc.Col(
                    [
                        # Country Analysis Section
                        html.Div(
                            [
                                # KPI rows
                                dbc.Row(
                                    [
                                        create_kpi_card(
                                            "Case Fatality", "cfr-kpi", "danger"
                                        ),
                                        create_kpi_card(
                                            "Vaccination", "vax-kpi", "success"
                                        ),
                                        create_kpi_card(
                                            "ICU Stress", "stress-kpi", "warning"
                                        ),
                                        create_kpi_card(
                                            "Bed Capacity", "healthcare-kpi", "info"
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                # Tabbed Charts
                                dcc.Tabs(
                                    id="country-tabs",
                                    value="tab-overview",
                                    children=[
                                        dcc.Tab(
                                            label="Overview",
                                            value="tab-overview",
                                            children=[
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            dbc.Card(
                                                                [
                                                                    dbc.CardHeader(
                                                                        "Epidemiological Timeline",
                                                                        className="fw-bold",
                                                                    ),
                                                                    dbc.CardBody(
                                                                        dcc.Graph(
                                                                            id="covid-graph",
                                                                            style={
                                                                                "height": "500px"
                                                                            },
                                                                        )
                                                                    ),
                                                                ],
                                                                className="shadow-sm h-100",
                                                            ),
                                                            width=12,
                                                            lg=8,
                                                        ),
                                                        dbc.Col(
                                                            dbc.Card(
                                                                [
                                                                    dbc.CardHeader(
                                                                        "Health Resilience",
                                                                        className="fw-bold",
                                                                    ),
                                                                    dbc.CardBody(
                                                                        dcc.Graph(
                                                                            id="resilience",
                                                                            style={
                                                                                "height": "500px"
                                                                            },
                                                                        )
                                                                    ),
                                                                ],
                                                                className="shadow-sm h-100",
                                                            ),
                                                            width=12,
                                                            lg=4,
                                                        ),
                                                    ],
                                                    className="mb-3 g-3 mt-2",
                                                ),
                                            ],
                                        ),
                                        dcc.Tab(
                                            label="Policy & Mortality",
                                            value="tab-policy",
                                            children=[
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            dbc.Card(
                                                                [
                                                                    dbc.CardHeader(
                                                                        "Policy Stringency vs. Vaccination & Mortality",
                                                                        className="fw-bold",
                                                                    ),
                                                                    dbc.CardBody(
                                                                        dcc.Graph(
                                                                            id="policy-vax-mortality-graph",
                                                                            style={
                                                                                "height": "400px"
                                                                            },
                                                                        )
                                                                    ),
                                                                ],
                                                                className="shadow-sm h-100",
                                                            ),
                                                            width=12,
                                                            lg=6,
                                                        ),
                                                        dbc.Col(
                                                            dbc.Card(
                                                                [
                                                                    dbc.CardHeader(
                                                                        "Case Fatality Rate Trend",
                                                                        className="fw-bold",
                                                                    ),
                                                                    dbc.CardBody(
                                                                        dcc.Graph(
                                                                            id="cfr-cumulative-chart",
                                                                            style={
                                                                                "height": "400px"
                                                                            },
                                                                        )
                                                                    ),
                                                                ],
                                                                className="shadow-sm h-100",
                                                            ),
                                                            width=12,
                                                            lg=6,
                                                        ),
                                                    ],
                                                    className="mb-3 g-3 mt-2",
                                                ),
                                            ],
                                        ),
                                        dcc.Tab(
                                            label="Reproduction Rate",
                                            value="tab-reproduction",
                                            children=[
                                                dbc.Row(
                                                    dbc.Col(
                                                        dbc.Card(
                                                            [
                                                                dbc.CardHeader(
                                                                    "Reproduction Rate Distribution",
                                                                    className="fw-bold",
                                                                ),
                                                                dbc.CardBody(
                                                                    dcc.Graph(
                                                                        id="reproduction-dist",
                                                                        style={
                                                                            "height": "450px"
                                                                        },
                                                                    )
                                                                ),
                                                            ],
                                                            className="shadow-sm",
                                                        ),
                                                        width=12,
                                                    ),
                                                    className="mb-3 mt-2",
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                            id="country-content",
                        ),
                        # Global Insights Section (initially hidden)
                        html.Div(
                            [
                                # Tabbed Global Charts
                                dcc.Tabs(
                                    id="global-tabs",
                                    value="tab-map",
                                    children=[
                                        dcc.Tab(
                                            label="Global Map",
                                            value="tab-map",
                                            children=[
                                                dbc.Row(
                                                    dbc.Col(
                                                        dbc.Card(
                                                            dbc.CardBody(
                                                                dcc.Graph(
                                                                    figure=create_deaths_per_mill_map(
                                                                        snapshot
                                                                    ),
                                                                    style={
                                                                        "height": "500px"
                                                                    },
                                                                ),
                                                            ),
                                                            className="shadow-sm",
                                                        ),
                                                        width=12,
                                                        className="mb-3",
                                                    ),
                                                    className="mt-2",
                                                ),
                                            ],
                                        ),
                                        dcc.Tab(
                                            label="Country Comparisons",
                                            value="tab-countries",
                                            children=[
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            dbc.Card(
                                                                [
                                                                    dbc.CardHeader(
                                                                        "Top Countries by Deaths",
                                                                        className="fw-bold",
                                                                    ),
                                                                    dbc.CardBody(
                                                                        dcc.Graph(
                                                                            figure=top_deaths,
                                                                            style={
                                                                                "height": "400px"
                                                                            },
                                                                        )
                                                                    ),
                                                                ],
                                                                className="shadow-sm h-100",
                                                            ),
                                                            width=12,
                                                            lg=6,
                                                            className="mb-3",
                                                        ),
                                                        dbc.Col(
                                                            dbc.Card(
                                                                [
                                                                    dbc.CardHeader(
                                                                        "Correlation Heatmap",
                                                                        className="fw-bold",
                                                                    ),
                                                                    dbc.CardBody(
                                                                        dcc.Graph(
                                                                            figure=create_correlation_heatmap(
                                                                                snapshot
                                                                            ),
                                                                            style={
                                                                                "height": "400px"
                                                                            },
                                                                        )
                                                                    ),
                                                                ],
                                                                className="shadow-sm h-100",
                                                            ),
                                                            width=12,
                                                            lg=6,
                                                            className="mb-3",
                                                        ),
                                                    ],
                                                    className="g-3 mt-2",
                                                ),
                                            ],
                                        ),
                                        dcc.Tab(
                                            label="Continental Trends",
                                            value="tab-continents",
                                            children=[
                                                dbc.Row(
                                                    dbc.Col(
                                                        dbc.Card(
                                                            [
                                                                dbc.CardHeader(
                                                                    "Continental Stacked Area",
                                                                    className="fw-bold",
                                                                ),
                                                                dbc.CardBody(
                                                                    dcc.Graph(
                                                                        figure=create_continent_stacked_area(
                                                                            df
                                                                        ),
                                                                        style={
                                                                            "height": "450px"
                                                                        },
                                                                    )
                                                                ),
                                                            ],
                                                            className="shadow-sm",
                                                        ),
                                                        width=12,
                                                        className="mb-3",
                                                    ),
                                                    className="mt-2",
                                                ),
                                            ],
                                        ),
                                        dcc.Tab(
                                            label="GDP & Mortality",
                                            value="tab-gdp",
                                            children=[
                                                dbc.Row(
                                                    dbc.Col(
                                                        dbc.Card(
                                                            [
                                                                dbc.CardHeader(
                                                                    "GDP vs Mortality Bubble Chart",
                                                                    className="fw-bold",
                                                                ),
                                                                dbc.CardBody(
                                                                    dcc.Graph(
                                                                        figure=create_gdp_mortality_bubble(
                                                                            snapshot
                                                                        ),
                                                                        style={
                                                                            "height": "500px"
                                                                        },
                                                                    )
                                                                ),
                                                            ],
                                                            className="shadow-sm",
                                                        ),
                                                        width=12,
                                                        className="mb-3",
                                                    ),
                                                    className="mt-2",
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                            id="global-content",
                            style={"display": "none"},
                        ),
                    ],
                    width=12,
                    lg=12,
                    id="main-content",
                ),
            ]
        ),
        # Footer
        dbc.Row(
            dbc.Col(
                html.P(
                    "Data source: Our World in Data | Dashboard built with Plotly Dash",
                    className="text-center text-muted small my-4",
                )
            )
        ),
    ],
    fluid=True,
    style={"maxWidth": "1600px", "backgroundColor": "#f8f9fa", "padding": "20px"},
)


@callback(
    [
        Output("covid-graph", "figure"),
        Output("policy-vax-mortality-graph", "figure"),
        Output("reproduction-dist", "figure"),
        Output("cfr-kpi", "children"),
        Output("vax-kpi", "children"),
        Output("stress-kpi", "children"),
        Output("healthcare-kpi", "children"),
        Output("cfr-cumulative-chart", "figure"),
        Output("resilience", "figure"),
    ],
    Input("country-dropdown", "value"),
)
def update_country_charts(selected_country):
    filtered_data = df[df["location"] == selected_country]

    # Graphs
    fig1 = create_cases_death_chart(filtered_data, selected_country)
    fig2 = create_policy_vax_mortality_chart(filtered_data, selected_country)
    fig3 = create_reproduction_dist(filtered_data, selected_country)
    fig5 = create_cfr_trend_chart(filtered_data, selected_country)
    fig6 = create_resilience_chart(snapshot, selected_country)

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

    # Healthcare capacity
    beds_per_thousand = filtered_data["hospital_beds_per_thousand"].iloc[0]
    healthcare = f"{beds_per_thousand:.1f} beds/1k"

    return fig1, fig2, fig3, cfr, vax, stress, healthcare, fig5, fig6


@callback(
    [
        Output("sidebar", "style"),
        Output("main-content", "width"),
        Output("main-content", "lg"),
    ],
    [
        Input("sidebar-toggle", "n_clicks"),
    ],
    prevent_initial_call=False,
)
def toggle_sidebar(n_clicks):
    ctx = callback_context
    if not ctx.triggered:
        return {"display": "none"}, 12, 12

    if n_clicks and n_clicks % 2 == 1:
        return {}, 12, 9
    return {"display": "none"}, 12, 12


@callback(
    [
        Output("country-content", "style"),
        Output("global-content", "style"),
        Output("nav-country", "active"),
        Output("nav-global", "active"),
    ],
    [
        Input("nav-country", "n_clicks"),
        Input("nav-global", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def toggle_content(country_clicks, global_clicks):
    ctx = callback_context
    if not ctx.triggered:
        return {"display": "block"}, {"display": "none"}, True, False

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "nav-country":
        return {"display": "block"}, {"display": "none"}, True, False
    else:
        return {"display": "none"}, {"display": "block"}, False, True


if __name__ == "__main__":
    app.run(debug=True)
