import streamlit as st
import pandas as pd
import io
from google import genai
from docx import Document

# ── Gemini setup (key from secrets.toml) ──────────────────────────────────────
def _get_gemini_client():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        if not api_key or api_key == "PASTE_YOUR_GEMINI_API_KEY_HERE":
            return None, "⚠️ Gemini API key not configured. Please update `.streamlit/secrets.toml`."
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"⚠️ Could not load Gemini client: {e}"


# ── Data summariser — sends stats only, never raw text ────────────────────────
def _summarise_data(df: pd.DataFrame) -> dict:
    summary = {}

    # Per-place stats
    place_stats = []
    for place, grp in df.groupby("place"):
        total = len(grp)
        counts = grp["sentiment"].value_counts()
        pos = counts.get("positive", 0)
        neg = counts.get("negative", 0)
        neu = counts.get("neutral", 0)
        pos_pct = round(pos / total * 100, 1)
        neg_pct = round(neg / total * 100, 1)
        neu_pct = round(neu / total * 100, 1)
        avg_score = round(grp["sentiment_score"].mean(), 3)

        # Top bigrams
        top_bigrams = []
        if "bigrams" in grp.columns:
            bigram_series = grp["bigrams"].dropna().astype(str)
            all_bigrams = []
            for row in bigram_series:
                all_bigrams.extend([b.strip() for b in row.split(",") if b.strip()])
            if all_bigrams:
                from collections import Counter
                top_bigrams = [b for b, _ in Counter(all_bigrams).most_common(5)]

        place_stats.append({
            "place": place,
            "total": total,
            "positive_pct": pos_pct,
            "negative_pct": neg_pct,
            "neutral_pct": neu_pct,
            "avg_score": avg_score,
            "top_bigrams": top_bigrams,
        })

    summary["place_stats"] = sorted(place_stats, key=lambda x: x["negative_pct"], reverse=True)

    # Weekly trend (last 4 weeks) for anomaly detection
    if "date" in df.columns:
        df2 = df.copy()
        df2["date"] = pd.to_datetime(df2["date"])
        df2["week"] = df2["date"].dt.to_period("W")
        weekly = (
            df2.groupby(["place", "week"])["sentiment"]
            .apply(lambda s: round((s == "negative").sum() / len(s) * 100, 1))
            .reset_index()
            .rename(columns={"sentiment": "neg_pct"})
        )
        anomalies = []
        for place, grp in weekly.groupby("place"):
            avg = grp["neg_pct"].mean()
            spikes = grp[grp["neg_pct"] > avg + 15]
            if not spikes.empty:
                for _, row in spikes.iterrows():
                    anomalies.append({
                        "place": place,
                        "week": str(row["week"]),
                        "neg_pct": row["neg_pct"],
                        "avg_neg_pct": round(avg, 1),
                    })
        summary["anomalies"] = anomalies
    else:
        summary["anomalies"] = []

    return summary


# ── Gemini call helper ─────────────────────────────────────────────────────────
_MODELS = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.0-flash"]

def _call_gemini(client, prompt: str) -> str:
    for model_name in _MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            err = str(e)
            if "429" in err or "RESOURCE_EXHAUSTED" in err:
                continue  # try next model
            return f"⚠️ Gemini error: {e}"
    return "⚠️ All Gemini models are currently quota-limited. Please try again in a few minutes."


# ── Prompt builders ────────────────────────────────────────────────────────────
def _build_report_prompt(summary: dict, lang: str) -> str:
    lang_str = "Bahasa Melayu Rasmi (formal administrative Malay)" if "Melayu" in lang else "English"
    lines = [f"You are an AI assistant helping MPKP (Majlis Perbandaran Kubang Pasu), a Malaysian municipal council, understand food tourism sentiment data. Write a professional Monthly Report Card in {lang_str}. For each place listed below, write 2-3 sentences summarising sentiment performance and give one specific, actionable recommendation for MPKP. Be concise and official in tone.\n\nData Summary:"]
    for p in summary["place_stats"]:
        lines.append(
            f"- {p['place']}: {p['total']} reviews | "
            f"{p['positive_pct']}% positive, {p['negative_pct']}% negative, {p['neutral_pct']}% neutral | "
            f"Avg sentiment score: {p['avg_score']} | "
            f"Top keywords: {', '.join(p['top_bigrams']) if p['top_bigrams'] else 'N/A'}"
        )
    lines.append("\nWrite the Report Card now:")
    return "\n".join(lines)


