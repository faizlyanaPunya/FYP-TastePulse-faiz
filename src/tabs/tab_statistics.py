import streamlit as st

def render(filtered_df):
    st.markdown("## 📊 Detailed Statistics")

    if filtered_df.empty:
        st.warning("⚠️ No data available for statistics.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Sentiment Score", f"{filtered_df['sentiment_score'].mean():.3f}")
    col1.metric("Std Dev", f"{filtered_df['sentiment_score'].std():.3f}")
    col2.metric("Median Score", f"{filtered_df['sentiment_score'].median():.3f}")
    col2.metric("Range", f"{filtered_df['sentiment_score'].min():.3f} to {filtered_df['sentiment_score'].max():.3f}")
    date_range_days = (filtered_df['date'].max() - filtered_df['date'].min()).days
    col3.metric("Date Range", f"{date_range_days} days")
