import streamlit as st
from src.plots import plot_overlap_timeseries

def render(df, date_range):
    st.markdown("## 🔄 Place Comparison")
    selected_places = st.multiselect("📍 Select Places (up to 5)", sorted(df["place"].unique()))

    if not selected_places:
        st.info("👆 Please select at least one place to compare")
        return

    if len(date_range) == 2:
        start_date, end_date = date_range
        comp_df_all = df[(df['date'] >= start_date) & (df['date'] <= end_date)].copy()
    else:
        comp_df_all = df.copy()

    PLACE_COLORS = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6']
    place_color_map = {p: PLACE_COLORS[i % len(PLACE_COLORS)] for i, p in enumerate(selected_places)}

    fig = plot_overlap_timeseries(comp_df_all, selected_places, place_color_map)
    st.plotly_chart(fig, use_container_width=True)