def _build_anomaly_prompt(summary: dict, lang: str) -> str:
    if not summary["anomalies"]:
        return None
    lang_str = "Bahasa Melayu Rasmi" if "Melayu" in lang else "English"
    lines = [f"You are an AI assistant for MPKP (Malaysian municipal council). Analyse these weekly negative sentiment spikes in food tourism reviews and explain what they likely mean, whether it signals a food safety or service issue, and what action MPKP should take. Be specific and professional. Answer in {lang_str}.\n\nAnomalies Detected:"]
    for a in summary["anomalies"]:
        lines.append(
            f"- {a['place']} during {a['week']}: {a['neg_pct']}% negative "
            f"(weekly average is {a['avg_neg_pct']}% — spike of +{round(a['neg_pct'] - a['avg_neg_pct'], 1)}%)"
        )
    lines.append("\nWrite the Anomaly Analysis now:")
    return "\n".join(lines)


def _build_positive_prompt(summary: dict, lang: str) -> str:
    top_places = sorted(summary["place_stats"], key=lambda x: x["positive_pct"], reverse=True)[:3]
    lang_str = "Bahasa Melayu Rasmi" if "Melayu" in lang else "English"
    lines = [f"You are an AI assistant for MPKP (Malaysian municipal council). Highlight what is working well in these top-performing food tourism locations and give MPKP specific recommendations on how to replicate their success at other locations. Be encouraging and practical. Answer in {lang_str}.\n\nTop Performing Places:"]
    for p in top_places:
        lines.append(
            f"- {p['place']}: {p['positive_pct']}% positive reviews | "
            f"Most praised topics: {', '.join(p['top_bigrams']) if p['top_bigrams'] else 'N/A'}"
        )
    lines.append("\nWrite the Positive Insights now:")
    return "\n".join(lines)


def _build_notice_prompt(p_stat: dict, notice_type: str, lang: str) -> str:
    lang_str = "Bahasa Melayu Rasmi (formal administrative Malay used by Malaysian government agencies)" if "Melayu" in lang else "formal English"
    top_kw = ", ".join(p_stat['top_bigrams']) if p_stat['top_bigrams'] else "general customer feedback"
    
    lines = [
        f"You are an Executive Administrative Officer for Majlis Perbandaran Kubang Pasu (MPKP).",
        f"Draft an official government formal advisory letter addressed to the Management of '{p_stat['place']}' in {lang_str}.",
        f"The notice type is: {notice_type}.",
        f"\nHere is the recent sentiment analysis data recorded by MPKP's monitoring system for this location:",
        f"- Total Reviews Analysed: {p_stat['total']}",
        f"- Sentiment Breakdown: {p_stat['positive_pct']}% Positive, {p_stat['neutral_pct']}% Neutral, {p_stat['negative_pct']}% Negative",
        f"- Overall Sentiment Health Score (0-1 scale): {p_stat['avg_score']}",
        f"- Primary Customer Keyword Complaints/Topics: {top_kw}",
        f"\nLetter Structure Requirements:",
        f"1. Header: Include official MPKP Rujukan Kami (Ref No: MPKP/JKP/2026/05-XXX) and Tarikh (current date placeholder).",
        f"2. Formal Salutation: Tuan/Puan, followed by a clear, capitalized formal subject line corresponding to {notice_type}.",
        f"3. Body Paragraph 1: Formally state that MPKP's tourism & sanitation monitoring system has reviewed their public customer feedback and state the key metrics.",
        f"4. Body Paragraph 2: If it is a warning/advisory (Hygiene/Service/Infra), formally request corrective action within 14 working days or state that MPKP health inspectors may conduct a premise visit. If it is a Commendation, congratulate them for boosting local Kubang Pasu tourism.",
        f"5. Professional Sign-off: 'Bahagian Kesihatan Persekitaran & Pelesenan, Majlis Perbandaran Kubang Pasu'.",
        f"\nWrite the formal letter now without any markdown code block syntax if possible, ready for professional document printing:"
    ]
    return "\n".join(lines)


