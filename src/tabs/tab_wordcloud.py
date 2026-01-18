import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def render(filtered_df):
    st.markdown("## ☁️ Word Cloud Analysis")
    st.markdown("### Visualize Most Common Words by Sentiment")
    
    if filtered_df.empty:
        st.warning("⚠️ No data available for word cloud.")
        return
    
    # Sentiment filter
    sentiment_filter = st.selectbox(
        "Select Sentiment Type",
        ['All', 'Positive', 'Neutral', 'Negative']
    )
    
    # Filter data based on selection
    if sentiment_filter != 'All':
        text_data = filtered_df[filtered_df['sentiment'] == sentiment_filter.lower()]['bigrams'].dropna()
    else:
        text_data = filtered_df['bigrams'].dropna()
    
    if text_data.empty:
        st.warning(f"⚠️ No {sentiment_filter.lower()} reviews available.")
        return
    
    # Combine all text
    combined_text = ' '.join(text_data.astype(str))
    
    if not combined_text.strip():
        st.warning("⚠️ No text data to generate word cloud.")
        return
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Reviews", len(text_data))
    col2.metric("Total Words", len(combined_text.split()))
    col3.metric("Unique Words", len(set(combined_text.split())))
    
    st.markdown("---")
    
    # Generate word cloud
    try:
        # Color schemes for different sentiments
        color_schemes = {
            'All': 'viridis',
            'Positive': 'Greens',
            'Neutral': 'Blues',
            'Negative': 'Reds'
        }
        
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color='white',
            colormap=color_schemes.get(sentiment_filter, 'viridis'),
            max_words=100,
            relative_scaling=0.5,
            min_font_size=10
        ).generate(combined_text)
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(15, 8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title(f'{sentiment_filter} Sentiment - Word Cloud', 
                    fontsize=20, pad=20, fontweight='bold')
        
        st.pyplot(fig)
        
        # Show top keywords
        st.markdown("### 📊 Top 20 Keywords")
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
