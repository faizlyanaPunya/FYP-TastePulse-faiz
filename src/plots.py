import matplotlib.pyplot as plt
import plotly.express as px

SENTIMENT_COLORS = ["#10b981", "#86efac", "#64748b"]

def plot_pie(values, labels, title=""):
    fig, ax = plt.subplots(figsize=(5, 5), facecolor="none")
    ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=SENTIMENT_COLORS,
        wedgeprops={"edgecolor": "white", "linewidth": 3}
    )
    ax.axis("equal")
    return fig


def plot_overlap_timeseries(df, selected_places, place_color_map):
    ts = (
        df.groupby(["date", "place"], as_index=False)["sentiment_score"]
        .mean()
    )

    fig = px.line(
        ts[ts["place"].isin(selected_places)],
        x="date",
        y="sentiment_score",
        color="place",
        color_discrete_map=place_color_map
    )

    fig.update_traces(mode="lines", connectgaps=True)
    return fig
