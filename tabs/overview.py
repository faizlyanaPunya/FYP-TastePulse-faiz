import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def render(insight_df):
    """Render Overview tab with sentiment distribution and top places"""
    
    st.markdown("### Overview - Test Data Insights (20%)")
    
    if insight_df.empty:
        st.warning("⚠️ No data available.")
        return
    
    # Key Metrics Cards
    st.markdown("#### 📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Reviews", len(insight_df))
    
    with col2:
        if 'date' in insight_df.columns:
            date_range = f"{insight_df['date'].min().strftime('%Y-%m-%d')} to {insight_df['date'].max().strftime('%Y-%m-%d')}"
        else:
            date_range = "N/A"
        st.metric("Date Range", date_range)
    
    with col3:
        st.metric("Number of Places", insight_df['place'].nunique())
    
    with col4:
        if 'sentiment_score' in insight_df.columns:
            avg_score = insight_df['sentiment_score'].mean()
            st.metric("Avg Sentiment Score", f"{avg_score:.2f}")
        else:
            st.metric("Avg Sentiment Score", "N/A")
    
    st.markdown("---")
    
    # Sentiment Distribution (Pie Chart)
    st.markdown("#### 🎯 Sentiment Distribution")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        sentiment_counts = insight_df['predicted_sentiment'].value_counts()
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=sentiment_counts.index,
            values=sentiment_counts.values,
            textposition='inside',
            textinfo='label+percent',
            marker=dict(colors=['#FF6B6B', '#4ECDC4', '#FFE66D'])
        )])
        
        fig_pie.update_layout(
            title="Sentiment Distribution",
            height=400
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("#### Summary")
        for sentiment, count in sentiment_counts.items():
            pct = (count / len(insight_df) * 100)
            st.write(f"**{sentiment}**: {count} ({pct:.1f}%)")
    
    st.markdown("---")
    
    # Sentiment Summary Table
    st.markdown("#### 📋 Sentiment Summary Table")
    
    summary_data = []
    for sentiment in insight_df['predicted_sentiment'].unique():
        sentiment_data = insight_df[insight_df['predicted_sentiment'] == sentiment]
        count = len(sentiment_data)
        pct = (count / len(insight_df) * 100)
        
        if 'sentiment_score' in insight_df.columns:
            avg_score = sentiment_data['sentiment_score'].mean()
        else:
            avg_score = 0
        
        summary_data.append({
            'Sentiment': sentiment,
            'Count': count,
            'Percentage': f"{pct:.1f}%",
            'Avg Score': f"{avg_score:.3f}"
        })
    
    summary_table = pd.DataFrame(summary_data)
    st.dataframe(summary_table, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Top 5 Places by Review Count
    st.markdown("#### 🏆 Top 5 Places by Review Count")
    
    top_places = insight_df['place'].value_counts().head(5)
    
    top_places_data = []
    for place in top_places.index:
        place_data = insight_df[insight_df['place'] == place]
        total = len(place_data)
        positive = len(place_data[place_data['predicted_sentiment'].str.lower() == 'positive'])
        negative = len(place_data[place_data['predicted_sentiment'].str.lower() == 'negative'])
        neutral = len(place_data[place_data['predicted_sentiment'].str.lower() == 'neutral'])
        positive_pct = (positive / total * 100) if total > 0 else 0
        
        top_places_data.append({
            'Place': place,
            'Total Reviews': total,
            'Positive': positive,
            'Negative': negative,
            'Neutral': neutral,
            'Positive %': f"{positive_pct:.1f}%"
        })
    
    top_places_df = pd.DataFrame(top_places_data)
    st.dataframe(top_places_df, use_container_width=True, hide_index=True)
    
    # Bar chart for top places
    col1, col2 = st.columns(2)
    
    with col1:
        fig_places = go.Figure(data=[
            go.Bar(
                x=top_places.index,
                y=top_places.values,
                marker_color='#4ECDC4',
                text=top_places.values,
                textposition='auto'
            )
        ])
        fig_places.update_layout(
            title="Top 5 Places - Review Count",
            xaxis_title="Place",
            yaxis_title="Number of Reviews",
            height=400
        )
        st.plotly_chart(fig_places, use_container_width=True)
    
    with col2:
        sentiment_by_place = []
        for place in top_places.index:
            place_data = insight_df[insight_df['place'] == place]
            sentiments = place_data['predicted_sentiment'].value_counts()
            for sentiment, count in sentiments.items():
                sentiment_by_place.append({
                    'Place': place,
                    'Sentiment': sentiment,
                    'Count': count
                })
        
        sentiment_place_df = pd.DataFrame(sentiment_by_place)
        
        fig_place_sentiment = px.bar(
            sentiment_place_df,
            x='Place',
            y='Count',
            color='Sentiment',
            barmode='stack',
            title="Sentiment Breakdown by Place",
            height=400
        )
        st.plotly_chart(fig_place_sentiment, use_container_width=True)