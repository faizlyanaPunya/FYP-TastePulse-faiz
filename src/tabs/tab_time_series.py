import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def render(filtered_df):
    st.markdown("## Sentiment Trends Over Time")

    if filtered_df.empty:
        st.warning("No data available for time series.")
        return

    # Create time series for each sentiment
    ts_data = []
    
    for sentiment in ['positive', 'neutral', 'negative']:
        sentiment_df = filtered_df[filtered_df['sentiment'] == sentiment]
        
        ts_sentiment = sentiment_df.groupby('date').agg({
            'sentiment_score': 'mean',
            'text': lambda x: '<br>'.join(['• ' + str(comment)[:80] + ('...' if len(str(comment)) > 80 else '') 
                                           for comment in x.dropna().head(5)]),
            'sentiment': 'count'
        }).reset_index()
        
        ts_sentiment.columns = ['date', 'avg_sentiment_score', 'top_comments', 'count']
        ts_sentiment['sentiment'] = sentiment
        ts_data.append(ts_sentiment)
    
    ts_overall = pd.concat(ts_data, ignore_index=True)
    
    # Create figure with custom hover data
    fig = go.Figure()
    
    # Define colors for each sentiment
    colors = {
        'positive': '#10b981',
        'neutral': '#f59e0b',
        'negative': '#ef4444'
    }
    
    # Add a line for each sentiment
    for sentiment in ['positive', 'neutral', 'negative']:
        sentiment_data = ts_overall[ts_overall['sentiment'] == sentiment]
        
        fig.add_trace(go.Scatter(
            x=sentiment_data['date'],
            y=sentiment_data['avg_sentiment_score'],
            mode='lines',
            name=sentiment.capitalize(),
            line=dict(color=colors[sentiment], width=3),
            hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br>' +
                          '<b>Sentiment:</b> ' + sentiment.capitalize() + '<br>' +
                          '<b>Avg Score:</b> %{y:.3f}<br>' +
                          '<b>Review Count:</b> %{customdata[0]}<br><br>' +
                          '<b>Sample Comments:</b><br>%{customdata[1]}<br>' +
                          '<extra></extra>',
            customdata=sentiment_data[['count', 'top_comments']].values
        ))
    
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Average Sentiment Score',
        hovermode='x unified',
        template='plotly_white',
        height=500,
        legend=dict(
            x=0.01,
            y=0.99,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='#e5e7eb',
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ----------------------------------------------------
    # NEW: AI GRAPH ANALYSIS ENGINE
    # ----------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Ask AI to Analyze this Trend")
    st.markdown("Generate an automated data-analyst explanation of the graph's visual movements.")
    
    if st.button("Generate Graph Analysis", type="primary"):
        from src.tabs.tab_ai_insights import _get_gemini_client, _call_gemini
        
        client, err = _get_gemini_client()
        if err:
            st.error(err)
        else:
            with st.spinner("Analyzing graph movements..."):
                dates_sorted = sorted(ts_overall['date'].unique())
                
                graph_data_str = "Chronological Time-Series Data:\n"
                for d in dates_sorted:
                    day_data = ts_overall[ts_overall['date'] == d]
                    graph_data_str += f"- Date: {d}\n"
                    for _, row in day_data.iterrows():
                        graph_data_str += f"  * {row['sentiment'].capitalize()} Line: Score={row['avg_sentiment_score']:.2f}, Volume={row['count']} reviews\n"
                        
                prompt = f"""You are a friendly food tourism advisor writing a simple report for local city council members and restaurant owners who are NOT technical or data experts.

Look at the time-series data below. It shows how people feel about food places over time — there are 3 lines on a graph: 
- The GREEN line = Happy/Positive reviews
- The YELLOW line = Neutral/Okay reviews  
- The RED line = Unhappy/Negative reviews

Your job is to describe what the graph looks like in very simple words, as if you are explaining it to someone who has never seen a graph before. Use everyday language like:
- "People were mostly happy during this period..."
- "There was a bad day on [date] where many complaints came in..."
- "Things got better towards the end of the week..."

Then give 1-2 simple suggestions on what the restaurant or city council should do next.

Keep it short (3-5 sentences), friendly, and easy to read. Avoid technical words like 'sentiment score', 'data points', 'anomaly', or 'trend analysis'. Write like you're talking to a friend.

DATA:
{graph_data_str}
"""
                try:
                    response_text = _call_gemini(client, prompt)
                    st.info(f"**AI Graph Analysis:**\n\n{response_text}")
                except Exception as e:
                    st.error(f"Error generating insights: {e}")
    
    # ----------------------------------------------------
    # NEW: ROOT CAUSE ANALYZER FOR MPKP INSIGHTS
    # ----------------------------------------------------
    st.markdown("---")
    st.markdown("## Deep-Dive: Root Cause Analysis")
    st.markdown("Tracing *why* sentiments drop. This section isolates the negative feedback in your selected timeframe to provide **actionable evidence for MPKP**.")
    
    # Isolate negative dataframe based on current filter
    negative_df = filtered_df[filtered_df['sentiment'] == 'negative']
    
    if negative_df.empty:
        st.success("Great news! There are no negative reviews in this selected timeframe and location.")
    else:
        st.error(f"Found **{len(negative_df)}** negative reviews. Analyzing the root causes...")
        
        col_ctx, col_evid = st.columns([1, 1.5])
        
        with col_ctx:
            st.markdown("#### Top Negative Indicators")
            st.caption("Frequently mentioned issues in this period:")
            
            with st.container():
                st.markdown('<div class="custom-card" style="padding: 15px;">', unsafe_allow_html=True)
                # Safely attempt to extract issues from the bigrams column
                if 'bigrams' in negative_df.columns:
                    try:
                        import ast
                        from collections import Counter
                        
                        all_bigrams = []
                        for b in negative_df['bigrams'].dropna():
                            if isinstance(b, str) and b.startswith('['):
                                all_bigrams.extend(ast.literal_eval(b))
                            elif isinstance(b, str):
                                # fallback if they are just comma separated
                                all_bigrams.extend([x.strip() for x in b.split(',') if x.strip()])
                                
                        if all_bigrams:
                            top_issues = Counter(all_bigrams).most_common(7)
                            for issue, count in top_issues:
                                # Highlight the issue name
                                st.markdown(f"**{issue}** — *(mentioned {count} times)*")
                        else:
                            st.write("Could not extract specific bigram topics. Check evidence panel.")
                    except Exception as e:
                        st.write("Error parsing context.")
                else:
                    st.write("Topic extraction requires a 'bigrams' column in your dataset.")
                st.markdown('</div>', unsafe_allow_html=True)
                
        with col_evid:
            st.markdown("#### Actionable Evidence (MPKP Reports)")
            st.caption("Latest verbatim feedback samples for context validation:")
            
            # Show the raw text as individual report cards
            # Check if 'date' column exists to sort
            if 'date' in negative_df.columns:
                sample_negatives = negative_df.sort_values(by='date', ascending=False)
            else:
                sample_negatives = negative_df
                
            sample_negatives = sample_negatives.head(5) # Take top 5 latest
            
            for _, row in sample_negatives.iterrows():
                place_name = row.get('place', 'Unknown Location')
                date_val = row.get('date', 'Unknown Date')
                
                with st.expander(f"Problem at {place_name} ({date_val})", expanded=True):
                    st.write(f"*{row.get('text', 'No text available')}*")