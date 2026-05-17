# UPDATED FILE: dashboard.py - Chat with Data Advisor Q&A flow fixed
# Add this new tab to your existing dashboard

import streamlit as st

from src.style import apply_theme
from src.sidebar import render_sidebar, initialize_session_state
from src.tabs import (
    tab_overview, 
    tab_time_series, 
    tab_wordcloud, 
    tab_model_evaluation,
    tab_initiatives,
    tab_map,
    tab_influencer,
    tab_ai_insights  # AI-Powered Insights
)

st.set_page_config(page_title="TastePulse - Food Tourism Insights", layout="wide", page_icon="🥘")
apply_theme()

# Initialize session state for model training
initialize_session_state()

# TastePulse Header
st.markdown("""
    <h1>
        <span style='-webkit-text-fill-color: initial;'>🥘</span> TastePulse
        <span style='font-size: 15px; font-weight: 400; opacity: 0.75; margin-left: 12px; vertical-align: middle;'>
            Northern Malaysia Food Tourism Sentiment Analysis
        </span>
    </h1>
""", unsafe_allow_html=True)

# Render sidebar (handles file upload and model training)
selected_place, date_range = render_sidebar()

# Check if data is available (either uploaded or from training)
if st.session_state.get('test_df') is None:
    st.info("📤 **Please upload a CSV file and train models to get started**")
    st.markdown("""
    ### How to use this dashboard:
    1. **Upload your dataset** in the sidebar (CSV file with columns: `text`, `sentiment`, `sentiment score`, `place` , `bigrams` )
    2. **Select models** to train (Multinomial Naive Bayes and/or LSTM)
    3. **Click 'Train Models'** to train and generate insights
    4. **Explore the tabs** to view sentiment analysis results
    
    > 💡 The dashboard will use the test data (20% split) for all insights and visualizations.
    """)
    st.stop()

# Use test data for all insights
df = st.session_state.test_df

# Apply place filter
filtered_df = df[df["place"] == selected_place] if selected_place != "All Places" else df

# Apply date filter if date_range is provided and valid
if date_range is not None and len(date_range) == 2:
    import pandas as pd
    start_date = pd.to_datetime(date_range[0]).date()
    end_date = pd.to_datetime(date_range[1]).date()
    if 'date' in filtered_df.columns:
        # Convert df date column to date for accurate comparison
        df_dates = pd.to_datetime(filtered_df['date']).dt.date
        filtered_df = filtered_df[(df_dates >= start_date) & (df_dates <= end_date)]

# Display tabs with model evaluation and NEW initiatives tab
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 Overview",
    "📈 Time Series",
    "☁️ Word Cloud",
    "📱 Social & Influencers",
    "💡 Initiatives",
    "🗺️ Map Area",
    "🤖 AI Insights",
    "🖇️ About"
])

with tab1: 
    tab_overview.render(df, selected_place)
with tab2: 
    tab_time_series.render(filtered_df)
with tab3: 
    tab_wordcloud.render(filtered_df)
with tab4: 
    tab_influencer.render(filtered_df, selected_place)
with tab5:
    tab_initiatives.render(df, selected_place)
with tab6:
    tab_map.render(filtered_df, selected_place)
with tab7:
    tab_ai_insights.render(df)
with tab8:
    tab_model_evaluation.render(st.session_state.model_results)