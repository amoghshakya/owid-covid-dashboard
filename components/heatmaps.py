import plotly.express as px
import pandas as pd


def create_correlation_heatmap(snapshot_data: pd.DataFrame):
    corr_cols = {
        "total_deaths_per_million": "Deaths/Million",
        "case_fatality_rate": "Case Fatality %",
        "gdp_per_capita": "GDP per Capita",
        "life_expectancy": "Life Expectancy",
        "human_development_index": "HDI",
        "median_age": "Median Age",
        "hospital_beds_per_thousand": "Hospital Beds/1k",
        "diabetes_prevalence": "Diabetes %",
        "cardiovasc_death_rate": "Cardiovasc. Death Rate",
        "population_density": "Pop. Density",
    }

    available_cols = [c for c in corr_cols.keys() if c in snapshot_data.columns]
    corr_df = snapshot_data[available_cols].copy()
    corr_df.rename(columns=corr_cols, inplace=True)

    corr_matrix = corr_df.corr()

    # Apply the Triangle Mask (Equivalent to np.triu)
    # Plotly doesn't have a "mask" argument, so we manually set half to NaN
    # mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    # df_masked = corr_matrix.mask(mask)

    fig = px.imshow(
        corr_matrix,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdYlGn",
        zmin=-1,
        zmax=1,
        title="<b>Correlation Heatmap — COVID-19 & Socioeconomic Variables</b>",
        labels=dict(color="Correlation"),
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_tickangle=-35,
        margin=dict(l=50, r=50, t=80, b=50),
        hoverlabel=dict(bgcolor="white", font_size=12),
    )

    return fig
