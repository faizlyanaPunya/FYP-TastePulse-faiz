import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render(filtered_df):
    st.markdown("## 📈 Sentiment Trends Over Time")

    if filtered_df.empty:
        st.warning("⚠️ No data available for time series.")
        return
    
    if 'date' not in filtered_df.columns or filtered_df['date'].isna().all():
        st.warning("⚠️ Date column not available for time series analysis")
        return
    
    if 'sentiment_score' not in filtered_df.columns:
        st.warning("⚠️ Sentiment score column not available")
        return

    # Calculate average sentiment score by date
    ts_overall = filtered_df.groupby('date')['sentiment_score'].mean().reset_index()
    
    # Create line chart
    fig = px.line(
        ts_overall, 
        x='date', 
        y='sentiment_score', 
        labels={'date':'Date', 'sentiment_score':'Avg Score'},
        title='Sentiment Score Over Time'
    )
    
    fig.update_traces(
        line=dict(color='#10b981', width=3),
        hovertemplate='Date: %{x}<br>Avg Score: %{y:.4f}<extra></extra>'
    )
    
    fig.update_layout(
        height=450,
        template='plotly_white',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Display statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_score = filtered_df['sentiment_score'].mean()
        st.metric("Avg Sentiment Score", f"{avg_score:.4f}")
    
    with col2:
        max_score = filtered_df['sentiment_score'].max()
        st.metric("Max Score", f"{max_score:.4f}")
    
    with col3:
        min_score = filtered_df['sentiment_score'].min()
        st.metric("Min Score", f"{min_score:.4f}")