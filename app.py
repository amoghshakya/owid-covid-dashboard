from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px

from utils.data_engine import load_data

app = Dash()

data = load_data()

app.layout = [
    html.H1("COVID-19 Data Visualization"),
    dcc.Dropdown(data["location"].unique(), "Nepal", id="country-dropdown"),
    dcc.Graph(id="covid-graph"),
]


@callback(
    Output("covid-graph", "figure"),
    Input("country-dropdown", "value"),
)
def update_graph(selected_country):
    filtered_data = data[data["location"] == selected_country]
    fig = px.line(
        filtered_data,
        x="date",
        y="new_cases_smoothed",
        title="Average Daily New COVID-19 Cases",
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="New Cases (7-day average)",
    )
    return fig


if __name__ == "__main__":
    # TODO: remove debug
    app.run(debug=True)
