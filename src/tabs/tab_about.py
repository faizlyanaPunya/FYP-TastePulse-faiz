import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

def render(model_results):
    """Render About page with project flow and Model Evaluation performance metrics"""
    
    st.markdown("### About TastePulse")
    st.info("**TastePulse** is an interactive Sentiment Analysis dashboard designed to uncover insights driving Northern Malaysia's food tourism. By analyzing public opinion, it helps identify dining trends, assess customer satisfaction, and recommend strategic initiatives.")
    
    # Project Team Details
    st.markdown("### Project Team")
    import os
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Supervisee")
        if os.path.exists("faiz.jpeg"):
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.image("faiz.jpeg", width=160)
        else:
            st.write("*(Pic)*")
        st.info("**Name:** Nur Faizlyana Binti Mohd Kamarul Ariffin\n\n**Matric No:** 300442 \n\n**Program:** Bachelor of Computer Science with hons.")

    with col2:
        st.markdown("#### Supervisor")
        if os.path.exists("juhaida.jpeg"):
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.image("juhaida.jpeg", width=170)
        else:
            st.write("*(Pic)*")
        st.success("**Name:** Assoc. Prof. Ts. Dr. Juhaida Binti Abu Bakar\n\n**Institution:** Universiti Utara Malaysia (UUM)")

    st.markdown("---")
    st.markdown("#### Peer Dashboards")
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("##### TastePulse Dashboard")
        if os.path.exists("najaa.jpg"):
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.image("najaa.jpg", width=185)
        else:
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.write("*(Pic)*")
        st.warning(
            "**Name:** Nur Najaa Aini Binti Mohd Puzi\n\n"
            "**Project:** TastePulse Dashboard\n\n"
            "**Sentiment Analysis of Food Tourism in Northern Community**."
        )

    with col4:
        st.markdown("##### ThemePulse Dashboard")
        if os.path.exists("mak.jpeg"):
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.image("mak.jpeg", width=160)
        else:
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.write("*(Pic)*")
        st.info(
            "**Name:** Mak Shei Wen\n\n"
            "**Project:** ThemePulse Dashboard\n\n"
            "**Topic Modeling of Food Tourism in Northern Community**"
        )
        
    st.markdown("---")
    
    st.markdown("### What is Sentiment Analysis?")
    st.info("""
    Sentiment analysis is a machine learning technique used to determine whether text data is **positive, negative, or neutral**. 
    In the context of our work, we are actively analyzing what locals and tourists say about food destinations across **Northern Malaysia** in **Kubang Pasu** district to be specific. 
    Instead of manually reading thousands of reviews, we automate this process to identify trends, pinpointing exactly *what* went wrong and *when*.
    """)
    
    st.markdown("### Detailed Project Flow — KDD Methodology")

    # ── Top overview: 5-Step Animated Workflow Ribbon ──────────────────────────────
    st.markdown("""
    <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; background: #ffffff; padding: 28px 36px; border-radius: 18px; border: 1px solid #B2D8E8; box-shadow: 0 10px 30px rgba(27, 63, 94, 0.08); margin: 16px 0 32px 0;">
        <div style="text-align: center; flex: 1; min-width: 120px; padding: 10px;">
            <div style="width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, #1B3F5E, #00838F); color: white; font-size: 20px; font-weight: 800; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px auto; box-shadow: 0 4px 12px rgba(0, 131, 143, 0.3);">01</div>
            <div style="font-weight: 800; font-size: 16px; color: #1B3F5E;">Selection</div>
            <div style="font-size: 13px; color: #00838F; font-weight: 600; margin-top: 4px;">Target Data</div>
        </div>
        <div style="color: #00838F; font-size: 24px; font-weight: 900; opacity: 0.4;">➔</div>
        <div style="text-align: center; flex: 1; min-width: 120px; padding: 10px;">
            <div style="width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, #1B3F5E, #00838F); color: white; font-size: 20px; font-weight: 800; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px auto; box-shadow: 0 4px 12px rgba(0, 131, 143, 0.3);">02</div>
            <div style="font-weight: 800; font-size: 16px; color: #1B3F5E;">Preprocessing</div>
            <div style="font-size: 13px; color: #00838F; font-weight: 600; margin-top: 4px;">Data Cleaning</div>
        </div>
        <div style="color: #00838F; font-size: 24px; font-weight: 900; opacity: 0.4;">➔</div>
        <div style="text-align: center; flex: 1; min-width: 120px; padding: 10px;">
            <div style="width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, #1B3F5E, #00838F); color: white; font-size: 20px; font-weight: 800; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px auto; box-shadow: 0 4px 12px rgba(0, 131, 143, 0.3);">03</div>
            <div style="font-weight: 800; font-size: 16px; color: #1B3F5E;">Transformation</div>
            <div style="font-size: 13px; color: #00838F; font-weight: 600; margin-top: 4px;">Feature Eng.</div>
        </div>
        <div style="color: #00838F; font-size: 24px; font-weight: 900; opacity: 0.4;">➔</div>
        <div style="text-align: center; flex: 1; min-width: 120px; padding: 10px;">
            <div style="width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, #1B3F5E, #00838F); color: white; font-size: 20px; font-weight: 800; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px auto; box-shadow: 0 4px 12px rgba(0, 131, 143, 0.3);">04</div>
            <div style="font-weight: 800; font-size: 16px; color: #1B3F5E;">Data Mining</div>
            <div style="font-size: 13px; color: #00838F; font-weight: 600; margin-top: 4px;">Model Training</div>
        </div>
        <div style="color: #00838F; font-size: 24px; font-weight: 900; opacity: 0.4;">➔</div>
        <div style="text-align: center; flex: 1; min-width: 120px; padding: 10px;">
            <div style="width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, #1B3F5E, #C2185B); color: white; font-size: 20px; font-weight: 800; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px auto; box-shadow: 0 4px 12px rgba(194, 24, 91, 0.4);">05</div>
            <div style="font-weight: 800; font-size: 16px; color: #1B3F5E;">Interpretation</div>
            <div style="font-size: 13px; color: #C2185B; font-weight: 600; margin-top: 4px;">Evaluation & Action</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### The KDD Story — Phase by Phase")

    # ── KDD Process Diagram ───────────────────────────────────────────────────
    if os.path.exists("kdd_process.png"):
        img_l, img_c, img_r = st.columns([1, 8, 1])
        with img_c:
            st.image("kdd_process.png", caption="Figure: KDD (Knowledge Discovery in Databases) Process Flow", use_container_width=True)
    st.markdown("")

    # ── 5 methodology tabs (one per KDD phase) ────────────────────────────────
    tab_m1, tab_m2, tab_m3, tab_m4, tab_m5 = st.tabs([
        "1. Selection",
        "2. Preprocessing",
        "3. Transformation",
        "4. Data Mining",
        "5. Interpretation & Evaluation",
    ])

    # ── Phase 1: Selection ────────────────────────────────────────────────────
    with tab_m1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1B3F5E 0%, #265E7E 100%); color: white; padding: 32px 40px; border-radius: 16px; box-shadow: 0 12px 32px rgba(27, 63, 94, 0.2); margin-bottom: 28px; display: flex; align-items: center; gap: 32px; border: 1px solid #00838F;">
            <div style="background: rgba(232, 244, 248, 0.15); backdrop-filter: blur(10px); border: 2px solid #B2D8E8; border-radius: 20px; min-width: 88px; height: 88px; display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 900; box-shadow: 0 8px 24px rgba(0,0,0,0.15); color: #FFFFFF;">
                01
            </div>
            <div>
                <div style="font-size: 14px; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; color: #B2D8E8; margin-bottom: 6px;">Phase 1 • KDD Methodology</div>
                <h2 style="color: white; margin: 0 0 10px 0; font-size: 28px; font-weight: 800; border: none; padding: 0;">Selection & Data Harvesting</h2>
                <p style="margin: 0; font-size: 16px; opacity: 0.95; line-height: 1.6; color: #E8F4F8;">
                    The foundation of KDD is identifying target data. We harvested thousands of community reviews and public comments from TikTok food pages across the <b>Kubang Pasu district</b> using specialized scraping tools, capturing authentic feedback in Malay, English, and northern mixed dialects.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            <div class="custom-card" style="border-left: 5px solid #00838F; height: 100%;">
                <div style="font-weight: 800; font-size: 18px; color: #1B3F5E; margin-bottom: 12px; display: flex; align-items: center; gap: 10px;">
                    <span style="width: 12px; height: 12px; border-radius: 50%; background: #00838F; display: inline-block;"></span> Target Domain
                </div>
                <div style="color: #374151; font-size: 15px; line-height: 1.8;">
                    • <b>Location:</b> Kubang Pasu district food outlets<br>
                    • <b>Source:</b> Public TikTok posts & review comments<br>
                    • <b>Focus:</b> Northern Malaysia food tourism sentiment
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown("""
            <div class="custom-card" style="border-left: 5px solid #C2185B; height: 100%;">
                <div style="font-weight: 800; font-size: 18px; color: #1B3F5E; margin-bottom: 12px; display: flex; align-items: center; gap: 10px;">
                    <span style="width: 12px; height: 12px; border-radius: 50%; background: #C2185B; display: inline-block;"></span> Tools & Scope
                </div>
                <div style="color: #374151; font-size: 15px; line-height: 1.8;">
                    • <b>Harvesting Tool:</b> Apify Comment Scraper API<br>
                    • <b>Platform:</b> TikTok video verbatim interactions<br>
                    • <b>Linguistic Scope:</b> Malay, English & local Kedah slang
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Phase 2: Preprocessing ────────────────────────────────────────────────
    with tab_m2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1B3F5E 0%, #265E7E 100%); color: white; padding: 32px 40px; border-radius: 16px; box-shadow: 0 12px 32px rgba(27, 63, 94, 0.2); margin-bottom: 28px; display: flex; align-items: center; gap: 32px; border: 1px solid #00838F;">
            <div style="background: rgba(232, 244, 248, 0.15); backdrop-filter: blur(10px); border: 2px solid #B2D8E8; border-radius: 20px; min-width: 88px; height: 88px; display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 900; box-shadow: 0 8px 24px rgba(0,0,0,0.15); color: #FFFFFF;">
                02
            </div>
            <div>
                <div style="font-size: 14px; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; color: #B2D8E8; margin-bottom: 6px;">Phase 2 • KDD Methodology</div>
                <h2 style="color: white; margin: 0 0 10px 0; font-size: 28px; font-weight: 800; border: none; padding: 0;">Text Preprocessing & Data Cleaning</h2>
                <p style="margin: 0; font-size: 16px; opacity: 0.95; line-height: 1.6; color: #E8F4F8;">
                    Raw social media verbatim is extremely noisy. We cleaned the corpus by removing duplicates, stripping URLs, HTML tags, and special characters. Using the <b>Malaya NLP library</b>, we normalized Malaysian shorthand (e.g., <i>x</i> → tidak, <i>nk</i> → nak) and handled mixed-language slang seamlessly.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            <div class="custom-card" style="border-left: 5px solid #00838F; height: 100%;">
                <div style="font-weight: 800; font-size: 18px; color: #1B3F5E; margin-bottom: 12px; display: flex; align-items: center; gap: 10px;">
                    <span style="width: 12px; height: 12px; border-radius: 50%; background: #00838F; display: inline-block;"></span> Noise Reduction
                </div>
                <div style="color: #374151; font-size: 15px; line-height: 1.8;">
                    • <b>Deduplication:</b> Removed duplicate entries & null rows<br>
                    • <b>Sanitization:</b> Stripped URLs, HTML codes & symbols<br>
                    • <b>Filtering:</b> Discarded non-informative emoji-only posts
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown("""
            <div class="custom-card" style="border-left: 5px solid #1B3F5E; height: 100%;">
                <div style="font-weight: 800; font-size: 18px; color: #1B3F5E; margin-bottom: 12px; display: flex; align-items: center; gap: 10px;">
                    <span style="width: 12px; height: 12px; border-radius: 50%; background: #1B3F5E; display: inline-block;"></span> Text Normalization
                </div>
                <div style="color: #374151; font-size: 15px; line-height: 1.8;">
                    • <b>Engine:</b> Malaya NLP library normalizer<br>
                    • <b>Shorthand:</b> Standardized Malaysian chat abbreviations<br>
                    • <b>Syntax:</b> Resolved mixed Malay-English vocabulary
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Phase 3: Transformation ───────────────────────────────────────────────
    with tab_m3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1B3F5E 0%, #265E7E 100%); color: white; padding: 32px 40px; border-radius: 16px; box-shadow: 0 12px 32px rgba(27, 63, 94, 0.2); margin-bottom: 28px; display: flex; align-items: center; gap: 32px; border: 1px solid #00838F;">
            <div style="background: rgba(232, 244, 248, 0.15); backdrop-filter: blur(10px); border: 2px solid #B2D8E8; border-radius: 20px; min-width: 88px; height: 88px; display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 900; box-shadow: 0 8px 24px rgba(0,0,0,0.15); color: #FFFFFF;">
                03
            </div>
            <div>
                <div style="font-size: 14px; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; color: #B2D8E8; margin-bottom: 6px;">Phase 3 • KDD Methodology</div>
                <h2 style="color: white; margin: 0 0 10px 0; font-size: 28px; font-weight: 800; border: none; padding: 0;">Feature Transformation & Bigrams</h2>
                <p style="margin: 0; font-size: 16px; opacity: 0.95; line-height: 1.6; color: #E8F4F8;">
                    Cleaned text must be converted into numerical features. We performed tokenization, stop-word filtering, and Bigram extraction (two-word phrases like <i>makanan sedap</i> or <i>layanan teruk</i>) to preserve critical contextual syntax. For Naive Bayes, we built TF-IDF matrices; for LSTM, padded word embedding sequences.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("""
            <div class="custom-card" style="border-left: 5px solid #00838F; height: 100%;">
                <div style="font-weight: 800; font-size: 17px; color: #1B3F5E; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                    <span style="width: 10px; height: 10px; border-radius: 50%; background: #00838F; display: inline-block;"></span> Tokenization
                </div>
                <div style="color: #374151; font-size: 14px; line-height: 1.6;">
                    Splitting sentences into individual meaningful linguistic tokens using Malaya's specialized tokenizer.
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown("""
            <div class="custom-card" style="border-left: 5px solid #265E7E; height: 100%;">
                <div style="font-weight: 800; font-size: 17px; color: #1B3F5E; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                    <span style="width: 10px; height: 10px; border-radius: 50%; background: #265E7E; display: inline-block;"></span> Stop-word Filter
                </div>
                <div style="color: #374151; font-size: 14px; line-height: 1.6;">
                    Filtering out common Malay filler words using a curated municipal domain stop-word list.
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_c:
            st.markdown("""
            <div class="custom-card" style="border-left: 5px solid #C2185B; height: 100%;">
                <div style="font-weight: 800; font-size: 17px; color: #1B3F5E; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                    <span style="width: 10px; height: 10px; border-radius: 50%; background: #C2185B; display: inline-block;"></span> Bigram Extraction
                </div>
                <div style="color: #374151; font-size: 14px; line-height: 1.6;">
                    Capturing two-word contextual phrases for robust representation of public customer sentiment.
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Phase 4: Data Mining ──────────────────────────────────────────────────
    with tab_m4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1B3F5E 0%, #265E7E 100%); color: white; padding: 32px 40px; border-radius: 16px; box-shadow: 0 12px 32px rgba(27, 63, 94, 0.2); margin-bottom: 28px; display: flex; align-items: center; gap: 32px; border: 1px solid #00838F;">
            <div style="background: rgba(232, 244, 248, 0.15); backdrop-filter: blur(10px); border: 2px solid #B2D8E8; border-radius: 20px; min-width: 88px; height: 88px; display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 900; box-shadow: 0 8px 24px rgba(0,0,0,0.15); color: #FFFFFF;">
                04
            </div>
            <div>
                <div style="font-size: 14px; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; color: #B2D8E8; margin-bottom: 6px;">Phase 4 • KDD Methodology</div>
                <h2 style="color: white; margin: 0 0 10px 0; font-size: 28px; font-weight: 800; border: none; padding: 0;">Data Mining & Model Training</h2>
                <p style="margin: 0; font-size: 16px; opacity: 0.95; line-height: 1.6; color: #E8F4F8;">
                    The core machine learning stage. We benchmarked two distinct architectures on an 80% training / 20% testing split to classify text into Positive, Neutral, and Negative: Multinomial Naive Bayes as a fast probabilistic baseline and LSTM as a deep recurrent neural network.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            <div class="custom-card" style="border-left: 5px solid #00838F; height: 100%;">
                <div style="font-weight: 800; font-size: 18px; color: #1B3F5E; margin-bottom: 12px; display: flex; align-items: center; gap: 10px;">
                    <span style="width: 12px; height: 12px; border-radius: 50%; background: #00838F; display: inline-block;"></span> Multinomial Naive Bayes
                </div>
                <div style="color: #374151; font-size: 15px; line-height: 1.8;">
                    • <b>Feature Input:</b> TF-IDF vectorised bigrams<br>
                    • <b>Performance:</b> Fast training & highly interpretable<br>
                    • <b>Role:</b> Serves as our robust baseline classification model<br>
                    • <b>Approach:</b> Probabilistic keyword-frequency mapping
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown("""
            <div class="custom-card" style="border-left: 5px solid #C2185B; height: 100%;">
                <div style="font-weight: 800; font-size: 18px; color: #1B3F5E; margin-bottom: 12px; display: flex; align-items: center; gap: 10px;">
                    <span style="width: 12px; height: 12px; border-radius: 50%; background: #C2185B; display: inline-block;"></span> Deep Learning LSTM
                </div>
                <div style="color: #374151; font-size: 15px; line-height: 1.8;">
                    • <b>Feature Input:</b> 128-dimension word embedding sequences<br>
                    • <b>Linguistic Power:</b> Captures word order & sentence context<br>
                    • <b>Nuance:</b> Resolves complex grammatical structures & negation<br>
                    • <b>Architecture:</b> Recurrent layers with Spatial Dropout
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Phase 5: Interpretation & Evaluation ─────────────────────────────────
    with tab_m5:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1B3F5E 0%, #C2185B 100%); color: white; padding: 32px 40px; border-radius: 16px; box-shadow: 0 12px 32px rgba(194, 24, 91, 0.25); margin-bottom: 28px; display: flex; align-items: center; gap: 32px; border: 1px solid #C2185B;">
            <div style="background: rgba(232, 244, 248, 0.15); backdrop-filter: blur(10px); border: 2px solid #B2D8E8; border-radius: 20px; min-width: 88px; height: 88px; display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 900; box-shadow: 0 8px 24px rgba(0,0,0,0.15); color: #FFFFFF;">
                05
            </div>
            <div>
                <div style="font-size: 14px; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; color: #B2D8E8; margin-bottom: 6px;">Phase 5 • KDD Methodology</div>
                <h2 style="color: white; margin: 0 0 10px 0; font-size: 28px; font-weight: 800; border: none; padding: 0;">Interpretation & Actionable Knowledge</h2>
                <p style="margin: 0; font-size: 16px; opacity: 0.95; line-height: 1.6; color: #E8F4F8;">
                    The final KDD phase transforms model outputs into actionable municipal intelligence. We evaluate models using Accuracy, Precision, Recall, and F1-Score, and generate Confusion Matrices. Beyond metrics, the dashboard synthesizes predictions into real-world operations—tracking sentiment weekly, extracting complaint themes, and empowering MPKP decision-making.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("""
            <div class="custom-card" style="border-left: 5px solid #00838F; height: 100%;">
                <div style="font-weight: 800; font-size: 17px; color: #1B3F5E; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                    <span style="width: 10px; height: 10px; border-radius: 50%; background: #00838F; display: inline-block;"></span> Model Metrics
                </div>
                <div style="color: #374151; font-size: 14px; line-height: 1.6;">
                    Accuracy, Precision, Recall & F1-Score rigorously evaluated on the 20% test split to ensure robust generalizability.
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown("""
            <div class="custom-card" style="border-left: 5px solid #265E7E; height: 100%;">
                <div style="font-weight: 800; font-size: 17px; color: #1B3F5E; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                    <span style="width: 10px; height: 10px; border-radius: 50%; background: #265E7E; display: inline-block;"></span> Trend Analysis
                </div>
                <div style="color: #374151; font-size: 14px; line-height: 1.6;">
                    Sentiment tracked across time to detect sudden satisfaction drops, complaint spikes, and emerging dining patterns.
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_c:
            st.markdown("""
            <div class="custom-card" style="border-left: 5px solid #C2185B; height: 100%;">
                <div style="font-weight: 800; font-size: 17px; color: #1B3F5E; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                    <span style="width: 10px; height: 10px; border-radius: 50%; background: #C2185B; display: inline-block;"></span> MPKP Reporting
                </div>
                <div style="color: #374151; font-size: 14px; line-height: 1.6;">
                    AI-driven executive report cards and formal advisory notices delivered directly for municipal food-tourism enforcement.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.markdown("### Model Evaluation - Test Set Performance")
    
    if not model_results:
        st.warning("No models trained yet. Please train models from the sidebar first to see evaluation metrics.")
        return
    
    # Calculate all metrics for evaluation
    all_metrics = {}
    
    for model_name, result in model_results.items():
        y_test = result['y_test']
        y_pred = result['y_pred']
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        all_metrics[model_name] = {
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1-Score': f1
        }
    
    # Display metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    metrics_list = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    columns = [col1, col2, col3, col4]
    
    for idx, metric in enumerate(metrics_list):
        with columns[idx]:
            # Generate the model scores HTML inside the card
            scores_html = ""
            for model_name, metrics in all_metrics.items():
                value = metrics[metric]
                # Pick a color based on performance (Teal for good, Navy for okay, Pink for critical)
                score_color = "#00838F" if value >= 0.70 else "#265E7E" if value >= 0.60 else "#C2185B"
                
                scores_html += f"""<div style="margin-bottom: 10px; padding: 12px; background: #F8FAFC; border-radius: 10px; border: 1px solid #B2D8E8; text-align: left;">
<div style="font-size: 11px; font-weight: 700; color: #37718E; text-transform: uppercase; letter-spacing: 0.5px;">{model_name}</div>
<div style="font-size: 26px; font-weight: 800; color: {score_color}; margin-top: 2px; letter-spacing: -0.5px;">{value:.3f}</div>
</div>"""
            
            # Card container HTML (no leading indents in multiline string)
            card_html = f"""<div class="custom-card" style="border-top: 4px solid #00838F; padding: 22px; border-radius: 16px; background: #FFFFFF; border: 1px solid #B2D8E8; box-shadow: 0 4px 15px rgba(0,0,0,0.04); display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
<div>
<h4 style="margin-top: 0; margin-bottom: 15px; color: #1B3F5E; font-size: 15px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.6px; text-align: center;">{metric}</h4>
{scores_html}
</div>
</div>"""
            st.markdown(card_html, unsafe_allow_html=True)
            
    st.markdown("---")
    
    # Comparison chart
    metrics_df = pd.DataFrame(all_metrics).T
    
    fig_metrics = go.Figure()
    for metric in metrics_df.columns:
        fig_metrics.add_trace(go.Bar(
            name=metric,
            x=metrics_df.index,
            y=metrics_df[metric],
            text=[f"{val:.3f}" for val in metrics_df[metric]],
            textposition='auto',
        ))
    
    fig_metrics.update_layout(
        title="Model Metrics Comparison",
        barmode='group',
        xaxis_title="Model",
        yaxis_title="Score",
        yaxis=dict(range=[0, 1]),
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig_metrics, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed model analysis
    st.markdown("### Detailed Model Analysis")
    
    for model_name, result in model_results.items():
        with st.expander(f"{model_name} Details", expanded=False):
            y_test = result['y_test']
            y_pred = result['y_pred']
            
            col1, col2 = st.columns(2)
            
            # Confusion Matrix
            with col1:
                cm = confusion_matrix(y_test, y_pred)
                unique_labels = sorted(set(y_test) | set(y_pred))
                
                fig_cm = go.Figure(data=go.Heatmap(
                    z=cm,
                    x=unique_labels,
                    y=unique_labels,
                    colorscale="Blues",
                    text=cm,
                    texttemplate="%{text}",
                    hovertemplate="True: %{y}<br>Predicted: %{x}<br>Count: %{z}<extra></extra>"
                ))
                fig_cm.update_layout(
                    title="Confusion Matrix",
                    xaxis_title="Predicted Label",
                    yaxis_title="True Label",
                    height=400
                )
                st.plotly_chart(fig_cm, use_container_width=True)
            
            # Classification Report
            with col2:
                report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
                report_df = pd.DataFrame(report).transpose()
                report_df = report_df[["precision", "recall", "f1-score", "support"]]
                report_df.columns = ["Precision", "Recall", "F1-Score", "Support"]
                
                # Round the values to 3 decimal places to avoid Jinja2 requirement
                report_df = report_df.round(3)
                
                st.markdown("#### Classification Report")
                st.dataframe(report_df, use_container_width=True)
            
            # Label distribution
            dist_data = pd.DataFrame({
                "True Labels": y_test.value_counts().sort_index(),
                "Predicted Labels": pd.Series(y_pred).value_counts().sort_index()
            }).fillna(0)
            
            fig_dist = go.Figure(data=[
                go.Bar(name="True", x=dist_data.index, y=dist_data["True Labels"]),
                go.Bar(name="Predicted", x=dist_data.index, y=dist_data["Predicted Labels"])
            ])
            fig_dist.update_layout(
                title="True vs Predicted Label Distribution",
                xaxis_title="Sentiment Label",
                yaxis_title="Count",
                barmode="group",
                height=400
            )
            st.plotly_chart(fig_dist, use_container_width=True)
