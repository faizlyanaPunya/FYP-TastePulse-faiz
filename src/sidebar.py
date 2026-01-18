import streamlit as st

def render_sidebar(df):

    
    # Filters Section
    st.sidebar.markdown("### 🔧 Tourism Filters")
    
    # Place selector
    st.sidebar.markdown("**📍 Food Destination**")
    selected_place = st.sidebar.selectbox(
        "Select Destination",
        sorted(df["place"].unique()),
        label_visibility="collapsed"
    )

    # Date range
    st.sidebar.markdown("**📅 Date Range**")
    
    min_date = df['date'].min()
    max_date = df['date'].max()
    
    date_range = st.sidebar.date_input(
        "Select date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info("💡 Explore food tourism sentiment across Northern Malaysia")

    return selected_place, date_range



