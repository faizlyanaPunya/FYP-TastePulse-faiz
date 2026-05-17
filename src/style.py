import streamlit as st

def apply_theme():
    st.markdown(
        """
        <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* ============================================
       DESIGN TOKENS — Student Dashboard BI Style
       Primary:    #1B3F5E  (dark navy-teal)
       Accent 1:   #00838F  (teal)
       Accent 2:   #C2185B  (pink/magenta)
       BG:         #E8F4F8  (powder blue)
       Card BG:    #FFFFFF
       Border:     #B2D8E8  (soft blue border)
       ============================================ */

    * {
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* ─── Global Background ─── */
    .stApp {
        background-color: #E8F4F8;
    }

    /* ─── Sidebar ─── */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #B2D8E8;
        box-shadow: 2px 0 12px rgba(0, 0, 0, 0.04);
    }

    /* ─── Page Header (h1 banner feel) ─── */
    h1 {
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 34px;
        background: linear-gradient(135deg, #1B3F5E 0%, #265E7E 100%);
        padding: 22px 32px;
        border-radius: 14px;
        margin-bottom: 1.2rem;
        letter-spacing: -0.5px;
    }

    h2 {
        color: #1B3F5E;
        font-weight: 700;
        font-size: 22px;
        margin-top: 1.5rem;
    }

    h3 {
        color: #265E7E;
        font-weight: 700;
        font-size: 18px;
        margin-top: 1rem;
    }

    h4 {
        color: #37718E;
        font-weight: 600;
        font-size: 15px;
    }

    /* ============================================
       TAB STYLING — BI Dashboard Style
       ============================================ */

    /* Hide default Streamlit tab underline & indicator */
    [data-baseweb="tab-highlight"],
    [data-testid="stTabIndicator"],
    div[data-testid="stTabs"] > div > div:nth-child(2) {
        display: none !important;
    }

    /* Tab list container */
    div[data-testid="stTabs"] > div {
        border-bottom: none !important;
        gap: 10px !important;
        margin-bottom: 20px !important;
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 8px 12px;
        border: 1px solid #B2D8E8;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    /* Individual tab — Inactive */
    button[data-testid="stTab"] {
        background-color: transparent !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        color: #37718E !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        margin-right: 4px !important;
        transition: all 0.2s ease !important;
    }

    button[data-testid="stTab"]:hover {
        background-color: #E8F4F8 !important;
        color: #1B3F5E !important;
    }

    /* Active Tab — Dark Navy with white text */
    button[data-testid="stTab"][aria-selected="true"] {
        background-color: #1B3F5E !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(27, 63, 94, 0.25) !important;
    }

    /* Force text colour to inherit */
    button[data-testid="stTab"] p {
        color: inherit !important;
    }

    /* ============================================
       METRIC CARDS
       ============================================ */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #B2D8E8;
        padding: 20px 24px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
        transition: all 0.2s ease;
    }

    div[data-testid="metric-container"]:hover {
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }

    div[data-testid="metric-container"] label {
        color: #37718E;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }

    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #1B3F5E;
        font-size: 30px;
        font-weight: 800;
    }

    /* ─── Highlighted metric (pink accent) — apply to first col metric ─── */
    div[data-testid="metric-container"]:nth-child(2) {
        border-top: 4px solid #C2185B;
    }
    div[data-testid="metric-container"]:nth-child(3) {
        border-top: 4px solid #C2185B;
    }

    /* ─── Streamlit native bordered containers ─── */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px !important;
        background-color: #FFFFFF !important;
        border: 1px solid #B2D8E8 !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04) !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
    }

    /* ============================================
       FORM ELEMENTS
       ============================================ */
    div[data-baseweb="select"] {
        border-radius: 10px;
        border: 1px solid #B2D8E8;
        background-color: #FFFFFF;
    }

    input, textarea {
        border-radius: 10px !important;
        border: 1px solid #B2D8E8 !important;
        background-color: #FFFFFF !important;
        color: #1B3F5E !important;
    }

    input:focus, textarea:focus {
        border-color: #00838F !important;
        box-shadow: 0 0 0 2px rgba(0, 131, 143, 0.2) !important;
    }

    /* ============================================
       ALERT BOXES
       ============================================ */
    .stAlert {
        border-radius: 10px;
        background-color: #FFFFFF;
        border: 1px solid #B2D8E8;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
    }

    div[data-baseweb="notification"][kind="success"] {
        border-left: 4px solid #00838F;
        background-color: #E0F7FA;
    }

    div[data-baseweb="notification"][kind="info"] {
        border-left: 4px solid #1B3F5E;
        background-color: #E8F4F8;
    }

    div[data-baseweb="notification"][kind="warning"] {
        border-left: 4px solid #F59E0B;
        background-color: #FFFBEB;
    }

    div[data-baseweb="notification"][kind="error"] {
        border-left: 4px solid #C2185B;
        background-color: #FCE4EC;
    }

    /* ============================================
       BUTTONS
       ============================================ */
    /* Primary Button — Teal (active/train) */
    button[data-testid="baseButton-primary"] {
        background-color: #00838F !important;
        color: #FFFFFF !important;
        border: 1px solid #00838F !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(0, 131, 143, 0.25) !important;
    }

    button[data-testid="baseButton-primary"]:hover {
        background-color: #00696F !important;
        box-shadow: 0 6px 18px rgba(0, 131, 143, 0.35) !important;
        transform: translateY(-1px) !important;
    }

    /* Secondary Button — White card */
    button[data-testid="baseButton-secondary"] {
        background-color: #FFFFFF !important;
        color: #1B3F5E !important;
        border: 1px solid #B2D8E8 !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }

    button[data-testid="baseButton-secondary"]:hover {
        background-color: #E8F4F8 !important;
        border-color: #37718E !important;
        transform: translateY(-1px) !important;
    }

    button[data-testid="baseButton-primary"] p,
    button[data-testid="baseButton-secondary"] p {
        color: inherit !important;
    }

    /* ============================================
       DATAFRAMES & CHARTS
       ============================================ */
    .stDataFrame {
        border-radius: 12px;
        border: 1px solid #B2D8E8;
        background-color: #FFFFFF;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
    }

    /* ============================================
       CUSTOM CARD CLASS
       ============================================ */
    .custom-card {
        background-color: #FFFFFF;
        padding: 20px 24px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
        border: 1px solid #B2D8E8;
        margin-bottom: 20px;
        transition: all 0.2s ease;
    }

    .custom-card:hover {
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }

    /* ============================================
       PROGRESS BARS
       ============================================ */
    .stProgress > div > div {
        background-color: #00838F;
        border-radius: 9999px;
        height: 8px;
    }

    /* ============================================
       EXPANDER
       ============================================ */
    .streamlit-expanderHeader {
        background-color: #FFFFFF !important;
        color: #1B3F5E !important;
        font-weight: 600 !important;
        border: 1px solid #B2D8E8 !important;
        border-radius: 10px !important;
    }

    .streamlit-expanderContent {
        border: 1px solid #B2D8E8 !important;
        border-top: none !important;
        border-bottom-left-radius: 10px !important;
        border-bottom-right-radius: 10px !important;
    }

    </style>
        """,
        unsafe_allow_html=True
    )
