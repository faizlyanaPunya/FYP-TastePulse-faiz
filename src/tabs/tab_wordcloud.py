import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import ast

def render(filtered_df):
    st.markdown("## Word Cloud Analysis")
    st.markdown("### Visualize Most Common Words by Sentiment")
    
    if filtered_df.empty:
        st.warning("No data available for word cloud.")
        return
    
    # Sentiment filter
    sentiment_filter = st.selectbox(
        "Select Sentiment Type",
        ['All', 'Positive', 'Neutral', 'Negative']
    )
    
    # Filter data based on selection
    if sentiment_filter != 'All':
        text_data = filtered_df[filtered_df['sentiment'] == sentiment_filter.lower()]['text_tokens'].dropna()
    else:
        text_data = filtered_df['text_tokens'].dropna()
    
    if text_data.empty:
        st.warning(f"No {sentiment_filter.lower()} reviews available.")
        return
    
    # Convert tuples to space-separated strings
    def convert_bigrams(bigram_str):
        try:
            # Parse string representation of tuple
            bigram_tuple = ast.literal_eval(bigram_str)
            # Convert tuple to space-separated string
            return ' '.join(bigram_tuple)
        except:
            # If it's already a string, return as is
            return str(bigram_str)
    
    text_data = text_data.apply(convert_bigrams)
    
    # Combine all text
    combined_text = ' '.join(text_data.astype(str))
    
    # Clean trailing apostrophes from words
    combined_text = re.sub(r"\b(\w+)'\b", r"\1", combined_text)
    
    if not combined_text.strip():
        st.warning("No text data to generate word cloud.")
        return
    
    st.markdown("---")
    
    # Generate word cloud FIRST
    try:
        # Color schemes for different sentiments
        color_schemes = {
            'All': 'viridis',
            'Positive': 'Greens',
            'Neutral': 'Blues',
            'Negative': 'Reds'
        }
        
        # Reduced width/height for a smaller image
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap=color_schemes.get(sentiment_filter, 'viridis'),
            max_words=100,
            relative_scaling=0.5,
            min_font_size=10
        ).generate(combined_text)
        
        # Create matplotlib figure with smaller figsize
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title(f'{sentiment_filter} Sentiment - Word Cloud', 
                    fontsize=16, pad=15, fontweight='bold')
        
        # Layout: Image on left, metric cards stacked on right
        col_img, col_metrics = st.columns([2.5, 1])
        
        with col_img:
            st.pyplot(fig)
            
        with col_metrics:
            st.markdown(f'''
            <div style="background-color: #fcfcfc; padding: 15px; border-radius: 12px; border-left: 6px solid #4CAF50; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;">
                <h4 style="margin: 0; color: #333; font-size: 15px; text-transform: uppercase;">Total Reviews</h4>
                <hr style="margin: 8px 0; border: none; border-top: 1px solid #eee;">
                <p style="font-size: 32px; font-weight: 800; color: #4CAF50; margin: 0;">{len(text_data):,}</p>
            </div>
            
            <div style="background-color: #fcfcfc; padding: 15px; border-radius: 12px; border-left: 6px solid #2196F3; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;">
                <h4 style="margin: 0; color: #333; font-size: 15px; text-transform: uppercase;">Total Words</h4>
                <hr style="margin: 8px 0; border: none; border-top: 1px solid #eee;">
                <p style="font-size: 32px; font-weight: 800; color: #2196F3; margin: 0;">{len(combined_text.split()):,}</p>
            </div>
            
            <div style="background-color: #fcfcfc; padding: 15px; border-radius: 12px; border-left: 6px solid #9c27b0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;">
                <h4 style="margin: 0; color: #333; font-size: 15px; text-transform: uppercase;">Unique Words</h4>
                <hr style="margin: 8px 0; border: none; border-top: 1px solid #eee;">
                <p style="font-size: 32px; font-weight: 800; color: #9c27b0; margin: 0;">{len(set(combined_text.split())):,}</p>
            </div>
            ''', unsafe_allow_html=True)
            
        st.markdown("---")
        
        # Show top keywords
        st.markdown("### Top 20 Keywords")
        word_freq = wordcloud.words_
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        
        # Display in a nice format
        cols = st.columns(2)
        mid_point = len(top_words) // 2
        
        with cols[0]:
            for i, (word, freq) in enumerate(top_words[:mid_point], 1):
                st.write(f"{i}. **{word}** - {freq:.4f}")
        
        with cols[1]:
            for i, (word, freq) in enumerate(top_words[mid_point:], mid_point + 1):
                st.write(f"{i}. **{word}** - {freq:.4f}")
                
    except Exception as e:
        st.error(f"Error generating word cloud: {str(e)}")
        st.info("Try selecting a different sentiment type or ensure there is enough text data.")