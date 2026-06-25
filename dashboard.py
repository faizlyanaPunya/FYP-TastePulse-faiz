# UPDATED FILE: dashboard.py - Chat with Data Advisor Q&A flow fixed
# Add this new tab to your existing dashboard

import streamlit as st

from src.style import apply_theme
from src.sidebar import render_sidebar, initialize_session_state
from src.tabs import (
    tab_overview, 
    tab_time_series, 
    tab_wordcloud, 
    tab_about,
    tab_initiatives,
    tab_map,
    tab_influencer,
    tab_ai_insights  # AI-Powered Insights
)

from PIL import Image
import base64

try:
    logo_img = Image.open("assets/TastePulse_Logo_Faiz.jpeg")
    with open("assets/TastePulse_Logo_Faiz.jpeg", "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode("utf-8")
    logo_html = f"<img src='data:image/jpeg;base64,{logo_b64}' style='width: 48px; height: 48px; border-radius: 12px; object-fit: cover; box-shadow: 0 4px 12px rgba(0,0,0,0.15); vertical-align: middle; margin-right: 12px;' />"
except Exception:
    logo_img = None
    logo_html = "<span style='font-weight: 900; color: #00838F; padding-right: 12px;'>TP</span>"

st.set_page_config(page_title="TastePulse - Food Tourism Insights", layout="wide", page_icon=logo_img)
apply_theme()

# Initialize session state for model training
initialize_session_state()

# TastePulse Header
st.markdown(f"""
    <h1 style='display: flex; align-items: center; padding-left: 25px;'>
        {logo_html}
        <span>
            TastePulse
            <span style='font-size: 15px; font-weight: 400; opacity: 0.90; margin-left: 12px; vertical-align: middle;'>
                Northern Malaysia Food Tourism Sentiment Analysis
            </span>
        </span>
    </h1>
""", unsafe_allow_html=True)


# Render sidebar (handles file upload and model training)
selected_place, date_range = render_sidebar()

# Check if data is available (either uploaded or from training)
if st.session_state.get('test_df') is None:
    st.info("👈 **Please upload a CSV dataset in the left sidebar to get started!**")
    
    # Visual Onboarding Guide
    st.markdown("""
    ### 🚀 Quick Start Guide
    
    To begin exploring the sentiment analysis insights:
    
    1. **Locate the Left Sidebar:** 
       * If you are on a mobile device or the sidebar is hidden, click the **`>`** arrow in the top-left corner of the screen to open it.
    2. **Upload the Dataset:**
       * In the sidebar, drag and drop or upload your CSV dataset file.
       * *Don't have a dataset?* You can download our sample dataset here:
         👉 [**Download Sample Dataset (Sentiment_Food_Data.csv)**](https://raw.githubusercontent.com/faizlyanaPunya/FYP-TastePulse-faiz/main/Sentiment_Food_Data.csv)
    3. **Select & Train Models:**
       * Choose the models you'd like to train (e.g., *Multinomial Naive Bayes* and/or *LSTM*).
       * Click the **"Train Models"** button.
    4. **Explore Insights:**
       * Once loaded, navigate through the tabs above to explore reviews, geographical maps, influencer reach, and AI-powered operational advisories!
    
    ---
    ### 📋 Dataset Column Requirements
    Your uploaded CSV must contain these columns:
    * `text` (Review content)
    * `sentiment` (`positive`, `negative`, or `neutral`)
    * `sentiment score` (Decimal value)
    * `place` (Restaurant or location name)
    * `bigrams` (Extracted key phrases)
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
    tab_about.render(st.session_state.model_results)