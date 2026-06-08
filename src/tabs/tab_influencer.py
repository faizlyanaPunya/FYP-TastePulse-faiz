# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
# pyrefly: ignore [missing-import]
import plotly.express as px
import requests

@st.cache_data(ttl=3600)
def get_tiktok_user_info(username):
    """Fetch TikTok user info using tikwm API, cached for performance"""
    clean_username = username.replace('@', '').strip()
    try:
        res = requests.get(f"https://www.tikwm.com/api/user/info?unique_id={clean_username}", timeout=3).json()
        if res.get('code') == 0:
            u = res['data']['user']
            s = res['data']['stats']
            
            # Format numbers helper
            def f(n):
                return f"{n/1e6:.1f}M" if n>1e6 else f"{n/1e3:.1f}K" if n>1e3 else str(n)
                
            return {
                "avatar": u.get('avatarMedium'),
                "nickname": u.get('nickname', ''),
                "verified": u.get('verified', False),
                "bio": u.get('signature', ''),
                "followers": f(s.get('followerCount', 0)),
                "videos": f(s.get('videoCount', 0)),
                "likes": f(s.get('heartCount', 0)),
                "success": True
            }
    except Exception:
        pass
    return {"success": False}

def render_mpkp_card(title, description, icon_type, color_hex):
    """Simplified professional card for MPKP (OBJ 4) with clean inline SVG icons"""
    tint = f"{color_hex}15"
    
    # SVG icon map (clean vectors instead of emojis)
    svg_icons = {
        "star": f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{color_hex}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>',
        "gem": f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{color_hex}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12l4 6-10 13L2 9z"></path><path d="M11 3 8 9l4 13 4-13-3-6"></path><path d="M2 9h20"></path></svg>',
        "alert": f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{color_hex}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
        "trend": f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{color_hex}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>',
    }
    
    icon_svg = svg_icons.get(icon_type, "")
    icon_div = f'<div style="background:{tint};width:45px;height:45px;border-radius:12px;display:flex;align-items:center;justify-content:center;border:1px solid {color_hex}30;">{icon_svg}</div>' if icon_svg else ""
    card_html = f"""<div style="background:#FFFFFF;padding:24px;border-radius:16px;border-top:5px solid {color_hex};border:1px solid #B2D8E8;box-shadow:0 10px 30px rgba(0,0,0,0.04);margin-bottom:20px;min-height:160px;display:flex;flex-direction:column;transition:all 0.3s ease;"><div style="display:flex;align-items:center;gap:15px;margin-bottom:15px;">{icon_div}<h4 style="margin:0;color:#1B3F5E;font-size:18px;font-weight:800;letter-spacing:-0.02em;">{title}</h4></div><p style="margin:0;color:#37718E;font-size:14.5px;line-height:1.6;font-weight:500;">{description}</p></div>"""
    st.markdown(card_html, unsafe_allow_html=True)

