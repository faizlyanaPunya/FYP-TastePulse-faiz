import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render(filtered_df):
    st.markdown("## 📈 Sentiment Trends Over Time")

    if filtered_df.empty:
        st.warning("⚠️ No data available for time series.")
        return

    ts_overall = filtered_df.groupby('date')['sentiment_score'].mean().reset_index()
    fig = px.line(ts_overall, x='date', y='sentiment_score', labels={'date':'Date', 'sentiment_score':'Avg Score'})
    fig.update_traces(line_color='#10b981', line_width=3)
    st.plotly_chart(fig, use_container_width=True)

    # window = st.slider("Moving Average Window (days)", 1, 30, 7)
    # ts_overall['ma'] = ts_overall['sentiment_score'].rolling(window).mean()

    # fig2 = go.Figure()
    # fig2.add_trace(go.Scatter(x=ts_overall['date'], y=ts_overall['sentiment_score'], name='Daily', line=dict(color='#86efac', width=1)))
    # fig2.add_trace(go.Scatter(x=ts_overall['date'], y=ts_overall['ma'], name=f'{window}-Day MA', line=dict(color='#10b981', width=3)))
    # st.plotly_chart(fig2, use_container_width=True)
