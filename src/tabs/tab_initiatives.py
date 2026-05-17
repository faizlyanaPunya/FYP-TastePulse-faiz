import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

def calculate_sentiment_health_score(place_df):
    """Calculates a score from 0-100 based on customer reviews (predicted_sentiment if available, else sentiment)"""
    if place_df.empty:
        return 0
    
    # Use model predictions if available, else ground truth
    target_col = 'predicted_sentiment' if 'predicted_sentiment' in place_df.columns else 'sentiment'
    
    if target_col not in place_df.columns:
        # Fallback to sentiment_score if no label columns exist
        return place_df['sentiment_score'].mean() * 100 if 'sentiment_score' in place_df.columns else 50
        
    sentiments = place_df[target_col].str.lower()
    total = len(sentiments)
    
    pos = len(sentiments[sentiments == 'positive'])
    neu = len(sentiments[sentiments == 'neutral'])
    
    # NPS-like calculation normalized to 0-100
    # Formula: (Positive + 0.5 * Neutral) / Total * 100
    score = ((pos + (0.5 * neu)) / total) * 100
    return score

def calculate_aspect_score(place_df, keywords):
    """Calculates sentiment health score explicitly for records mentioning given keywords"""
    if place_df.empty:
        return None
    # match any keyword with word boundaries
    pattern = '|'.join([rf'\b{kw}\b' for kw in keywords])
    subset = place_df[place_df['text'].str.contains(pattern, case=False, na=False, regex=True)]
    if len(subset) < 2: 
        return None
    return calculate_sentiment_health_score(subset)

INFRA_KEYWORDS = ['parking', 'parkir', 'meja', 'kerusi', 'sesak', 'jam', 'kipas', 'panas', 'kemudahan', 'fasiliti', 'jalan', 'toilet', 'tandas']
HYGIENE_KEYWORDS = ['tikus', 'lipas', 'kotor', 'keracunan', 'sakit perut', 'lalat', 'tandas', 'hapak', 'busuk', 'bau']
PRICING_KEYWORDS = ['murah', 'mahal', 'harga', 'berbaloi', 'duit', 'mahai']
SERVICE_KEYWORDS = ['staff', 'servis', 'layanan', 'lambat', 'cepat', 'pekerja', 'tunggu']
PORTION_KEYWORDS = ['portion', 'banyak', 'sikit', 'kenyang', 'ciput']


def get_top_keywords(place_df, sentiment_type):
    """Extract actual common words or bigrams from the text, rather than a hardcoded list"""
    target_col = 'predicted_sentiment' if 'predicted_sentiment' in place_df.columns else 'sentiment'
    filtered_df = place_df[place_df[target_col].str.lower() == sentiment_type]
    
    if filtered_df.empty:
        return []
        
    # If the user has a bigrams column, use it!
    if 'bigrams' in filtered_df.columns:
        # Try to parse stringified lists or just count comma separated
        all_words = " ".join(filtered_df['bigrams'].dropna().astype(str)).replace('[', '').replace(']', '').replace("'", "").split(',')
        words = [w.strip().lower() for w in all_words if len(w.strip()) > 2]
    else:
        # Fallback: simple split of text (basic tokenization)
        text_data = " ".join(filtered_df['text'].dropna().astype(str)).lower()
        words = [word for word in text_data.split() if len(word) > 4] # ignore very short words
        
    if not words:
        return []
        
    # Get top most common, but filter out some possible Malay stop words
    malay_stopwords = ['tidak', 'yang', 'untuk', 'dengan', 'pada', 'dari', 'akan', 'lebih', 'boleh', 'telah']
    count = Counter(words)
    return [word for word, freq in count.most_common(8) if word not in malay_stopwords][:3]