def _build_chat_prompt(summary: dict, question: str, lang: str) -> str:
    lang_str = "Bahasa Melayu" if "Melayu" in lang else "English"
    
    lines = [
        f"You are an expert data analyst and municipal advisor for Majlis Perbandaran Kubang Pasu (MPKP).",
        f"Answer the user's question directly based on the aggregated dataset summary below.",
        f"Please answer in {lang_str}. Be highly insightful, professional, and clear.",
        f"\nUser Question: '{question}'",
        f"\nAggregated Dataset Summary for Kubang Pasu Food Destinations:"
    ]
    for p in summary["place_stats"][:30]:
        lines.append(
            f"- {p['place']}: {p['total']} reviews | "
            f"{p['positive_pct']}% pos, {p['negative_pct']}% neg, {p['neutral_pct']}% neu | "
            f"Avg score: {p['avg_score']} | "
            f"Keywords: {', '.join(p['top_bigrams']) if p['top_bigrams'] else 'N/A'}"
        )
    if summary["anomalies"]:
        lines.append("\nRecent Anomalies / Spikes Detected:")
        for a in summary["anomalies"]:
            lines.append(f"- {a['place']} in week {a['week']}: {a['neg_pct']}% negative (avg is {a['avg_neg_pct']}%)")
            
    lines.append("\nAnswer the question now:")
    return "\n".join(lines)


def _build_social_prompt(p_stat: dict, platform: str, lang: str) -> str:
    lang_str = "Bahasa Melayu (casual and engaging Malaysian social media style with popular local terms)" if "Melayu" in lang else "engaging Malaysian English"
    top_kw = ", ".join(p_stat['top_bigrams']) if p_stat['top_bigrams'] else "amazing local food"
    
    lines = [
        f"You are the official social media marketing manager for Majlis Perbandaran Kubang Pasu (MPKP) Tourism Board.",
        f"Create an engaging, viral promotional post for '{p_stat['place']}' tailored for {platform} in {lang_str}.",
        f"Here are the real metrics and customer praises for this location:",
        f"- Total Reviews: {p_stat['total']}",
        f"- Positive Rating: {p_stat['positive_pct']}% of visitors love this place!",
        f"- Most Praised Features / Dishes: {top_kw}",
        f"\nRequirements:",
        f"- Include an exciting hook at the beginning.",
        f"- Mention why foodies visiting Kedah / Kubang Pasu must try this spot.",
        f"- Use appropriate emojis throughout.",
        f"- End with a strong Call to Action (e.g., 'Save this post for your next trip to Kubang Pasu!').",
        f"- Include viral local hashtags: #VisitKedah #FoodieKubangPasu #MPKPTourism #KedahFood #MakanLokal.",
        f"\nWrite the post now:"
    ]
    return "\n".join(lines)


# ── Helper to create Word document ─────────────────────────────────────────────
def _create_word_doc(text: str) -> bytes:
    doc = Document()
    for line in text.split('\n'):
        doc.add_paragraph(line.strip())
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

# ── Callback functions for chat pills ──────────────────────────────────────────
def _set_query_hygiene():
    st.session_state.custom_query_input = "List the top 3 places with the most hygiene complaints and explain why."

def _set_query_service():
    st.session_state.custom_query_input = "Which places have the highest positive sentiment and what are customers praising?"

def _set_query_infra():
    st.session_state.custom_query_input = "Summarize the infrastructure and parking complaints across Kubang Pasu."