def render(filtered_df, selected_place):
    st.markdown("## Social & Influencers")
    st.markdown("Analytics on user interactions and the content creators driving them.")
    st.markdown("---")
    
    if filtered_df.empty:
        st.warning("No data available to display insights.")
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
    
    st.markdown("### Simple Action Plan")
    col1, col2 = st.columns(2)
    
    with col1:
        if avg_sentiment > 0.7 and avg_likes > 5:
            render_mpkp_card("Great Tourism Candidate", f"This shop is very popular ({avg_likes:.1f} likes) and people love it. MPKP should use this shop in official tourism videos.", "star", color_pos)
        elif avg_sentiment > 0.7 and avg_likes <= 5:
            render_mpkp_card("Hidden Gem Found", f"People love the food here ({avg_sentiment:.2f} score), but not many people know about it yet. MPKP should help promote this shop.", "gem", "#2196F3")
        else:
            render_mpkp_card("Needs Better Quality", "Customer rating is low. The shop should fix their food or service before MPKP starts to promote them.", "alert", "#9E9E9E")

    with col2:
        reply_ratio = avg_replies / avg_likes if avg_likes > 0 else 0
        if reply_ratio > 0.5:
            render_mpkp_card("Viral Complaint Warning", f"Many people are arguing or complaining in the comments. MPKP should check if the shop is having service problems.", "alert", color_neg)
        else:
            render_mpkp_card("Positive Social Media Growth", "The conversation is calm and positive. People are mostly sharing the menu and liking the videos.", "trend", "#10b981")
            
    st.markdown("<hr style='border: 0; border-top: 1px solid #B2D8E8; margin: 30px 0;'>", unsafe_allow_html=True)
    st.markdown("### Top Contributors")
    
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
            rank_str = f"#{i+1}"
            user = row['username']
            likes = int(row['total_likes'])
            videos = int(row['total_videos'])
            avg_likes = int(likes / videos) if videos > 0 else likes
            sentiment = row['avg_sentiment']
            
            color = color_pos if sentiment >= 0.6 else color_neu if sentiment >= 0.4 else color_neg
            status = "" if sentiment >= 0.6 else "Balanced View" if sentiment >= 0.4 else "Critical Voice"
            status_tag = f'<span style="color: {color}; font-weight: 600;">{status}</span>' if status else ''
            
            # Fetch TikTok info using the cached helper
            info = get_tiktok_user_info(user)
            avatar_html = ""
            if info.get("success") and info.get("avatar"):
                import urllib.parse
                encoded_avatar = urllib.parse.quote(info["avatar"])
                avatar_html = f'<img src="https://wsrv.nl/?url={encoded_avatar}" style="width:60px;height:60px;object-fit:cover;border-radius:50%;box-shadow:0 4px 12px rgba(0,0,0,0.15);border:2px solid #FFFFFF;margin: 10px auto 15px auto;display:block;">'
            else:
                # Fallback to initials if API fails or rate-limited
                initial = user.lstrip('@')[0].upper() if len(user) > 1 else 'U'
                if i == 0:
                    avatar_bg = "linear-gradient(135deg, #FFD700, #FFA500)" # Gold
                elif i == 1:
                    avatar_bg = "linear-gradient(135deg, #CFD8DC, #90A4AE)" # Silver
                else:
                    avatar_bg = "linear-gradient(135deg, #D7CCC8, #8D6E63)" # Bronze
                avatar_html = f'<div style="background: {avatar_bg}; color: #FFFFFF; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: 800; margin: 10px auto 15px auto; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 2px solid #FFFFFF;">{initial}</div>'
            rank_badge = f'<div style="margin-bottom: 8px;"><span style="background: {color}15; color: {color}; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;">Rank {rank_str}</span></div>'
            
            # Clean vector SVG for external link (no emojis)
            ext_link_svg = f'<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-left: 5px;"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>'
            
            with cols[i]:
                card_html = f"""<div class="custom-card" style="border-top: 4px solid {color}; border: 1px solid {color_border}; text-align: center; padding: 22px; border-radius: 16px; background: #FFFFFF; display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
<div>
{rank_badge}
{avatar_html}
<h3 style="margin-top: 0; margin-bottom: 15px; color: {color_text}; font-size: 17px; font-weight: 700; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{user}</h3>
<div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px; border-radius: 12px; margin-bottom: 15px;">
<p style="margin: 0; font-size: 26px; font-weight: 800; color: #1B3F5E; letter-spacing: -0.5px;">{avg_likes:,}</p>
<p style="margin: 0; font-size: 11px; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Avg Likes / Video</p>
</div>
</div>
<div>
<div style="margin-bottom: 15px;">
<a href="https://www.tiktok.com/{user.strip()}" target="_blank" style="background:#1B3F5E; color:white; padding:8px 18px; border-radius:20px; font-size:12px; font-weight:600; text-decoration:none; display:inline-flex; align-items:center; box-shadow:0 2px 8px rgba(27,63,94,0.25);">Visit Profile {ext_link_svg}</a>
</div>
<div style="display: flex; justify-content: space-between; align-items: center; font-size: 13px; padding-top: 12px; border-top: 1px solid #F1F5F9;">
<span style="color: #64748B; font-weight: 600;"><strong>{videos}</strong> Videos</span>
{status_tag}
</div>
</div>
</div>"""
                st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Deep-Dive by Influencer")
    
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
        sentiment_label = "" if avg_sent >= 0.6 else "Balanced View" if avg_sent >= 0.4 else "Critical Voice"
        sentiment_color = color_pos if avg_sent >= 0.6 else color_neu if avg_sent >= 0.4 else color_neg

        info = get_tiktok_user_info(selected_influencer)
        if info.get("success"):
            avatar_url = info.get("avatar")
            nickname = info.get("nickname")
            is_verified = info.get("verified")
            bio = info.get("bio")
            followers = info.get("followers")
            total_vid = info.get("videos")
            total_likes = info.get("likes")
        else:
            avatar_url, followers, total_vid, total_likes, nickname, is_verified, bio = None, "Unknown", "Unknown", "Unknown", "", False, ""
        import urllib.parse
        encoded_avatar = urllib.parse.quote(avatar_url) if avatar_url else None
        avatar_img = f'<img src="https://wsrv.nl/?url={encoded_avatar}" style="width:100%;height:100%;object-fit:cover;border-radius:50%;box-shadow:0 4px 10px rgba(0,0,0,0.15);">' if encoded_avatar else '<div style="width:100%;height:100%;border-radius:50%;background:#1B3F5E;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:bold;color:white;">USER</div>'
        
        safe_bio = ""
        if bio:
            b = bio[:150].replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;').replace("'", "&#39;").replace('\n','<br>')
            safe_bio = f'<p style="margin-top:15px;font-size:15px;color:#475569;font-style:italic;line-height:1.5;">"{b}{"..." if len(bio)>150 else ""}"</p>'

        label_html = f'<span style="background:{sentiment_color}15;padding:6px 14px;border-radius:20px;color:{sentiment_color};font-weight:600;border:1px solid {sentiment_color}30;font-size:13px;">{sentiment_label}</span>' if sentiment_label else ""
        verified_html = f' <span title="Verified" style="background:#20d5ec;color:white;font-size:12px;padding:3px 10px;border-radius:12px;vertical-align:middle;font-weight:bold;margin-left:8px;">VERIFIED</span>' if is_verified else ""

        profile_html = f"""<div style="display:flex;gap:20px;flex-wrap:wrap;margin-bottom:30px;align-items:stretch;"><div style="flex:1;min-width:250px;display:flex;flex-direction:column;gap:20px;"><div style="background:#FFFFFF;border-radius:16px;border:1px solid {color_border};padding:30px 20px;box-shadow:0 8px 30px rgba(0,0,0,0.04);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;flex:1;"><div style="width:110px;height:110px;margin-bottom:15px;">{avatar_img}</div><h2 style="margin:0;color:{color_text};font-size:30px;font-weight:800;letter-spacing:-0.5px;display:flex;align-items:center;justify-content:center;">{nickname if nickname else selected_influencer}{verified_html}</h2><p style="margin:5px 0 15px 0;color:#64748b;font-size:17px;font-weight:600;">{selected_influencer}</p>{label_html}{safe_bio}</div><a href="https://www.tiktok.com/{selected_influencer.strip()}" target="_blank" style="background:#1B3F5E;color:white;border-radius:16px;padding:16px;text-decoration:none;font-weight:600;font-size:15px;display:flex;justify-content:center;align-items:center;gap:10px;box-shadow:0 4px 15px rgba(0,0,0,0.2);">View TikTok Profile</a></div><div style="flex:2;min-width:300px;display:flex;flex-direction:column;gap:20px;"><div style="background:#FFFFFF;border-radius:16px;border:1px solid {color_border};padding:25px;box-shadow:0 8px 30px rgba(0,0,0,0.04);flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;"><div style="font-size:38px;font-weight:800;color:{color_text};">{followers}</div><div style="font-size:13px;color:#64748b;font-weight:600;text-transform:uppercase;">Total Followers</div></div><div style="display:flex;gap:20px;flex:1;"><div style="background:#FFFFFF;border-radius:16px;border:1px solid {color_border};padding:20px;box-shadow:0 8px 30px rgba(0,0,0,0.04);flex:1;text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center;"><div style="font-size:28px;font-weight:800;color:{color_text};">{total_vid}</div><div style="font-size:11px;color:#64748b;font-weight:600;text-transform:uppercase;">Total Videos</div></div><div style="background:#FFFFFF;border-radius:16px;border:1px solid {color_border};padding:20px;box-shadow:0 8px 30px rgba(0,0,0,0.04);flex:1;text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center;"><div style="font-size:28px;font-weight:800;color:{color_text};">{total_likes}</div><div style="font-size:11px;color:#64748b;font-weight:600;text-transform:uppercase;">Total Likes</div></div></div></div></div>"""
        st.markdown(profile_html, unsafe_allow_html=True)

        if not inf_df.empty:
            feedbacks = [r for _, r in inf_df.head(3).iterrows()]
            cols = st.columns(3)
            for j, row in enumerate(feedbacks):
                p, d, s, t, v = str(row.get('place','')), str(row.get('createTimeISO','')), str(row.get('sentiment','')).upper(), str(row.get('text','')), str(row.get('videoWebUrl','#'))
                c = color_pos if s=="POSITIVE" else color_neg if s=="NEGATIVE" else color_neu
                card = f"""<div style="background:#FFFFFF;border-radius:14px;padding:20px;margin-bottom:20px;box-shadow:0 4px 20px rgba(0,0,0,0.04);border:1px solid {color_border};border-left:6px solid {c};display:flex;flex-direction:column;min-height:250px;height:100%;"><div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:15px;flex-wrap:wrap;gap:10px;"><div style="font-size:11px;font-weight:800;color:{c};background:{c}15;padding:4px 10px;border-radius:20px;border:1px solid {c}30;letter-spacing:0.5px;">{s}</div><div style="font-size:12px;color:#64748b;font-weight:600;display:flex;flex-direction:column;align-items:flex-end;gap:4px;"><span>{p}</span><span>{d}</span></div></div><div style="font-size:15px;color:{color_text};margin-bottom:20px;line-height:1.5;font-weight:500;font-style:italic;flex-grow:1;">"{t}"</div><div style="display:flex;justify-content:center;margin-top:auto;"><a href="{v}" target="_blank" style="font-size:13px;background:#1B3F5E;color:white;padding:10px 0;width:100%;text-align:center;border-radius:8px;text-decoration:none;font-weight:600;display:inline-flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 4px 15px rgba(0,0,0,0.15);">Watch Video</a></div></div>"""
                with cols[j]: st.markdown(card, unsafe_allow_html=True)
