import streamlit as st
import pandas as pd

def render_sidebar():
    """Render sidebar with file upload, model training, and filters"""
    
    # File Upload Section
    st.sidebar.markdown("### 📂 Upload Dataset")
    uploaded_file = st.sidebar.file_uploader(
        "Upload your CSV file",
        type=["csv"],
        help="Required columns: text, sentiment, place"
    )
    
    # Handle file upload
    if uploaded_file is not None:
        try:
            uploaded_df = pd.read_csv(uploaded_file)
            
            # Validate required columns
            required_cols = {'text', 'sentiment', 'place'}
            if not required_cols.issubset(set(uploaded_df.columns)):
                st.sidebar.error(f"❌ Missing columns: {required_cols - set(uploaded_df.columns)}")
                return None, None
            
            st.sidebar.success("✅ Dataset uploaded!")
            st.sidebar.write(f"Shape: {uploaded_df.shape}")
            
            # Store in session state
            st.session_state.uploaded_df = uploaded_df
            training_df = uploaded_df
            
        except Exception as e:
            st.sidebar.error(f"Error loading file: {e}")
            return None, None
    else:
        training_df = st.session_state.get('uploaded_df', None)
        if training_df is None:
            st.sidebar.info("👆 Please upload a CSV file to begin")
    
    st.sidebar.markdown("---")
    
    # Model Training Section
    st.sidebar.markdown("### 🤖 Train & Compare Models")
    
    if training_df is None:
        st.sidebar.warning("⚠️ Upload dataset first")
        return None, None
    
    train_multinomial = st.sidebar.checkbox("✓ Multinomial Naive Bayes", value=True)
    train_lstm = st.sidebar.checkbox("✓ LSTM", value=False)
    
    if train_multinomial or train_lstm:
        if st.sidebar.button("🚀 Train Models", use_container_width=True):
            # Import here to avoid circular imports
            from src.tabs.tab_model_training import train_models
            
            if 'text' in training_df.columns and 'sentiment' in training_df.columns:
                models_config = {
                    'train_multinomial': train_multinomial,
                    'train_lstm': train_lstm
                }
                st.session_state.model_results, st.session_state.models_trained, st.session_state.test_df = train_models(training_df, models_config)
                st.sidebar.success("✅ Models trained successfully!")
                st.sidebar.info(f"📊 Test data: {len(st.session_state.test_df)} rows (20% split)")
            else:
                st.sidebar.error("Dataset must contain 'text' and 'sentiment' columns")
    else:
        st.sidebar.warning("Select at least one model")
    
    st.sidebar.markdown("---")
    
    # Filters Section (only show if test data is available)
    test_df = st.session_state.get('test_df', None)
    
    if test_df is not None and not test_df.empty:
        # Convert date column to datetime if it exists
        if 'date' in test_df.columns:
            test_df['date'] = pd.to_datetime(test_df['date'])
        st.sidebar.markdown("### 🔧 Tourism Filters")
        
        # Place selector
        st.sidebar.markdown("**📍 Food Destination**")
        places = ["All Places"] + sorted(test_df["place"].unique().tolist())
        selected_place = st.sidebar.selectbox(
            "Select Destination",
            places,
            label_visibility="collapsed"
        )

        # Date range (if date column exists)
        date_range = None
        if 'date' in test_df.columns:
            st.sidebar.markdown("**📅 Date Range**")
            
            min_date = pd.to_datetime(test_df['date']).min()
            max_date = pd.to_datetime(test_df['date']).max()
            
            # Date filter type selector
            date_filter_type = st.sidebar.radio(
                "Filter by:",
                ["No filter", "Year", "Date range"],
                horizontal=True,
                label_visibility="collapsed"
            )
            
            if date_filter_type == "Date range":
                date_range = st.sidebar.date_input(
                    "Select date range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                    label_visibility="collapsed"
                )
            elif date_filter_type == "Year":
                min_year = min_date.year
                max_year = max_date.year
                selected_year = st.sidebar.slider(
                    "Select year",
                    min_value=min_year,
                    max_value=max_year,
                    value=max_year,
                    label_visibility="collapsed"
                )
                # Convert year selection to date range
                date_range = (pd.Timestamp(f'{selected_year}-01-01'), pd.Timestamp(f'{selected_year}-12-31'))
            else:
                date_range = None
        
        # Footer
        st.sidebar.markdown("---")
        st.sidebar.info("💡 Insights based on test data (20% split)")
    else:
        selected_place = None
        date_range = None

    return selected_place, date_range


def initialize_session_state():
    """Initialize all session state variables"""
    if "models_trained" not in st.session_state:
        st.session_state.models_trained = False
    if "model_results" not in st.session_state:
        st.session_state.model_results = {}
    if "test_df" not in st.session_state:
        st.session_state.test_df = None
    if "uploaded_df" not in st.session_state:
        st.session_state.uploaded_df = None