# ── Main render ────────────────────────────────────────────────────────────────
def render(df: pd.DataFrame):
    st.markdown("### 🤖 AI-Powered Municipal Insights & Operations")
    st.info(
        "This suite uses **Google Gemini AI** to transform your sentiment data into direct operational tools "
        "for MPKP officials — including report generation, advisory drafting, interactive Q&A, and social marketing."
    )

    if df is None or df.empty:
        st.warning("⚠️ No data available. Please upload and train a model first.")
        return

    # Load client
    client, error = _get_gemini_client()
    if error:
        st.error(error)
        st.markdown(
            "**To fix this:** Open `.streamlit/secrets.toml` and paste your Gemini API key. "
            "Get one free at [aistudio.google.com](https://aistudio.google.com)."
        )
        return

    # Compute summary once
    with st.spinner("📊 Analysing your data..."):
        summary = _summarise_data(df)

    st.success(f"✅ Data ready — {len(summary['place_stats'])} places analysed across {df['sentiment'].count():,} reviews.")
    st.markdown("---")

    # Global Settings / Language Selection Bar
    col_lang, col_sec = st.columns([1, 2])
    with col_lang:
        lang_choice = st.radio("🌐 Language / Bahasa:", ["English", "Bahasa Melayu (Rasmi)"], horizontal=True, key="ai_lang_toggle")
    with col_sec:
        st.caption("🔒 Privacy Assurance: Only aggregated statistical counts and top keyword phrases are sent to Google Gemini. Individual raw customer reviews and personal data are never shared.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── AI Functional Suite Tabs ──────────────────────────────────────────────
    tabs = st.tabs([
        "📊 Monthly Report Card", 
        "📜 MPKP Advisory Generator", 
        "💬 Chat with Data Advisor", 
        "📱 Social Campaign Builder", 
        "🚨 Anomaly Detector", 
        "🌟 Positive Insights"
    ])

    # ── Tab 1: Monthly Report Card ────────────────────────────────────────────
    with tabs[0]:
        st.markdown("#### 📋 MPKP Monthly Report Card")
        st.caption("AI-generated executive summary of sentiment performance per destination with recommended municipal actions.")

        if st.button("✨ Generate Monthly Report Card", key="btn_report"):
            with st.spinner("Gemini is writing the report card..."):
                prompt = _build_report_prompt(summary, lang_choice)
                st.session_state.ai_report_card = _call_gemini(client, prompt)

        if "ai_report_card" in st.session_state:
            st.markdown(st.session_state.ai_report_card)
            docx_bytes = _create_word_doc(st.session_state.ai_report_card)
            st.download_button(
                label="📥 Download Report Card (.docx)",
                data=docx_bytes,
                file_name="MPKP_Monthly_Report_Card.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="dl_report"
            )

    # ── Tab 2: MPKP Official Advisory Generator ───────────────────────────────
    with tabs[1]:
        st.markdown("#### 📜 MPKP Official Advisory Notice Generator")
        st.caption("Draft official formal notices or advisory letters from MPKP to restaurant management in formal administrative Malay or English.")
        
        places_list = [p["place"] for p in summary["place_stats"]]
        col1, col2 = st.columns(2)
        with col1:
            selected_place = st.selectbox("📌 Select Food Destination / Restaurant:", places_list, key="sel_notice_place")
        with col2:
            notice_type = st.selectbox(
                "📑 Select Advisory Type:", 
                [
                    "Hygiene & Sanitation Inspection Warning",
                    "Customer Service Improvement Advisory",
                    "Infrastructure / Parking Congestion Notice",
                    "Official Commendation (Excellent Performance)"
                ],
                key="sel_notice_type"
            )
            
        if st.button("✨ Draft Official Advisory Notice", key="btn_gen_notice"):
            with st.spinner(f"Gemini is drafting official notice for {selected_place}..."):
                p_stat = next((p for p in summary["place_stats"] if p["place"] == selected_place), None)
                prompt = _build_notice_prompt(p_stat, notice_type, lang_choice)
                st.session_state[f"ai_notice_{selected_place}"] = _call_gemini(client, prompt)
                
        if f"ai_notice_{selected_place}" in st.session_state:
            notice_text = st.session_state[f"ai_notice_{selected_place}"]
            st.markdown("##### 📄 Formal Letter Preview / Pratonton Surat Rasmi:")
            st.markdown(f'<div style="border:1px solid #cbd5e1; padding:30px; border-radius:10px; background:#f8fafc; color:#1e293b; font-family:serif; line-height:1.6; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">{notice_text.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            docx_bytes = _create_word_doc(notice_text)
            st.download_button(
                label=f"📥 Download Official Notice ({selected_place}.docx)",
                data=docx_bytes,
                file_name=f"MPKP_Notis_{selected_place.replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key=f"dl_notice_{selected_place}"
            )

    # ── Tab 3: Chat with Data Advisor ─────────────────────────────────────────
    with tabs[2]:
        st.markdown("#### 💬 AI Data Q&A Assistant")
        st.caption("Ask Gemini free-form questions about your Kubang Pasu food destination sentiment dataset.")
        
        if "custom_query_input" not in st.session_state:
            st.session_state.custom_query_input = ""

        st.markdown("**💡 Quick Ask / Soalan Pantas:**")
        cols = st.columns(3)
        cols[0].button("🏷️ Top Hygiene Violators", on_click=_set_query_hygiene, key="btn_q_hygiene")
        cols[1].button("🏷️ Best Customer Service", on_click=_set_query_service, key="btn_q_service")
        cols[2].button("🏷️ District Parking & Infra", on_click=_set_query_infra, key="btn_q_infra")
            
        query = st.text_input("💬 Ask your question about the data:", key="custom_query_input")
        
        if st.button("✨ Ask AI Advisor", key="btn_ask_advisor", type="primary") and query:
            with st.spinner("🤖 Gemini is analyzing your question..."):
                prompt = _build_chat_prompt(summary, query, lang_choice)
                st.session_state.chat_last_query = query
                st.session_state.chat_response = _call_gemini(client, prompt)
                
        if "chat_response" in st.session_state:
            st.markdown("---")
            st.markdown(f"**👤 You asked:** `{st.session_state.get('chat_last_query', query)}`")
            st.markdown("##### 🤖 Advisor Answer / Jawapan AI:")
            st.info(st.session_state.chat_response)

    # ── Tab 4: Social Campaign Builder ────────────────────────────────────────
    with tabs[3]:
        st.markdown("#### 📱 Food Tourism Social Media Campaign Builder")
        st.caption("Generate captivating, viral promotional posts for top-rated food destinations to boost Kubang Pasu food tourism.")
        
        top_places_list = [p["place"] for p in sorted(summary["place_stats"], key=lambda x: x["positive_pct"], reverse=True)]
        
        col1, col2 = st.columns(2)
        with col1:
            social_place = st.selectbox("📌 Select Destination to Promote:", top_places_list, key="sel_social_place")
        with col2:
            platform = st.selectbox("📲 Target Platform:", ["Instagram (Visual & Catchy)", "TikTok (Trendy & Viral)", "Facebook (Community & Descriptive)"], key="sel_social_platform")
            
        if st.button("✨ Generate Social Media Campaign", key="btn_gen_social"):
            with st.spinner(f"Gemini is creating viral campaign for {social_place}..."):
                p_stat = next((p for p in summary["place_stats"] if p["place"] == social_place), None)
                prompt = _build_social_prompt(p_stat, platform, lang_choice)
                st.session_state[f"ai_social_{social_place}_{platform}"] = _call_gemini(client, prompt)
                
        if f"ai_social_{social_place}_{platform}" in st.session_state:
            post_text = st.session_state[f"ai_social_{social_place}_{platform}"]
            st.markdown("##### 🚀 Campaign Copy / Salinan Kempen:")
            st.success(post_text)

    # ── Tab 5: Anomaly Detector ───────────────────────────────────────────────
    with tabs[4]:
        st.markdown("#### 🚨 Review Anomaly Detector")
        st.caption("Flags places with sudden spikes in negative sentiment — potential hygiene incidents or viral complaints.")

        anomaly_prompt = _build_anomaly_prompt(summary, lang_choice)
        if anomaly_prompt is None:
            st.success("✅ No anomalies detected — sentiment trends are stable across all places.")
        else:
            spike_count = len(summary["anomalies"])
            st.warning(f"⚠️ **{spike_count} anomalies detected** across your data. Click below for AI analysis.")
            if st.button("✨ Analyse Anomalies", key="btn_anomaly"):
                with st.spinner("Gemini is analysing the spikes..."):
                    st.session_state.ai_anomaly_analysis = _call_gemini(client, anomaly_prompt)
                    
            if "ai_anomaly_analysis" in st.session_state:
                st.markdown(st.session_state.ai_anomaly_analysis)
                docx_bytes = _create_word_doc(st.session_state.ai_anomaly_analysis)
                st.download_button(
                    label="📥 Download Anomaly Analysis (.docx)",
                    data=docx_bytes,
                    file_name="MPKP_Anomaly_Analysis.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key="dl_anomaly"
                )

    # ── Tab 6: Positive Insights ──────────────────────────────────────────────
    with tabs[5]:
        st.markdown("#### 🌟 What Worked? Positive Insights")
        st.caption("Highlights top-performing places and gives MPKP recommendations to replicate their success elsewhere.")

        if st.button("✨ Generate Positive Insights", key="btn_positive"):
            with st.spinner("Gemini is identifying what works..."):
                prompt = _build_positive_prompt(summary, lang_choice)
                st.session_state.ai_positive_insights = _call_gemini(client, prompt)
                
        if "ai_positive_insights" in st.session_state:
            st.markdown(st.session_state.ai_positive_insights)
            docx_bytes = _create_word_doc(st.session_state.ai_positive_insights)
            st.download_button(
                label="📥 Download Positive Insights (.docx)",
                data=docx_bytes,
                file_name="MPKP_Positive_Insights.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="dl_positive"
            )
