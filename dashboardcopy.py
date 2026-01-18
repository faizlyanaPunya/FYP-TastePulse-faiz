import streamlit as st
import pandas as pd
from tabs.sidebar import render_sidebar, initialize_session_state
from tabs.overview import render as render_overview
from tabs.model_evaluation import render as render_model_evaluation
from tabs.time_series import render as render_time_series
from tabs.details import render as render_details

st.set_page_config(page_title="TastePulse - Food Tourism Insights", layout="wide", page_icon="🍜")

st.markdown("## 🍜 TastePulse")
st.markdown("**Northern Malaysia Food Tourism Sentiment Analysis**")

# Initialize session state
initialize_session_state()

# Render sidebar
render_sidebar()

# Main content
df = st.session_state.df

if df is None:
    st.info("📤 Please upload a CSV file to get started")
    st.stop()

required_cols = {"sentiment", "place", "text"}
if not required_cols.issubset(set(df.columns)):
    st.error(f"❌ Dataset must contain columns: {required_cols}")
    st.stop()

# Convert date if exists
if 'createTimeISO' in df.columns:
    df['date'] = pd.to_datetime(df['createTimeISO'], errors='coerce')
elif 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Filter data by selected place
if st.session_state.selected_place == "All Places":
    filtered_df = df.copy()
else:
    filtered_df = df[df['place'] == st.session_state.selected_place].copy()

# Display place info
st.markdown(f"### 📍 {st.session_state.selected_place}")
st.write(f"Total reviews: **{len(filtered_df)}**")

# Display tabs if models are trained
if st.session_state.models_trained and st.session_state.model_results:
    
    # Get the first trained model's predictions and test data
    first_model = list(st.session_state.model_results.keys())[0]
    y_test = st.session_state.model_results[first_model]['y_test']
    y_pred = st.session_state.model_results[first_model]['y_pred']
    
    # Create insight dataframe with predictions from the original data
    insight_df = df[df.index.isin(y_test.index)].copy()
    insight_df['predicted_sentiment'] = y_pred
    insight_df['true_sentiment'] = y_test.values
    
    # Now filter the insight_df by selected place
    if st.session_state.selected_place != "All Places":
        insight_df = insight_df[insight_df['place'] == st.session_state.selected_place].copy()
    
    insights_tab1, insights_tab2, insights_tab3, insights_tab4 = st.tabs(
        ["📌 Overview", "🔍 Model Evaluation", "📈 Time Series", "📋 Details"]
    )
    
    with insights_tab1:
        render_overview(insight_df)
    
    with insights_tab2:
        render_model_evaluation(st.session_state.model_results)
    
    with insights_tab3:
        render_time_series(insight_df)
    
    with insights_tab4:
        render_details(insight_df)

else:
    st.info("👆 Select models and click 'Train Models' in the sidebar to see results")