import streamlit as st
from src.plots import plot_pie

def render(filtered_df):
    st.markdown("## 🎯 Average Sentiment Scores")
    st.markdown("### Model Confidence Analysis")

    if filtered_df.empty:
        st.warning("⚠️ No sentiment scores available.")
        return

    avg_scores = filtered_df[["positive","neutral","negative"]].mean()
    st.pyplot(plot_pie(avg_scores, ["Positive", "Neutral", "Negative"]))

    filtered_df["overall_score"] = filtered_df["positive"] - filtered_df["negative"]
    st.metric("🎯 Overall Score", f"{filtered_df['overall_score'].mean():.3f}")
