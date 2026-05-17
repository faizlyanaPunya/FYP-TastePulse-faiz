import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

def render(model_results):
    """Render About page with project flow and Model Evaluation performance metrics"""
    
    st.markdown("### 📖 About TastePulse")
    st.info("**TastePulse** is an interactive Sentiment Analysis dashboard designed to uncover insights driving Northern Malaysia's food tourism. By analyzing public opinion, it helps identify dining trends, assess customer satisfaction, and recommend strategic initiatives.")
    
    # Project Team Details
    st.markdown("### 👥 Project Team")
    import os
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 👨‍🎓 Supervisee")
        if os.path.exists("faiz.jpeg"):
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.image("faiz.jpeg", width=160)
        else:
            st.write("*(Pic)*")
        st.info("**Name:** Nur Faizlyana Binti Mohd Kamarul Ariffin\n\n**Matric No:** 300442 \n\n**Program:** Bachelor of Computer Science with hons.")

    with col2:
        st.markdown("#### 👨‍🏫 Supervisor")
        if os.path.exists("juhaida.jpeg"):
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.image("juhaida.jpeg", width=170)
        else:
            st.write("*(Pic)*")
        st.success("**Name:** Assoc. Prof. Ts. Dr. Juhaida Binti Abu Bakar\n\n**Institution:** Universiti Utara Malaysia (UUM)")

    st.markdown("---")
    st.markdown("#### 👥 Peer Dashboards")
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("##### 🍽️ TastePulse Dashboard")
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
        st.markdown("##### 🎨 ThemePulse Dashboard")
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
    
    st.markdown("### 🧠 What is Sentiment Analysis?")
    st.info("""
    Sentiment analysis is a machine learning technique used to determine whether text data is **positive, negative, or neutral**. 
    In the context of our work, we are actively analyzing what locals and tourists say about food destinations across **Northern Malaysia** in **Kubang Pasu** district to be specific. 
    Instead of manually reading thousands of reviews, we automate this process to identify trends, pinpointing exactly *what* went wrong and *when*.
    """)
    
    st.markdown("### 🔄 Detailed Project Flow — KDD Methodology")

    # ── Top overview: 5 phase cards without messy arrows ──────────────────────────────
    f1, f2, f3, f4, f5 = st.columns(5)

    with f1:
        st.info("#### 🎯 Phase 1\n**Selection**\nTarget Data")
    with f2:
        st.warning("#### 🧹 Phase 2\n**Preprocessing**\nData Cleaning")
    with f3:
        st.success("#### ⚙️ Phase 3\n**Transformation**\nFeature Eng.")
    with f4:
        st.error("#### 🤖 Phase 4\n**Data Mining**\nModel Training")
    with f5:
        st.info("#### 📊 Phase 5\n**Interpretation**\nEvaluation")

    st.markdown("#### 📖 The KDD Story — Phase by Phase")

    # ── KDD Process Diagram ───────────────────────────────────────────────────
    if os.path.exists("kdd_process.png"):
        img_l, img_c, img_r = st.columns([1, 8, 1])
        with img_c:
            st.image("kdd_process.png", caption="Figure: KDD (Knowledge Discovery in Databases) Process Flow", use_container_width=True)
    st.markdown("")

    # ── 5 methodology tabs (one per KDD phase) ────────────────────────────────
    tab_m1, tab_m2, tab_m3, tab_m4, tab_m5 = st.tabs([
        "🎯 1. Selection",
        "🧹 2. Preprocessing",
        "⚙️ 3. Transformation",
        "🤖 4. Data Mining",
        "📊 5. Interpretation & Evaluation",
    ])

    # ── Phase 1: Selection ────────────────────────────────────────────────────
    with tab_m1:
        c_icon, c_text = st.columns([1, 4])
        with c_icon:
            st.markdown("<div style='font-size:80px;text-align:center;margin-top:0;'>🕵️</div>", unsafe_allow_html=True)
        with c_text:
            st.info(
                "### Phase 1 — Selection\n\n"
                "The first step in KDD is identifying **what data to use**. "
                "We targeted **TikTok public posts and comments** from food-related pages within the "
                "**Kubang Pasu district** of Northern Malaysia. "
                "Using the **Apify Comment Scraper**, we harvested thousands of community reviews written "
                "in Malay, English, and local mixed dialects."
            )
        # Mini detail cards
        col_a, col_b = st.columns(2)
        with col_a:
            st.info(
                "**🎯 Target Domain**\n\n"
                "- Kubang Pasu district food outlets\n"
                "- TikTok public posts & comments\n"
                "- Focused on Northern Malaysia food tourism"
            )
        with col_b:
            st.warning(
                "**🛠️ Tools Used**\n\n"
                "- **Apify Comment Scraper** for data harvesting\n"
                "- TikTok as primary data source\n"
                "- Malay + English + local slang scope"
            )

    # ── Phase 2: Preprocessing ────────────────────────────────────────────────
    with tab_m2:
        c_icon, c_text = st.columns([1, 4])
        with c_icon:
            st.markdown("<div style='font-size:80px;text-align:center;margin-top:0;'>🧹</div>", unsafe_allow_html=True)
        with c_text:
            st.warning(
                "### Phase 2 — Preprocessing\n\n"
                "Raw social media data is extremely noisy. During this phase we cleaned and prepared "
                "the raw text before any further analysis. This included removing **duplicates**, "
                "stripping **URLs, HTML tags, and special characters**, and handling "
                "**mixed-language content** (Malay + English + local slang).\n\n"
                "We applied the **Malaya NLP library** — built specifically for the Malay language — "
                "to normalise casing and standardise common Malaysian shorthand "
                "(e.g. *x* → tidak, *nk* → nak)."
            )
        col_a, col_b = st.columns(2)
        with col_a:
            st.warning(
                "**🧹 Cleaning Steps**\n\n"
                "- Removed duplicates & null entries\n"
                "- Stripped URLs, HTML & special characters\n"
                "- Removed irrelevant emoji-only posts"
            )
        with col_b:
            st.success(
                "**🔧 Normalisation**\n\n"
                "- Malaya NLP for Malay text normalisation\n"
                "- Standardised Malaysian shorthand\n"
                "- Handled mixed Malay + English content"
            )

    # ── Phase 3: Transformation ───────────────────────────────────────────────
    with tab_m3:
        c_icon, c_text = st.columns([1, 4])
        with c_icon:
            st.markdown("<div style='font-size:80px;text-align:center;margin-top:0;'>⚙️</div>", unsafe_allow_html=True)
        with c_text:
            st.success(
                "### Phase 3 — Transformation\n\n"
                "Cleaned text must be converted into a format that machine learning models can process. "
                "We performed **Tokenisation** (splitting sentences into tokens), "
                "**Stop-word removal** (filtering out filler words), and "
                "**Bigram extraction** — capturing two-word phrases like *makanan sedap* or *layanan teruk* "
                "that carry richer meaning than single words in Malay context.\n\n"
                "For **Naive Bayes** we applied **TF-IDF vectorisation**. "
                "For **LSTM** we built **word embedding sequences** to capture word order."
            )
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.success(
                "**✂️ Tokenisation**\n\n"
                "Split sentences into individual meaningful tokens using Malaya tokeniser"
            )
        with col_b:
            st.info(
                "**🚫 Stop-word Removal**\n\n"
                "Removed Malay filler words using a curated stop-word list"
            )
        with col_c:
            st.warning(
                "**🔗 Bigram Extraction**\n\n"
                "Captured two-word phrases for richer Malay context representation"
            )

    # ── Phase 4: Data Mining ──────────────────────────────────────────────────
    with tab_m4:
        c_icon, c_text = st.columns([1, 4])
        with c_icon:
            st.markdown("<div style='font-size:80px;text-align:center;margin-top:0;'>🤖</div>", unsafe_allow_html=True)
        with c_text:
            st.error(
                "### Phase 4 — Data Mining\n\n"
                "This is where the core machine learning happens. We benchmarked **two distinct architectures** "
                "to classify text sentiment into Positive, Neutral, and Negative:\n\n"
                "- **Multinomial Naive Bayes:** A fast probabilistic model using TF-IDF features. "
                "Reliable, interpretable, and serves as a strong baseline.\n"
                "- **LSTM (Long Short-Term Memory):** A deep learning model that processes word *sequences*, "
                "allowing it to understand Malay grammar and contextual meaning far better than simpler models.\n\n"
                "Data was split **80% training / 20% testing** for a fair, unbiased evaluation."
            )
        col_a, col_b = st.columns(2)
        with col_a:
            st.info(
                "**📐 Multinomial Naive Bayes**\n\n"
                "- Input: TF-IDF vectorised bigrams\n"
                "- Fast & interpretable\n"
                "- Serves as the baseline model\n"
                "- Probabilistic keyword-frequency approach"
            )
        with col_b:
            st.error(
                "**🧠 LSTM (Deep Learning)**\n\n"
                "- Input: Word embedding sequences\n"
                "- Understands word order & context\n"
                "- Captures Malay linguistic nuances\n"
                "- More powerful for complex sentiment"
            )

    # ── Phase 5: Interpretation & Evaluation ─────────────────────────────────
    with tab_m5:
        c_icon, c_text = st.columns([1, 4])
        with c_icon:
            st.markdown("<div style='font-size:80px;text-align:center;margin-top:0;'>📈</div>", unsafe_allow_html=True)
        with c_text:
            st.info(
                "### Phase 5 — Interpretation & Evaluation\n\n"
                "The final KDD phase transforms model outputs into **actionable knowledge**. "
                "We evaluated both models using **Accuracy, Precision, Recall, and F1-Score** "
                "and generated **Confusion Matrices** to understand classification behaviour.\n\n"
                "Beyond metrics, the dashboard synthesises predictions into real-world insights — "
                "tracking sentiment trends over **4-week timeframes**, identifying complaint themes "
                "via **Word Cloud & Bigram** analysis, and delivering targeted recommendations "
                "for **MPKP** food-tourism enforcement decisions."
            )
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.success(
                "**📏 Model Metrics**\n\n"
                "Accuracy, Precision, Recall & F1-Score evaluated on the 20% test split"
            )
        with col_b:
            st.warning(
                "**🗓️ Trend Analysis**\n\n"
                "Sentiment tracked weekly to detect drops & complaints over time"
            )
        with col_c:
            st.info(
                "**🏛️ MPKP Reporting**\n\n"
                "Actionable insights delivered for food-tourism policy & enforcement"
            )
        
    st.markdown("---")
    
    st.markdown("### 🔍 Model Evaluation - Test Set Performance")
    
    if not model_results:
        st.warning("⚠️ No models trained yet. Please train models from the sidebar first to see evaluation metrics.")
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
            st.markdown(f"### {metric}")
            for model_name, metrics in all_metrics.items():
                value = metrics[metric]
                st.metric(model_name, f"{value:.3f}")
    
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
    st.markdown("### 📊 Detailed Model Analysis")
    
    for model_name, result in model_results.items():
        with st.expander(f"📈 {model_name} Details", expanded=False):
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
