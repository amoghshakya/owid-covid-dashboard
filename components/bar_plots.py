import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def create_country_completeness_bar(filtered_data: pd.DataFrame, country_name: str):
    key_vars = [
        "total_deaths_per_million",
        "stringency_index",
        "icu_patients_per_million",
        "people_fully_vaccinated_per_hundred",
        "hospital_beds_per_thousand",
    ]

    completeness = (filtered_data[key_vars].notnull().mean() * 100).reset_index()
    completeness.columns = ["Variable", "Completeness"]

    fig = px.bar(
        completeness,
        x="Completeness",
        y="Variable",
        orientation="h",
        text_auto=".1f",
        title=f"Data Reporting Reliability: {country_name}",
        color="Completeness",
        color_continuous_scale="RdYlGn",
        range_x=[0, 100],
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Data Presence (%)",
        yaxis_title="",
        showlegend=False,
    )

    return fig


def create_top_countries_death(df: pd.DataFrame):
    """
    Takes snapshot dataframe and creates a horizontal bar chart of the top 15 countries by total deaths per million.

    Params:
        df: pd.DataFrame - snapshot dataframe with latest data for each country
    Returns:
    fig: plotly.graph_objects.Figure - horizontal bar chart of top 15 countries by total deaths per million
    """
    top15 = (
        df.nlargest(15, "total_deaths")
        .copy()
        .sort_values("total_deaths", ascending=False)
    )
    continent_colors = {
        "North America": "#e74c3c",
        "South America": "#e67e22",
        "Europe": "#3498db",
        "Asia": "#2ecc71",
        "Africa": "#9b59b6",
        "Oceania": "#1abc9c",
    }

    fig = px.bar(
        top15,
        x="total_deaths",
        y="location",
        orientation="h",
        color="continent",
        color_discrete_map=continent_colors,
        text="total_deaths",  # This allows us to format the labels on the bars
        title="<b>Top 15 Countries by Total COVID-19 Deaths</b>",
        labels={
            "total_deaths": "Total Deaths",
            "location": "Country",
            "continent": "Continent",
        },
        template="plotly_white",
    )
    fig.update_traces(
        texttemplate="%{x:,.2f}M",
        textposition="outside",
        marker_line_color="white",
        marker_line_width=0.5,
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Total Deaths per Million",
        yaxis_title="Country",
    )
    fig.update_xaxes(
        tickformat=".2s",
    )
    return fig


def create_resilience_chart(snapshot: pd.DataFrame, selected_country: str):
    """
    Takes snapshot df
    Vertical bar comparing country Life Expectancy vs Global Average
    """
    country_val = snapshot[snapshot["location"] == selected_country][
        "life_expectancy"
    ].values[0]
    global_avg = snapshot["life_expectancy"].mean()

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=[selected_country],
            y=[country_val],
            orientation="v",
            marker_color="#3498db",
            name=selected_country,
            text=f"{country_val:.1f} Years",
            textposition="auto",
            width=0.4,
        )
    )

    fig.add_hline(
        y=global_avg,
        line_dash="dash",
        line_color="red",
        line_width=2,
        annotation_text=f"Global Avg: {global_avg:.1f}",
        annotation_position="top left",
    )

    fig.update_layout(
        title=f"<b>Life Expectancy Resilience: {selected_country}</b>",
        xaxis_title="",
        yaxis_title="Life Expectancy (Years)",
        yaxis=dict(range=[50, 95]),
        template="plotly_white",
        margin=dict(l=50, r=50, t=80, b=50),
    )

    return fig
