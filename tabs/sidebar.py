import streamlit as st
import pandas as pd
from tabs.model_training import train_models

def render_sidebar():
    """Render sidebar with upload, model training, and place filter"""
    
    with st.sidebar:
        st.markdown("### 📂 Upload Dataset")
        uploaded_file = st.file_uploader(
            "Upload CSV file",
            type=["csv"],
            help="Required columns: sentiment, place, text"
        )
        
        if uploaded_file is not None:
            try:
                st.session_state.df = pd.read_csv(uploaded_file)
                st.success("✅ Dataset uploaded successfully!")
                st.write(f"Shape: {st.session_state.df.shape}")
            except Exception as e:
                st.error(f"Error loading file: {e}")
        
        st.markdown("---")
        st.markdown("### 🤖 Train & Compare Models")
        
        train_multinomial = st.checkbox("✓ Multinomial Naive Bayes", value=True)
        train_lstm = st.checkbox("✓ LSTM", value=False)
        
        if train_multinomial or train_lstm:
            if st.button("🚀 Train Models", use_container_width=True):
                df = st.session_state.df
                if df is not None:
                    models_config = {
                        'train_multinomial': train_multinomial,
                        'train_lstm': train_lstm
                    }
                    st.session_state.model_results, st.session_state.models_trained = train_models(df, models_config)
                    st.success("✅ Models trained successfully!")
                else:
                    st.error("Please upload dataset first")
        else:
            st.warning("Select at least one model")
        
        st.markdown("---")
        st.markdown("### 📍 Filter by Place")
        
        df = st.session_state.df
        if df is not None and 'place' in df.columns:
            places = ["All Places"] + sorted(df['place'].unique().tolist())
            st.session_state.selected_place = st.selectbox(
                "Select a place",
                places,
                index=0 if st.session_state.selected_place == "All Places" else (places.index(st.session_state.selected_place) if st.session_state.selected_place in places else 0)
            )
        else:
            st.info("Upload dataset to filter by place")

def initialize_session_state():
    """Initialize all session state variables"""
    if "df" not in st.session_state:
        st.session_state.df = None
    if "models_trained" not in st.session_state:
        st.session_state.models_trained = False
    if "model_results" not in st.session_state:
        st.session_state.model_results = {}
    if "selected_place" not in st.session_state:
        st.session_state.selected_place = "All Places"