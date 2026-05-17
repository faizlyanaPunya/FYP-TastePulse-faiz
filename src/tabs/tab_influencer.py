import streamlit as st
import pandas as pd
import plotly.express as px

def render_mpkp_card(title, description, icon, color_hex):
    """Simplified professional card for MPKP (OBJ 4)"""
    tint = f"{color_hex}15"
    card_html = f"""<div style="background:#FFFFFF;padding:24px;border-radius:16px;border-top:5px solid {color_hex};border:1px solid #B2D8E8;box-shadow:0 10px 30px rgba(0,0,0,0.04);margin-bottom:20px;min-height:160px;display:flex;flex-direction:column;transition:all 0.3s ease;"><div style="display:flex;align-items:center;gap:12px;margin-bottom:15px;"><div style="background:{tint};width:45px;height:45px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;border:1px solid {color_hex}30;">{icon}</div><h4 style="margin:0;color:#1B3F5E;font-size:18px;font-weight:800;letter-spacing:-0.02em;">{title}</h4></div><p style="margin:0;color:#37718E;font-size:14.5px;line-height:1.6;font-weight:500;">{description}</p></div>"""
    st.markdown(card_html, unsafe_allow_html=True)

def render(filtered_df, selected_place):
    st.markdown("## 📱 Social & Influencers")
    st.markdown("Analytics on user interactions and the content creators driving them.")
    st.markdown("---")
    
    if filtered_df.empty:
        st.warning("⚠️ No data available to display insights.")
        return
        
    df_copy = filtered_df.copy()
    avg_likes = df_copy['diggCount'].mean()
    avg_replies = df_copy['replyCommentTotal'].mean()
    avg_sentiment = df_copy['sentiment_score'].mean()
    
    # Theme Colors
    color_pos = "#00838F" # Teal
    color_neu = "#F59E0B" # Orange
    color_neg = "#C2185B" # Magenta
    color_border = "#B2D8E8" # Theme blue border
    color_text = "#1B3F5E" # Dark navy text
    
    st.markdown("### 🏛️ Simple Action Plan")
    col1, col2 = st.columns(2)
    
    with col1:
        if avg_sentiment > 0.7 and avg_likes > 5:
            render_mpkp_card("Great Tourism Candidate", f"This shop is very popular ({avg_likes:.1f} likes) and people love it. MPKP should use this shop in official tourism videos.", "🏆", color_pos)
        elif avg_sentiment > 0.7 and avg_likes <= 5:
            render_mpkp_card("Hidden Gem Found", f"People love the food here ({avg_sentiment:.2f} score), but not many people know about it yet. MPKP should help promote this shop.", "💎", "#2196F3")
        else:
            render_mpkp_card("Needs Better Quality", "Customer rating is low. The shop should fix their food or service before MPKP starts to promote them.", "🛠️", "#9E9E9E")

    with col2:
        reply_ratio = avg_replies / avg_likes if avg_likes > 0 else 0
        if reply_ratio > 0.5:
            render_mpkp_card("Viral Complaint Warning", f"Many people are arguing or complaining in the comments. MPKP should check if the shop is having service problems.", "🚨", color_neg)
        else:
            render_mpkp_card("Positive Social Media Growth", "The conversation is calm and positive. People are mostly sharing the menu and liking the videos.", "📈", "#10b981")
            
    st.markdown("<hr style='border: 0; border-top: 1px solid #B2D8E8; margin: 30px 0;'>", unsafe_allow_html=True)
    st.markdown("### 🏆 Top Contributors")
    
    urls = filtered_df['videoWebUrl'].astype(str)
    usernames = urls.str.extract(r'(@[\w.-]+)')[0].fillna('Unknown')
    temp_df = filtered_df.copy()
    temp_df['username'] = usernames

    influencer_stats = temp_df.groupby('username').agg(
        total_videos=('text', 'count'),
        avg_sentiment=('sentiment_score', 'mean'),
        total_likes=('diggCount', 'sum'),
        total_replies=('replyCommentTotal', 'sum')
    ).reset_index()
    
    influencer_stats = influencer_stats.sort_values(by='total_likes', ascending=False)
    valid_influencers = influencer_stats[influencer_stats['username'] != 'Unknown']
    top_list = valid_influencers.head(3) if not valid_influencers.empty else influencer_stats.head(3)

    if not top_list.empty:
        cols = st.columns(min(len(top_list), 3))
        for i, (idx, row) in enumerate(top_list.iterrows()):
            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
            user = row['username']
            likes = int(row['total_likes'])
            videos = int(row['total_videos'])
            avg_likes = int(likes / videos) if videos > 0 else likes
            sentiment = row['avg_sentiment']
            
            color = color_pos if sentiment >= 0.6 else color_neu if sentiment >= 0.4 else color_neg
            status = "" if sentiment >= 0.6 else "Balanced View 🔅" if sentiment >= 0.4 else "Critical Voice 🍎"
            status_tag = f'<span style="color: {color}; font-weight: 600;">{status}</span>' if status else ''
            
            with cols[i]:
                card_html = f"""<div class="custom-card" style="border-top: 4px solid {color}; border: 1px solid {color_border}; text-align: center; padding: 20px;"><h1 style="font-size: 3rem; margin-bottom: 0px;"><span style='-webkit-text-fill-color: initial;'>{medal}</span></h1><h3 style="margin-top: 5px; margin-bottom: 15px; color: {color_text};">{user}</h3><div style="background: rgba(0,0,0,0.03); padding: 15px; border-radius: 10px; margin-bottom: 15px;"><p style="margin: 0; font-size: 24px; font-weight: 800; color: {color_pos};">{avg_likes:,}</p><p style="margin: 0; font-size: 13px; color: #6b7c6e; text-transform: uppercase;">Avg Likes / Video</p></div><div style="margin-bottom: 15px;"><a href="https://www.tiktok.com/{user.strip()}" target="_blank" style="background:#1B3F5E; color:white; padding:8px 18px; border-radius:20px; font-size:13px; font-weight:600; text-decoration:none; display:inline-flex; align-items:center; gap:8px; box-shadow:0 2px 8px rgba(0,0,0,0.15);"><span style="color:#fe2c55; font-size:15px;">🎵</span> Visit Profile</a></div><div style="display: flex; justify-content: space-between; font-size: 14px; padding: 0 10px; margin-top: 10px;"><span style="color: #6b7c6e;"><strong>{videos}</strong> Videos</span>{status_tag}</div></div>"""
                st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🔍 Deep-Dive by Influencer")
    
    influencer_options = ["All Influencers"] + valid_influencers['username'].tolist()
    selected_influencer = st.selectbox("Select an influencer:", options=influencer_options)
    
    if selected_influencer == "All Influencers":
        fig = px.bar(valid_influencers.head(15), x='username', y='total_likes', color='avg_sentiment', color_continuous_scale=[color_neg, color_neu, color_pos], labels={'total_likes': 'Total Likes', 'username': 'Influencer'})
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        inf_df = temp_df[temp_df['username'] == selected_influencer]
        inf_stats = influencer_stats[influencer_stats['username'] == selected_influencer]
        avg_sent = float(inf_stats['avg_sentiment'].iloc[0]) if not inf_stats.empty else 0
        sentiment_label = "" if avg_sent >= 0.6 else "Balanced View 🔅" if avg_sent >= 0.4 else "Critical Voice 🍎"
        sentiment_color = color_pos if avg_sent >= 0.6 else color_neu if avg_sent >= 0.4 else color_neg

        import requests
        avatar_url, followers, total_vid, total_likes, nickname, is_verified, bio = None, "Unknown", "Unknown", "Unknown", "", False, ""
        try:
            res = requests.get(f"https://www.tikwm.com/api/user/info?unique_id={selected_influencer.replace('@','')}", timeout=3).json()
            if res.get('code') == 0:
                u = res['data']['user']; s = res['data']['stats']
                avatar_url, nickname, is_verified, bio = u.get('avatarMedium'), u.get('nickname',''), u.get('verified', False), u.get('signature','')
                def f(n): return f"{n/1e6:.1f}M" if n>1e6 else f"{n/1e3:.1f}K" if n>1e3 else str(n)
                followers, total_vid, total_likes = f(s.get('followerCount',0)), f(s.get('videoCount',0)), f(s.get('heartCount',0))
        except: pass
            
        avatar_img = f'<img src="{avatar_url}" style="width:100%;height:100%;object-fit:cover;border-radius:50%;box-shadow:0 4px 10px rgba(0,0,0,0.15);">' if avatar_url else '<div style="width:100%;height:100%;border-radius:50%;background:linear-gradient(135deg,#1B3F5E,#000);display:flex;align-items:center;justify-content:center;font-size:32px;color:white;">📸</div>'
        
        safe_bio = ""
        if bio:
            b = bio[:150].replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;').replace("'", "&#39;").replace('\n','<br>')
            safe_bio = f'<p style="margin-top:15px;font-size:12px;color:#64748b;font-style:italic;line-height:1.4;">"{b}{"..." if len(bio)>150 else ""}"</p>'

        label_html = f'<span style="background:{sentiment_color}15;padding:6px 14px;border-radius:20px;color:{sentiment_color};font-weight:600;border:1px solid {sentiment_color}30;font-size:13px;">{sentiment_label}</span>' if sentiment_label else ""
        verified_html = f' <span title="Verified" style="color:#20d5ec;font-size:18px;">✅</span>' if is_verified else ""

        profile_html = f"""<div style="display:flex;gap:20px;flex-wrap:wrap;margin-bottom:30px;align-items:stretch;"><div style="flex:1;min-width:250px;display:flex;flex-direction:column;gap:20px;"><div style="background:#FFFFFF;border-radius:16px;border:1px solid {color_border};padding:30px 20px;box-shadow:0 8px 30px rgba(0,0,0,0.04);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;flex:1;"><div style="width:90px;height:90px;margin-bottom:15px;">{avatar_img}</div><h2 style="margin:0;color:{color_text};font-size:24px;font-weight:800;letter-spacing:-0.5px;">{nickname if nickname else selected_influencer}{verified_html}</h2><p style="margin:5px 0 15px 0;color:#64748b;font-size:14px;font-weight:600;">{selected_influencer}</p>{label_html}{safe_bio}</div><a href="https://www.tiktok.com/{selected_influencer.strip()}" target="_blank" style="background:#1B3F5E;color:white;border-radius:16px;padding:16px;text-decoration:none;font-weight:600;font-size:15px;display:flex;justify-content:center;align-items:center;gap:10px;box-shadow:0 4px 15px rgba(0,0,0,0.2);"><span style="font-size:18px;color:#fe2c55;">🎵</span> View TikTok Profile</a></div><div style="flex:2;min-width:300px;display:flex;flex-direction:column;gap:20px;"><div style="background:#FFFFFF;border-radius:16px;border:1px solid {color_border};padding:25px;box-shadow:0 8px 30px rgba(0,0,0,0.04);flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;"><div style="font-size:30px;margin-bottom:5px;">👥</div><div style="font-size:38px;font-weight:800;color:{color_text};">{followers}</div><div style="font-size:13px;color:#64748b;font-weight:600;text-transform:uppercase;">Total Followers</div></div><div style="display:flex;gap:20px;flex:1;"><div style="background:#FFFFFF;border-radius:16px;border:1px solid {color_border};padding:20px;box-shadow:0 8px 30px rgba(0,0,0,0.04);flex:1;text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center;"><div style="font-size:26px;">📺</div><div style="font-size:28px;font-weight:800;color:{color_text};">{total_vid}</div><div style="font-size:11px;color:#64748b;font-weight:600;text-transform:uppercase;">Total Videos</div></div><div style="background:#FFFFFF;border-radius:16px;border:1px solid {color_border};padding:20px;box-shadow:0 8px 30px rgba(0,0,0,0.04);flex:1;text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center;"><div style="font-size:26px;">❤️</div><div style="font-size:28px;font-weight:800;color:{color_text};">{total_likes}</div><div style="font-size:11px;color:#64748b;font-weight:600;text-transform:uppercase;">Total Likes</div></div></div></div></div>"""
        st.markdown(profile_html, unsafe_allow_html=True)

        if not inf_df.empty:
            feedbacks = [r for _, r in inf_df.head(3).iterrows()]
            cols = st.columns(3)
            for j, row in enumerate(feedbacks):
                p, d, s, t, v = str(row.get('place','')), str(row.get('createTimeISO','')), str(row.get('sentiment','')).upper(), str(row.get('text','')), str(row.get('videoWebUrl','#'))
                c = color_pos if s=="POSITIVE" else color_neg if s=="NEGATIVE" else color_neu
                card = f"""<div style="background:#FFFFFF;border-radius:14px;padding:20px;margin-bottom:20px;box-shadow:0 4px 20px rgba(0,0,0,0.04);border:1px solid {color_border};border-left:6px solid {c};display:flex;flex-direction:column;min-height:250px;height:100%;"><div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:15px;flex-wrap:wrap;gap:10px;"><div style="font-size:11px;font-weight:800;color:{c};background:{c}15;padding:4px 10px;border-radius:20px;border:1px solid {c}30;letter-spacing:0.5px;">{s}</div><div style="font-size:12px;color:#64748b;font-weight:600;display:flex;flex-direction:column;align-items:flex-end;gap:4px;"><span>📍 {p}</span><span>🕒 {d}</span></div></div><div style="font-size:15px;color:{color_text};margin-bottom:20px;line-height:1.5;font-weight:500;font-style:italic;flex-grow:1;">"{t}"</div><div style="display:flex;justify-content:center;margin-top:auto;"><a href="{v}" target="_blank" style="font-size:13px;background:#1B3F5E;color:white;padding:10px 0;width:100%;text-align:center;border-radius:8px;text-decoration:none;font-weight:600;display:inline-flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 4px 15px rgba(0,0,0,0.15);"><span style="color:#fe2c55;font-size:16px;">🎵</span> Watch Video</a></div></div>"""
                with cols[j]: st.markdown(card, unsafe_allow_html=True)
