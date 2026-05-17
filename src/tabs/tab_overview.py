import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from src.tabs.tab_initiatives import calculate_sentiment_health_score, get_top_keywords

def render(df, selected_place):
    st.markdown("## 📊 Executive Summary Hub")
    st.markdown("<p style='color: #37718E; font-size: 15px; margin-top: -10px; margin-bottom: 25px;'>A high-level overview of Northern Malaysia food tourism performance.</p>", unsafe_allow_html=True)
    
    if df.empty:
        st.warning("⚠️ No data available.")
        return
    
    # ── CALCULATIONS ─────────────────────────────────────────────────────────────
    total_posts = len(df)
    total_places = df['place'].nunique()
    
    # Calculate global health score
    global_health = calculate_sentiment_health_score(df)
    
    # Calculate best and worst places
    places = df['place'].unique()
    place_scores = []
    for p in places:
        p_df = df[df['place'] == p]
        score = calculate_sentiment_health_score(p_df)
        place_scores.append({'Place': p, 'Score': score})
    
    score_df = pd.DataFrame(place_scores).sort_values(by='Score', ascending=False)
    top_places = score_df.head(3)
    bottom_places = score_df.tail(3)
    
    # Get overall keywords
    top_pos_kws = get_top_keywords(df, 'positive')
    top_neg_kws = get_top_keywords(df, 'negative')

    sentiment_counts = df['sentiment'].value_counts()

    # ── LAYER 1: METRICS ────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style="background: #FFFFFF; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.04); border: 1px solid #B2D8E8; text-align: center;">
                <h4 style="color: #1B3F5E; margin: 0; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;">Total Reviews</h4>
                <p style="color: #00838F; font-size: 38px; font-weight: 800; margin: 5px 0 0 0;">{:,}</p>
            </div>
        """.format(total_posts), unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div style="background: #FFFFFF; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.04); border: 1px solid #B2D8E8; text-align: center;">
                <h4 style="color: #1B3F5E; margin: 0; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;">Food Destinations</h4>
                <p style="color: #00838F; font-size: 38px; font-weight: 800; margin: 5px 0 0 0;">{:,}</p>
            </div>
        """.format(total_places), unsafe_allow_html=True)
        
    with col3:
        # Color logic for health score
        health_color = "#00838F" if global_health >= 70 else "#F59E0B" if global_health >= 50 else "#C2185B"
        st.markdown("""
            <div style="background: #FFFFFF; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.04); border: 1px solid #B2D8E8; text-align: center; border-top: 4px solid {color};">
                <h4 style="color: #1B3F5E; margin: 0; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;">Global Health Score</h4>
                <p style="color: {color}; font-size: 38px; font-weight: 800; margin: 5px 0 0 0;">{score:.1f}%</p>
            </div>
        """.format(score=global_health, color=health_color), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── LAYER 2: LEADERBOARD ─────────────────────────────────────────────────────
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #1B3F5E; margin-top: 0; margin-bottom: 20px;'>🏆 Destination Leaderboard</h3>", unsafe_allow_html=True)
    
    # Generate HTML for Top Performers
    top_html = ""
    for i, row in top_places.iterrows():
        top_html += f"<div style='display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(0, 131, 143, 0.1);'><span style='font-weight: 600; color: #1B3F5E; font-size: 15px;'>{row['Place']}</span><span style='color: #00838F; font-weight: 700; background: rgba(0, 131, 143, 0.1); padding: 2px 10px; border-radius: 12px; font-size: 13px;'>{row['Score']:.1f}%</span></div>"
        
    # Generate HTML for Bottom Performers
    bottom_html = ""
    for i, row in bottom_places.iterrows():
        bottom_html += f"<div style='display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(194, 24, 91, 0.1);'><span style='font-weight: 600; color: #1B3F5E; font-size: 15px;'>{row['Place']}</span><span style='color: #C2185B; font-weight: 700; background: rgba(194, 24, 91, 0.1); padding: 2px 10px; border-radius: 12px; font-size: 13px;'>{row['Score']:.1f}%</span></div>"
        
    st.markdown(
        f"<div style='display: flex; justify-content: space-between; gap: 30px; flex-wrap: wrap;'>"
        f"<div style='flex: 1; min-width: 300px; padding: 20px; background: rgba(0, 131, 143, 0.03); border-top: 4px solid #00838F; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.02);'>"
        f"<h4 style='color: #00838F; margin-top: 0; font-size: 16px; margin-bottom: 15px;'>🟢 Top Performers</h4>"
        f"{top_html}</div>"
        f"<div style='flex: 1; min-width: 300px; padding: 20px; background: rgba(194, 24, 91, 0.03); border-top: 4px solid #C2185B; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.02);'>"
        f"<h4 style='color: #C2185B; margin-top: 0; font-size: 16px; margin-bottom: 15px;'>🔴 Needs Attention</h4>"
        f"{bottom_html}</div></div>", 
        unsafe_allow_html=True
    )
    
    st.markdown("</div>", unsafe_allow_html=True)

    # ── LAYER 3: CHARTS ──────────────────────────────────────────────────────────
    row3_col1, row3_col2 = st.columns(2)
    
    with row3_col1:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #1B3F5E; margin-top: 0;'>🥧 Overall Sentiment Breakdown</h3>", unsafe_allow_html=True) 
        
        fig_pie = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index.str.capitalize(),
            color=sentiment_counts.index,
            color_discrete_map={
                'positive': '#00838F', # Theme Teal
                'neutral': '#F59E0B',  # Theme Warning Orange
                'negative': '#C2185B'  # Theme Pink/Magenta
            },
            hole=0.3
        )
        
        fig_pie.update_traces(textposition='inside', textinfo='percent+label', textfont_size=12)
        fig_pie.update_layout(showlegend=True, height=280, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with row3_col2:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #1B3F5E; margin-top: 0;'>📈 Sentiment Trend Over Time</h3>", unsafe_allow_html=True)
        
        if 'date' in df.columns:
            daily_sentiment = df.groupby('date').agg({'sentiment_score': 'mean', 'text': 'count'}).reset_index()
            
            fig_time = go.Figure()
            fig_time.add_trace(go.Scatter(
                x=daily_sentiment['date'],
                y=daily_sentiment['sentiment_score'],
                mode='lines',
                name='Sentiment Score',
                line=dict(color='#00838F', width=3), # Theme Teal
                fill='tozeroy',
                fillcolor='rgba(0, 131, 143, 0.2)' # Teal with opacity
            ))
            
            fig_time.update_layout(
                showlegend=False,
                height=280,
                margin=dict(t=10, b=30, l=30, r=10),
                plot_bgcolor='rgba(255, 255, 255, 0)',
                paper_bgcolor='rgba(255, 255, 255, 0)'
            )
            st.plotly_chart(fig_time, use_container_width=True)
        else:
            st.info("📅 Date data is not available for trend analysis.")
        st.markdown("</div>", unsafe_allow_html=True)
