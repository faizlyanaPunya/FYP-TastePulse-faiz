import streamlit as st

def apply_theme():
    st.markdown(
        """
        <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');
    
    /* ============================================
       GLOBAL STYLES & RESET
       ============================================ */
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Main app background - Soft cream */
    .stApp {
        background: linear-gradient(135deg, #faf8f5 0%, #f5f2ed 50%, #ede8e0 100%);
        background-attachment: fixed;
    }
    
    /* Subtle overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.02);
        pointer-events: none;
        z-index: 0;
    }

    /* ============================================
       SIDEBAR STYLING
       ============================================ */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(250, 248, 245, 0.98) 0%, rgba(255, 255, 255, 0.95) 100%);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(123, 164, 145, 0.15);
        box-shadow: 4px 0 20px rgba(123, 164, 145, 0.08);
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }

    /* ============================================
       TAB STYLING - Soft sage green
       ============================================ */
    button[data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        margin-right: 12px;
        padding: 14px 28px;
        color: #5a6c5d;
        border: 2px solid rgba(123, 164, 145, 0.2);
        font-weight: 600;
        font-size: 15px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }

    button[data-baseweb="tab"]:hover {
        background: rgba(123, 164, 145, 0.12);
        border-color: rgba(123, 164, 145, 0.35);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(123, 164, 145, 0.15);
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #7ba491 0%, #84a98c 100%);
        color: white;
        font-weight: 700;
        border-color: transparent;
        box-shadow: 0 8px 24px rgba(123, 164, 145, 0.3);
        transform: translateY(-2px) scale(1.02);
    }

    /* ============================================
       METRIC CARDS - Soft earthy style
       ============================================ */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(123, 164, 145, 0.15);
        padding: 28px;
        border-radius: 20px;
        box-shadow: 
            0 8px 32px rgba(123, 164, 145, 0.1),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.9);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    /* Subtle gradient border effect */
    div[data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #7ba491, #c9ae86, #c97c5d, #7ba491);
        background-size: 400% 400%;
        border-radius: 20px;
        z-index: -1;
        opacity: 0;
        transition: opacity 0.4s;
        animation: gradientShift 4s ease infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    div[data-testid="metric-container"]:hover::before {
        opacity: 0.2;
    }
    
    div[data-testid="metric-container"]:hover {
        box-shadow: 
            0 20px 60px rgba(123, 164, 145, 0.2),
            inset 0 1px 0 0 rgba(255, 255, 255, 1);
        transform: translateY(-4px) scale(1.02);
        background: rgba(255, 255, 255, 0.98);
    }

    div[data-testid="metric-container"] label {
        color: #6b7c6e;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        background: linear-gradient(135deg, #7ba491 0%, #84a98c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 42px;
        font-weight: 800;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* ============================================
       TYPOGRAPHY
       ============================================ */
    h1 {
        background: linear-gradient(135deg, #7ba491 0%, #84a98c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 48px;
        margin-bottom: 0.5rem;
        font-family: 'Space Grotesk', sans-serif;
        text-shadow: 0 4px 12px rgba(123, 164, 145, 0.15);
    }
    
    h2 {
        color: #3d4f42;
        font-weight: 700;
        font-size: 32px;
        margin-top: 1.5rem;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    h3 {
        color: #4a5d4e;
        font-weight: 600;
        font-size: 24px;
        margin-top: 1rem;
    }

    /* ============================================
       FORM ELEMENTS
       ============================================ */
    div[data-baseweb="select"] {
        border-radius: 16px;
        border: 2px solid rgba(123, 164, 145, 0.2);
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    div[data-baseweb="select"]:hover {
        border-color: rgba(123, 164, 145, 0.4);
        box-shadow: 0 4px 12px rgba(123, 164, 145, 0.12);
    }
    
    /* Input fields */
    input, textarea {
        border-radius: 12px;
        border: 2px solid rgba(123, 164, 145, 0.2) !important;
        background: rgba(255, 255, 255, 0.95) !important;
        transition: all 0.3s ease;
    }
    
    input:focus, textarea:focus {
        border-color: rgba(123, 164, 145, 0.5) !important;
        box-shadow: 0 0 0 3px rgba(123, 164, 145, 0.08) !important;
    }

    /* ============================================
       ALERT BOXES
       ============================================ */
    .stAlert {
        border-radius: 16px;
        border: none;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(123, 164, 145, 0.1);
        padding: 1.25rem;
    }
    
    /* Success alert */
    div[data-baseweb="notification"][kind="success"] {
        border-left: 4px solid #84a98c;
    }
    
    /* Info alert */
    div[data-baseweb="notification"][kind="info"] {
        border-left: 4px solid #7ba491;
    }
    
    /* Warning alert */
    div[data-baseweb="notification"][kind="warning"] {
        border-left: 4px solid #c9ae86;
    }
    
    /* Error alert */
    div[data-baseweb="notification"][kind="error"] {
        border-left: 4px solid #c97c5d;
    }

    /* ============================================
       BUTTONS
       ============================================ */
    .stButton > button {
        background: linear-gradient(135deg, #7ba491 0%, #84a98c 100%);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 12px 32px;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 16px rgba(123, 164, 145, 0.25);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(123, 164, 145, 0.35);
        background: linear-gradient(135deg, #84a98c 0%, #7ba491 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }

    /* ============================================
       DATAFRAMES & TABLES
       ============================================ */
    .stDataFrame {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(123, 164, 145, 0.08);
    }
    
    /* ============================================
       CHARTS & VISUALIZATIONS
       ============================================ */
    .js-plotly-plot {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(123, 164, 145, 0.08);
    }

    /* ============================================
       CUSTOM CONTAINERS
       ============================================ */
    .custom-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        padding: 28px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(123, 164, 145, 0.12);
        border: 1px solid rgba(123, 164, 145, 0.15);
        margin-bottom: 24px;
        transition: all 0.4s ease;
    }
    
    .custom-card:hover {
        box-shadow: 0 16px 48px rgba(123, 164, 145, 0.2);
        transform: translateY(-4px);
    }

    /* ============================================
       PROGRESS BARS
       ============================================ */
    .stProgress > div > div {
        background: linear-gradient(90deg, #7ba491 0%, #84a98c 100%);
        border-radius: 10px;
        height: 12px;
    }

    /* ============================================
       SCROLLBAR - Soft sage
       ============================================ */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(250, 248, 245, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #7ba491 0%, #84a98c 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #84a98c 0%, #7ba491 100%);
    }

    /* ============================================
       ANIMATIONS
       ============================================ */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .element-container {
        animation: fadeInUp 0.6s ease-out;
    }

    /* ============================================
       MARKDOWN & TEXT
       ============================================ */
    .stMarkdown {
        color: #3d4f42;
    }
    
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(123, 164, 145, 0.25) 50%, 
            transparent 100%);
        margin: 2rem 0;
    }
    
    /* ============================================
       SIDEBAR IMPROVEMENTS
       ============================================ */
    section[data-testid="stSidebar"] h2 {
        color: #7ba491;
        font-weight: 700;
        font-size: 24px;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    section[data-testid="stSidebar"] h3 {
        color: #4a5d4e;
        font-weight: 600;
        font-size: 18px;
    }
    
    section[data-testid="stSidebar"] label {
        color: #5a6c5d;
        font-weight: 600;
        font-size: 14px;
    }

    </style>
        """,
        unsafe_allow_html=True
    )


