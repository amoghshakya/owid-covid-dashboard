from dash import html
import dash_bootstrap_components as dbc


def create_kpi_card(title, id_name, color):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.H6(title, className=f"text-white-50 mb-2"),
                    html.H3(id=id_name, className="mb-0 fw-bold"),
                ]
            ),
            color=color,
            inverse=True,
            className="shadow-sm text-center",
        ),
        width=12,
        md=3,
    )
