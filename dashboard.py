import streamlit as st
from src.data_loader import load_data
from src.style import apply_theme
from src.sidebar import render_sidebar
from src.tabs import tab_overview, tab_time_series, tab_scores, tab_place_comparison, tab_statistics, tab_wordcloud, tab_engagement

st.set_page_config(page_title="TastePulse - Food Tourism Insights", layout="wide", page_icon="🍜")
apply_theme()

# TastePulse Header
st.markdown("# 🍜 TastePulse")
st.markdown("**Northern Malaysia Food Tourism Sentiment Analysis**")
st.markdown("---")

df = load_data("sentiment_results_score_clean.csv")
selected_place, date_range = render_sidebar(df)

filtered_df = df[df["place"] == selected_place]

tab1, tab2, tab4, tab6, tab7 = st.tabs([
    "📌 Overview", "📈 Time Series", "📊 Comparison", "☁️ Word Cloud", "📱 Engagement"
])

with tab1: tab_overview.render(df, selected_place)
with tab2: tab_time_series.render(filtered_df)
# with tab3: tab_scores.render(filtered_df)
with tab4: tab_place_comparison.render(df, date_range)
# with tab5: tab_statistics.render(filtered_df)
with tab6: tab_wordcloud.render(filtered_df)
with tab7: tab_engagement.render(filtered_df)
