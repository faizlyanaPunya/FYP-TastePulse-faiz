import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def render(df, selected_place):
    st.markdown("## 📊 Food Tourism Overview")
    
    if df.empty:
        st.warning("⚠️ No data available.")
        return
    
    # Calculate metrics
    total_posts = len(df)
    total_places = df['place'].nunique()
    sentiment_counts = df['sentiment'].value_counts()
    
    # First Row: 2 Cards with containers
    row1_col1, row1_col2 = st.columns(2)
    
    # Card 1: Total Posts
    with row1_col1:
        with st.container():
            st.markdown("""
                <div style="
                    background: rgba(255, 255, 255, 0.95);
                    padding: 1rem;
                    border-radius: 20px;
                    box-shadow: 0 8px 32px rgba(123, 164, 145, 0.15);
                    border: 1px solid rgba(123, 164, 145, 0.2);
                    text-align: center;
                ">
                    <h3 style="color: #7ba491; margin: 0 0 0 0; font-size: 25px;">📝 Total Posts</h3>
                    <p style="font-size: 50px; font-weight: 800; margin: 0; color: #7ba491;">{:,}</p>
                    <p style="color: #6b7c6e; font-size: 14px; margin: 0.5rem 0 0 0;">Food Reviews</p>
                </div>
            """.format(total_posts), unsafe_allow_html=True)
    
    # Card 2: Total Restaurants
    with row1_col2:
        with st.container():
            st.markdown("""
                <div style="
                    background: rgba(255, 255, 255, 0.95);
                    padding: 1rem;
                    border-radius: 20px;
                    box-shadow: 0 8px 32px rgba(123, 164, 145, 0.15);
                    border: 1px solid rgba(123, 164, 145, 0.2);
                    text-align: center;
                ">
                    <h3 style="color: #7ba491; margin: 0 0 0 0; font-size: 25px;">🏪 Places</h3>
                    <p style="font-size: 50px; font-weight: 800; margin: 0; color: #7ba491;">{}</p>
                    <p style="color: #6b7c6e; font-size: 14px; margin: 0.5rem 0 0 0;">Food Places</p>
                </div>
            """.format(total_places), unsafe_allow_html=True)
    
    # Add spacing between rows
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Second Row: 2 Cards
    row2_col1, row2_col2 = st.columns(2)
    
    # Card 3: Overall Sentiment Pie Chart
    with row2_col1:
        with st.container():
            st.markdown("<h3 style='font-size: 25px;'>🥧 Overall Sentiment</h3>", unsafe_allow_html=True) 
        
        fig_pie = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index.str.capitalize(),
            color=sentiment_counts.index,
            color_discrete_map={
                'positive': '#7ba491',
                'neutral': '#c9ae86',
                'negative': '#c97c5d'
            },
            hole=0.3
        )
        
        fig_pie.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=12
        )
        
        fig_pie.update_layout(
            showlegend=True,
            height=300,
            margin=dict(t=20, b=20, l=20, r=20)
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Card 4: Time Series
    with row2_col2:
        with st.container():
            st.markdown("<h3 style='font-size: 25px;'>📈 Sentiment Trends</h3>", unsafe_allow_html=True)
        
        # Group by date
        daily_sentiment = df.groupby('date').agg({
            'sentiment_score': 'mean',
            'text': 'count'
        }).reset_index()
        
        fig_time = go.Figure()
        
        # Sentiment line
        fig_time.add_trace(go.Scatter(
            x=daily_sentiment['date'],
            y=daily_sentiment['sentiment_score'],
            mode='lines',
            name='Sentiment Score',
            line=dict(color='#7ba491', width=3),
            fill='tozeroy',
            fillcolor='rgba(123, 164, 145, 0.2)'
        ))
        
        fig_time.update_layout(
            showlegend=False,
            height=300,
            margin=dict(t=20, b=40, l=40, r=20),
            xaxis_title='Date',
            yaxis_title='Score',
            plot_bgcolor='rgba(255, 255, 255, 0.9)',
            paper_bgcolor='rgba(255, 255, 255, 0)'
        )
        
        st.plotly_chart(fig_time, use_container_width=True)
