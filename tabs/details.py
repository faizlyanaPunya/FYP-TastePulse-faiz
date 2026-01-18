import streamlit as st
import pandas as pd

def render(insight_df):
    """Render Details tab with additional insights and data preview"""
    
    st.markdown("### Additional Insights & Details")
    
    if insight_df.empty:
        st.warning("⚠️ No data available.")
        return
    
    st.markdown("#### 📊 Data Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Total Records:** ", len(insight_df))
        st.write("**Unique Places:** ", insight_df['place'].nunique())
        st.write("**Sentiment Classes:** ", insight_df['predicted_sentiment'].nunique())
    
    with col2:
        if 'date' in insight_df.columns and not insight_df['date'].isna().all():
            st.write("**Date Range:** ", f"{insight_df['date'].min().strftime('%Y-%m-%d')} to {insight_df['date'].max().strftime('%Y-%m-%d')}")
        if 'sentiment_score' in insight_df.columns:
            st.write("**Avg Score:** ", f"{insight_df['sentiment_score'].mean():.3f}")
            st.write("**Max Score:** ", f"{insight_df['sentiment_score'].max():.3f}")
            st.write("**Min Score:** ", f"{insight_df['sentiment_score'].min():.3f}")
    
    st.markdown("---")
    st.markdown("#### 📋 Full Dataset Preview")
    st.dataframe(insight_df[['place', 'sentiment', 'predicted_sentiment', 'text']].head(20), use_container_width=True)