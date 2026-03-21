import plotly.graph_objects as go
import pandas as pd


def create_reproduction_dist(df: pd.DataFrame, selected_country: str):
    r_vals = df["reproduction_rate"].dropna()
    r_vals = r_vals[(r_vals > 0) & (r_vals < 3)]  # Clipped at 3 for better visibility

    fig = go.Figure()

    # need to create two separate traces for this
    fig.add_trace(
        go.Histogram(
            x=r_vals[r_vals < 1],
            nbinsx=40,
            name="Controlled (R < 1)",
            marker_color="#2ecc71",
            opacity=0.75,
        )
    )

    fig.add_trace(
        go.Histogram(
            x=r_vals[r_vals >= 1],
            nbinsx=40,
            name="Spreading (R > 1)",
            marker_color="#e74c3c",
            opacity=0.75,
        )
    )

    fig.add_vline(
        x=1.0,
        line_dash="dash",
        line_color="black",
        annotation_text="Threshold (R=1)",
        annotation_position="top left",
    )
    fig.add_vline(
        x=r_vals.mean(),
        line_color="orange",
        annotation_text=f"Mean: {r_vals.mean():.2f}",
        annotation_position="bottom right",
        annotation_yshift=10,
    )

    fig.update_layout(
        title=f"<b>Distribution of Reproduction Rate (R): {selected_country}</b>",
        xaxis_title="Reproduction Rate (R)",
        yaxis_title="Frequency (Observations)",
        barmode="overlay",
        template="plotly_white",
        showlegend=True,
    )

    return fig
