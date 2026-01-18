import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def render(filtered_df):
    st.markdown("## 📱 Engagement Metrics Analysis")
    st.markdown("### Analyze Likes & Replies by Sentiment")
    
    if filtered_df.empty:
        st.warning("⚠️ No data available for engagement analysis.")
        return
    
    # Overall engagement metrics
    st.markdown("### 📊 Overall Engagement Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Avg Likes per Review", f"{filtered_df['diggCount'].mean():.1f}")
    col2.metric("Avg Replies per Review", f"{filtered_df['replyCommentTotal'].mean():.1f}")
    col3.metric("Total Likes", f"{filtered_df['diggCount'].sum():,}")
    col4.metric("Total Replies", f"{filtered_df['replyCommentTotal'].sum():,}")
    
    st.markdown("---")
    
    # Engagement by sentiment
    st.markdown("### 🎯 Engagement by Sentiment Type")
    
    engagement_by_sentiment = filtered_df.groupby('sentiment').agg({
        'diggCount': ['mean', 'sum', 'max'],
        'replyCommentTotal': ['mean', 'sum', 'max'],
        'text': 'count'
    }).round(2)
    
    # Flatten column names
    engagement_by_sentiment.columns = [
        'Avg Likes', 'Total Likes', 'Max Likes',
        'Avg Replies', 'Total Replies', 'Max Replies',
        'Review Count'
    ]
    
    # Display the table with styling
    st.dataframe(
        engagement_by_sentiment.style.background_gradient(cmap='YlGnBu', subset=['Avg Likes', 'Avg Replies'])
                               .format({
                                   'Avg Likes': '{:.2f}',
                                   'Avg Replies': '{:.2f}',
                                   'Total Likes': '{:,.0f}',
                                   'Total Replies': '{:,.0f}',
                                   'Max Likes': '{:,.0f}',
                                   'Max Replies': '{:,.0f}',
                                   'Review Count': '{:,.0f}'
                               }),
        use_container_width=True
    )
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👍 Average Likes by Sentiment")
        avg_likes = filtered_df.groupby('sentiment')['diggCount'].mean().reset_index()
        avg_likes.columns = ['Sentiment', 'Avg Likes']
        
        colors = {'positive': '#10b981', 'neutral': '#f59e0b', 'negative': '#ef4444'}
        avg_likes['color'] = avg_likes['Sentiment'].map(colors)
        
        fig_likes = px.bar(
            avg_likes, 
            x='Sentiment', 
            y='Avg Likes',
            color='Sentiment',
            color_discrete_map=colors,
            text='Avg Likes'
        )
        fig_likes.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig_likes.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_likes, use_container_width=True)
    
    with col2:
        st.markdown("#### 💬 Average Replies by Sentiment")
        avg_replies = filtered_df.groupby('sentiment')['replyCommentTotal'].mean().reset_index()
        avg_replies.columns = ['Sentiment', 'Avg Replies']
        avg_replies['color'] = avg_replies['Sentiment'].map(colors)
        
        fig_replies = px.bar(
            avg_replies,
            x='Sentiment',
            y='Avg Replies',
            color='Sentiment',
            color_discrete_map=colors,
            text='Avg Replies'
        )
        fig_replies.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig_replies.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_replies, use_container_width=True)
    
    st.markdown("---")
    
    # Engagement distribution
    st.markdown("### 📈 Engagement Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Likes Distribution")
        fig_likes_dist = px.box(
            filtered_df,
            x='sentiment',
            y='diggCount',
            color='sentiment',
            color_discrete_map=colors,
            labels={'sentiment': 'Sentiment', 'diggCount': 'Number of Likes'}
        )
        fig_likes_dist.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_likes_dist, use_container_width=True)
    
    with col2:
        st.markdown("#### Replies Distribution")
        fig_replies_dist = px.box(
            filtered_df,
            x='sentiment',
            y='replyCommentTotal',
            color='sentiment',
            color_discrete_map=colors,
            labels={'sentiment': 'Sentiment', 'replyCommentTotal': 'Number of Replies'}
        )
        fig_replies_dist.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_replies_dist, use_container_width=True)
    
    st.markdown("---")
    
    # Top engaged posts by sentiment
    st.markdown("### 🌟 Most Engaged Reviews")
    
    sentiment_filter = st.selectbox(
        "Filter by Sentiment",
        ['All', 'Positive', 'Neutral', 'Negative']
    )
    
    if sentiment_filter != 'All':
        display_df = filtered_df[filtered_df['sentiment'] == sentiment_filter.lower()]
    else:
        display_df = filtered_df
    
    # Calculate total engagement score
    display_df = display_df.copy()
    display_df['total_engagement'] = display_df['diggCount'] + display_df['replyCommentTotal']
    
    # Get top 10 most engaged
    top_engaged = display_df.nlargest(10, 'total_engagement')[
        ['text', 'sentiment', 'diggCount', 'replyCommentTotal', 'total_engagement', 'createTimeISO']
    ]
    
    # Display in a nice format
    for idx, row in top_engaged.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            sentiment_emoji = {'positive': '😊', 'neutral': '😐', 'negative': '😞'}
            
            with col1:
                st.write(f"{sentiment_emoji.get(row['sentiment'], '•')} **{row['text'][:150]}...**")
            with col2:
                st.metric("👍 Likes", int(row['diggCount']))
            with col3:
                st.metric("💬 Replies", int(row['replyCommentTotal']))
            
            st.caption(f"Posted: {row['createTimeISO'].strftime('%Y-%m-%d')}")
            st.markdown("---")
    
    # Engagement over time
    st.markdown("### 📅 Engagement Trends Over Time")
    
    # Group by date
    daily_engagement = filtered_df.groupby('date').agg({
        'diggCount': 'mean',
        'replyCommentTotal': 'mean'
    }).reset_index()
    
    fig_timeline = go.Figure()
    
    fig_timeline.add_trace(go.Scatter(
        x=daily_engagement['date'],
        y=daily_engagement['diggCount'],
        name='Avg Likes',
        line=dict(color='#10b981', width=2),
        mode='lines+markers'
    ))
    
    fig_timeline.add_trace(go.Scatter(
        x=daily_engagement['date'],
        y=daily_engagement['replyCommentTotal'],
        name='Avg Replies',
        line=dict(color='#3b82f6', width=2),
        mode='lines+markers'
    ))
    
    fig_timeline.update_layout(
        xaxis_title='Date',
        yaxis_title='Average Count',
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
    