def render_initiative_card(title, strategy, recommendation, priority_label, priority_value, color="#4CAF50"):
    """Creates a clean box using the global custom-card class"""
    st.markdown(f"""
        <div class="custom-card" style="border-left: 5px solid {color}; padding: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <h4 style="margin: 0; color: #3d4f42; font-family: 'Space Grotesk', sans-serif;">{title}</h4>
                <span style="background: {color}22; color: {color}; padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 14px;">
                    {priority_label}: {priority_value}
                </span>
            </div>
            <p style="margin: 5px 0; color: #5a6c5d; font-size: 15px;"><b>Strategy:</b> {strategy}</p>
            <div style="background-color: {color}11; padding: 15px; border-radius: 10px; border: 1px solid {color}44; color: #2d3f32; margin-top: 15px; font-weight: 500;">
                💡 <b>Action Item:</b> {recommendation}
            </div>
        </div>
    """, unsafe_allow_html=True)


def render(df, selected_place="All Places"):
    """Main page that shows advice based on your data"""
    if df.empty:
        st.warning("⚠️ No data found.")
        return

    st.markdown("## 💡 Actionable Initiatives & Strategies")
    st.markdown("Data-driven recommendations to improve food tourism in Northern Malaysia based on your model predictions.")
    st.markdown("---")
    
    if selected_place == "All Places":
        st.info("👆 Choose a specific food destination on the sidebar to see targeted improvement strategies.")
        
        # === RESTORED: MPKP Hygiene & Infrastructure Global Roster ===
        st.markdown("### 🚨 MPKP District Maintenance & Hygiene Roster")
        st.markdown("Automated assessment of restaurant health and public infrastructure in Kubang Pasu.")
        
        h_pattern = '|'.join([rf'\b{kw}\b' for kw in HYGIENE_KEYWORDS])
        i_pattern = '|'.join([rf'\b{kw}\b' for kw in INFRA_KEYWORDS])
        
        places_list = sorted(df['place'].unique().tolist())
        dashboard_data = []
        for p in places_list:
            p_df = df[df['place'] == p]
            h_violations = p_df[p_df['text'].str.contains(h_pattern, case=False, na=False, regex=True)]
            
            h_status = "🚨 Warning" if not h_violations.empty else "✅ Passed"
            i_score = calculate_aspect_score(p_df, INFRA_KEYWORDS)
            i_status = f"{i_score:.1f}%" if i_score is not None else "No Data"
            
            overall = calculate_sentiment_health_score(p_df)
            
            dashboard_data.append({
                "Destination": p,
                "Health Score": f"{overall:.1f}%",
                "Hygiene": h_status,
                "Infra Status": i_status
            })
            
        roster_df = pd.DataFrame(dashboard_data).sort_values(by="Health Score")
        st.dataframe(roster_df, use_container_width=True, hide_index=True)
        st.markdown("<br><hr>", unsafe_allow_html=True)
        
        # Summary table showing how shops are doing
        places = sorted(df['place'].unique().tolist())
        summary_data = []
        for p in places:
            p_df = df[df['place'] == p]
            score = calculate_sentiment_health_score(p_df)
            summary_data.append({"Destination": p, "Health Score": score, "Total Reviews": len(p_df)})
        
        summary_df = pd.DataFrame(summary_data).sort_values(by="Health Score", ascending=False)
        
        # UI Improvement: Show a bar chart comparing top places instead of just a table
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("### 🏆 Destination Health Ranking")
            fig = px.bar(
                summary_df.head(10), # Show top 10 to avoid clutter
                x="Health Score", 
                y="Destination", 
                orientation='h',
                color="Health Score",
                color_continuous_scale="RdYlGn",
                text="Health Score"
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
            fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=400, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("### 📊 Detailed Summary")
            display_df = summary_df.copy()
            display_df["Health Score"] = display_df["Health Score"].apply(lambda x: f"{x:.1f}%")
            st.dataframe(display_df, use_container_width=True, hide_index=True)

        st.markdown("<br><hr>", unsafe_allow_html=True)
        st.markdown("### 📅 District-Wide Peak Visiting Days")
        if 'createTimeISO' in df.columns and not df['createTimeISO'].isna().all():
            # Create a copy to avoid SettingWithCopyWarning
            time_df = df.copy()
            # Ensure it is a datetime object to avoid .dt accessor errors
            time_df['createTimeISO'] = pd.to_datetime(time_df['createTimeISO'], errors='coerce')
            time_df = time_df.dropna(subset=['createTimeISO'])
            
            if not time_df.empty:
                time_df['day_name'] = time_df['createTimeISO'].dt.day_name()
                
                # Order from Sunday to Saturday
                days_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
                daily_counts = time_df['day_name'].value_counts().reindex(days_order).fillna(0).reset_index()
                daily_counts.columns = ['Day', 'Review Count']
                
                fig_time_global = px.line(
                    daily_counts, 
                    x='Day', 
                    y='Review Count',
                    markers=True
                )
                fig_time_global.update_traces(line_color="#9c27b0", marker=dict(size=8))
                fig_time_global.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': days_order}, height=350, margin=dict(t=20, b=20, l=20, r=20))
                st.plotly_chart(fig_time_global, use_container_width=True)
                
                if not daily_counts['Review Count'].sum() == 0:
                    peak_day_global = daily_counts.loc[daily_counts['Review Count'].idxmax()]
                    st.info(f"💡 **MPKP Insight:** The busiest day for food tourism across the district is **{peak_day_global['Day']}**. MPKP should ensure traffic control, parking availability, and waste collection are optimized around this period.")
            else:
                st.info("📅 Date data is empty.")
        else:
            st.info("🕒 Time data is not available.")

        # === COMPLAINT CATEGORY DRILL-DOWN ===
        st.markdown("<br><hr>", unsafe_allow_html=True)
        st.markdown("### 🗂️ Complaint Category Drill-Down")
        st.markdown("Select an MPKP department category to see which places are receiving the most complaints, along with raw evidence.")
        
        target_col = 'predicted_sentiment' if 'predicted_sentiment' in df.columns else 'sentiment'
        neg_df = df[df[target_col].str.lower() == 'negative'].copy()
        
        # Helper to get subset based on keywords
        def get_category_subset(data, keywords):
            pattern = '|'.join([rf'\b{kw}\b' for kw in keywords])
            return data[data['text'].str.contains(pattern, case=False, na=False, regex=True)]
            
        hyg_df = get_category_subset(neg_df, HYGIENE_KEYWORDS)
        srv_df = get_category_subset(neg_df, SERVICE_KEYWORDS)
        prc_df = get_category_subset(neg_df, PRICING_KEYWORDS)
        inf_df = get_category_subset(neg_df, INFRA_KEYWORDS)
        
        cat_tabs = st.tabs([
            f"🧼 Hygiene ({len(hyg_df)})", 
            f"🛎️ Service ({len(srv_df)})", 
            f"💰 Pricing ({len(prc_df)})", 
            f"🏗️ Infrastructure ({len(inf_df)})"
        ])
        
        def render_category_tab(cat_df, title, color):
            if cat_df.empty:
                st.success(f"✅ No {title.lower()} complaints detected across the district.")
                return
                
            # Group by place to get count
            place_counts = cat_df['place'].value_counts().reset_index()
            place_counts.columns = ['Place', 'Complaint Count']
            
            st.markdown(f"<h4 style='color: {color}; margin-top: 10px;'>Complaint Counts by Destination ({title})</h4>", unsafe_allow_html=True)
            st.dataframe(place_counts, use_container_width=True, hide_index=True)
            
            st.markdown(f"**Raw Evidence ({title}):**")
            with st.expander(f"🔍 View All {len(cat_df)} {title} Complaint Reviews"):
                sorted_df = cat_df.sort_values(by='sentiment_score') if 'sentiment_score' in cat_df.columns else cat_df
                for idx, row in sorted_df.iterrows():
                    score_str = f"{row['sentiment_score']:.2f}" if 'sentiment_score' in row else 'N/A'
                    st.markdown(f"""
                    <div style="background: rgba(0,0,0,0.02); border-left: 3px solid {color}; padding: 15px; margin-bottom: 10px; border-radius: 4px;">
                        <div style="margin-bottom: 5px;">
                            <strong style="color: #1B3F5E;">{row['place']}</strong> 
                            <span style="color: {color}; font-size: 13px; font-weight: 600; background: {color}11; padding: 2px 8px; border-radius: 10px; margin-left: 10px;">Score: {score_str}</span>
                        </div>
                        <span style="font-style: italic; color: #2d3f32;">"{row['text']}"</span>
                    </div>
                    """, unsafe_allow_html=True)

        with cat_tabs[0]:
            render_category_tab(hyg_df, "Hygiene", "#C2185B")
        with cat_tabs[1]:
            render_category_tab(srv_df, "Service", "#F59E0B")
        with cat_tabs[2]:
            render_category_tab(prc_df, "Pricing", "#00838F")
        with cat_tabs[3]:
            render_category_tab(inf_df, "Infrastructure", "#37718E")

    else:
        place_df = df[df['place'] == selected_place]
        health = calculate_sentiment_health_score(place_df)
        
        # Get actual keywords
        neg_words = get_top_keywords(place_df, 'negative')
        pos_words = get_top_keywords(place_df, 'positive')

        # Display health score clearly
        st.markdown(f"### Score for **{selected_place}**")
        
        # Decide color and priority based on the score
        if health >= 70.0:
            status_color = "#00838F" # Theme Teal (Good)
            health_text = "Target Met (Excellent / Good)"
            growth_prio = "Very High"
            train_prio = "Low"
        elif health >= 50.0:
            status_color = "#F59E0B" # Theme Orange (Average)
            health_text = "Action Required (Average / Okay)"
            growth_prio = "Medium"
            train_prio = "Medium"
        else:
            status_color = "#C2185B" # Theme Magenta (Needs Work)
            health_text = "Critical Intervention Required"
            growth_prio = "Low"
            train_prio = "High (Urgent)"

        # Progress bar-style metric
        st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 15px; border: 1px solid rgba(123, 164, 145, 0.2); margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 10px;">
                    <span style="font-size: 18px; color: #5a6c5d; font-weight: 600;">Overall Sentiment Health</span>
                    <span style="font-size: 38px; font-weight: 800; color: {status_color}; font-family: 'Space Grotesk', sans-serif;">{health:.1f}%</span>
                </div>
                <div style="width: 100%; background-color: #eee; border-radius: 10px; height: 12px; overflow: hidden;">
                    <div style="width: {health}%; background-color: {status_color}; height: 100%; border-radius: 10px; transition: width 1s ease-in-out;"></div>
                </div>
                <div style="margin-top: 10px; color: #6b7c6e; font-size: 14px;">Assessment: <b>{health_text}</b></div>
            </div>
        """, unsafe_allow_html=True)

        # === RESTORED: MPKP Hygiene Check (Local) ===
        h_pattern = '|'.join([rf'\b{kw}\b' for kw in HYGIENE_KEYWORDS])
        violations_df = place_df[place_df['text'].str.contains(h_pattern, case=False, na=False, regex=True)]
        
        if not violations_df.empty:
            mentioned_kws = [kw for kw in HYGIENE_KEYWORDS if violations_df['text'].str.contains(rf'\b{kw}\b', case=False, regex=True).any()]
            st.markdown(f"""
            <div style="background-color: #ffebee; border-left: 5px solid #f44336; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <h4 style="color: #b71c1c; margin-top: 0;">🚨 CRITICAL HYGIENE WARNING</h4>
                <p style="color: #b71c1c; margin-bottom: 0;"><strong>{len(violations_df)} review(s)</strong> mention hygiene issues. <br>
                <strong>Keywords:</strong> {", ".join(mentioned_kws)}<br>
                <em>This location may be flagged for inspection.</em></p>
            </div>
            """, unsafe_allow_html=True)

        infra_score = calculate_aspect_score(place_df, INFRA_KEYWORDS)

        # Action 1: Marketing / Growth
        pos_str = ', '.join(pos_words) if pos_words else 'the great food'
        rec1 = f"Highlight '{pos_str}' in social media campaigns and apply for the 'Northern Food Trail' verified spot." if health >= 60 \
               else "Halt expanding marketing budgets temporarily. Focus on fixing core sentiment issues before inviting more tourists."
        
        render_initiative_card(
            "📣 1. Marketing & Tourism Growth",
            "Promoting the destination to a wider audience",
            rec1,
            "Urgency", growth_prio, status_color
        )

        # Action 2: Staff and Experience
        neg_str = ', '.join(neg_words) if neg_words else 'general service quality'
        rec2 = "Host a workshop for other local vendors on how to maintain high customer satisfaction." if health >= 80 \
               else f"Conduct an immediate service training session specifically addressing these recurring complaints from the AI model: '{neg_str}'."
        
        render_initiative_card(
            "👥 2. Service Quality & Training",
            "Upskilling staff and improving customer hospitality",
            rec2,
            "Urgency", train_prio, status_color
        )

        # Action 3: Infrastructure / Facilities
        vol = len(place_df)
        if not violations_df.empty:
            rec3 = "URGENT cleaning and pest control required. Postpone other upgrades until hygiene standards are met."
        elif infra_score is not None and infra_score < 45:
            rec3 = f"Infrastructure score is CRITICAL ({infra_score:.0f}%). Prioritize adding more seating or fixing ventilation/fans immediately."
        else:
            rec3 = "Submit a formal proposal to city council (MPKP) to upgrade parking or seating capacity due to high volume." if vol >= 15 \
                   else "Monitor review volume over the next 3 months to justify physical upgrades."
        
        render_initiative_card(
            "🏗️ 3. Facility Enhancements",
            "Upgrading physical shop aspects based on demand",
            rec3,
            "Impact", "High" if vol >= 15 or (infra_score is not None and infra_score < 45) else "Normal", 
            "#2196F3" if violations_df.empty else "#f44336"
        )

        st.markdown("<br><hr>", unsafe_allow_html=True)
        st.markdown("### 📅 Peak Visiting Days")
        if 'createTimeISO' in place_df.columns and not place_df['createTimeISO'].isna().all():
            p_time_df = place_df.copy()
            # Ensure it is a datetime object to avoid .dt accessor errors
            p_time_df['createTimeISO'] = pd.to_datetime(p_time_df['createTimeISO'], errors='coerce')
            p_time_df = p_time_df.dropna(subset=['createTimeISO'])
            
            if not p_time_df.empty:
                p_time_df['day_name'] = p_time_df['createTimeISO'].dt.day_name()
                
                # Order from Sunday to Saturday
                days_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
                daily_counts = p_time_df['day_name'].value_counts().reindex(days_order).fillna(0).reset_index()
                daily_counts.columns = ['Day', 'Review Count']
                
                fig_time = px.line(
                    daily_counts, 
                    x='Day', 
                    y='Review Count',
                    markers=True
                )
                fig_time.update_traces(line_color="#2196F3", marker=dict(size=8))
                fig_time.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': days_order}, height=300, margin=dict(t=20, b=20, l=20, r=20))
                st.plotly_chart(fig_time, use_container_width=True)
                
                if not daily_counts['Review Count'].sum() == 0:
                    peak_day = daily_counts.loc[daily_counts['Review Count'].idxmax()]
                    st.info(f"💡 **Business Insight:** Most reviews for {selected_place} are posted on **{peak_day['Day']}**. The owner should allocate more staff and prepare inventory before this peak day to maintain good service.")
            else:
                st.info("📅 Date data is empty for this place.")
        else:
            st.info("🕒 Time data is not available for this place.")