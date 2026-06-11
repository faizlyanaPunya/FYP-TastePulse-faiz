# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
# pyrefly: ignore [missing-import]
import plotly.express as px


# ── Helpers ───────────────────────────────────────────────────────────────────

def _initials_div(username, rank_index=3, size_px=60, font_size=24):
    """Pure HTML initials avatar with rank-coloured gradient."""
    initial = username.lstrip('@')[0].upper() if len(username) > 1 else 'U'
    grads = [
        "linear-gradient(135deg,#FFD700,#FFA500)",   # gold   – rank 1
        "linear-gradient(135deg,#CFD8DC,#90A4AE)",   # silver – rank 2
        "linear-gradient(135deg,#D7CCC8,#8D6E63)",   # bronze – rank 3
        "linear-gradient(135deg,#1B3F5E,#37718E)",   # navy   – other
    ]
    grad = grads[min(rank_index, 3)]
    return (
        f'<div style="background:{grad};color:#FFF;width:{size_px}px;height:{size_px}px;'
        f'border-radius:50%;display:flex;align-items:center;justify-content:center;'
        f'font-size:{font_size}px;font-weight:800;'
        f'box-shadow:0 4px 12px rgba(0,0,0,0.15);border:2px solid #FFF;">'
        f'{initial}</div>'
    )


def _avatar_img(username, rank_index, size_px, font_size):
    """
    <img> that the BROWSER fetches from unavatar.io (no Python HTTP call).
    onerror JS swaps in the initials div if the image cannot load.
    """
    clean   = username.replace('@', '').strip()
    src     = f"https://unavatar.io/tiktok/{clean}"
    initial = username.lstrip('@')[0].upper() if len(username) > 1 else 'U'
    grads   = [
        "linear-gradient(135deg,#FFD700,#FFA500)",
        "linear-gradient(135deg,#CFD8DC,#90A4AE)",
        "linear-gradient(135deg,#D7CCC8,#8D6E63)",
        "linear-gradient(135deg,#1B3F5E,#37718E)",
    ]
    grad = grads[min(rank_index, 3)]
    fb_style = (
        f"background:{grad};color:#FFF;width:{size_px}px;height:{size_px}px;"
        f"border-radius:50%;display:flex;align-items:center;justify-content:center;"
        f"font-size:{font_size}px;font-weight:800;"
        f"box-shadow:0 4px 12px rgba(0,0,0,.15);border:2px solid #FFF;"
    )
    img_style = (
        f"width:{size_px}px;height:{size_px}px;object-fit:cover;"
        f"border-radius:50%;box-shadow:0 4px 12px rgba(0,0,0,.15);border:2px solid #FFF;"
    )
    onerror = (
        f"this.style.display='none';"
        f"var d=document.createElement('div');"
        f"d.setAttribute('style','{fb_style}');"
        f"d.textContent='{initial}';"
        f"this.parentNode.appendChild(d);"
    )
    return f'<img src="{src}" style="{img_style}" onerror="{onerror}">'


# ── MPKP action card ──────────────────────────────────────────────────────────

def _mpkp_card(title, description, icon_type, color_hex):
    tint = f"{color_hex}15"
    icons = {
        "star":  f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{color_hex}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
        "gem":   f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{color_hex}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12l4 6-10 13L2 9z"/><path d="M11 3 8 9l4 13 4-13-3-6"/><path d="M2 9h20"/></svg>',
        "alert": f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{color_hex}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        "trend": f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{color_hex}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
    }
    icon_svg = icons.get(icon_type, "")
    icon_div = (
        f'<div style="background:{tint};width:45px;height:45px;border-radius:12px;'
        f'display:flex;align-items:center;justify-content:center;border:1px solid {color_hex}30;">'
        f'{icon_svg}</div>'
    ) if icon_svg else ""
    st.markdown(
        f'<div style="background:#FFF;padding:24px;border-radius:16px;border-top:5px solid {color_hex};'
        f'border:1px solid #B2D8E8;box-shadow:0 10px 30px rgba(0,0,0,.04);'
        f'margin-bottom:20px;min-height:160px;display:flex;flex-direction:column;">'
        f'<div style="display:flex;align-items:center;gap:15px;margin-bottom:15px;">'
        f'{icon_div}<h4 style="margin:0;color:#1B3F5E;font-size:18px;font-weight:800;">{title}</h4></div>'
        f'<p style="margin:0;color:#37718E;font-size:14.5px;line-height:1.6;font-weight:500;">{description}</p></div>',
        unsafe_allow_html=True,
    )


# ── Main render ───────────────────────────────────────────────────────────────

def render(filtered_df, selected_place):
    st.markdown("## Social & Influencers")
    st.markdown("Analytics on user interactions and the content creators driving them.")
    st.markdown("---")

    if filtered_df.empty:
        st.warning("No data available to display insights.")
        return

    avg_likes     = filtered_df['diggCount'].mean()
    avg_replies   = filtered_df['replyCommentTotal'].mean()
    avg_sentiment = filtered_df['sentiment_score'].mean()

    CP = "#00838F"   # teal   – positive
    CN = "#F59E0B"   # amber  – neutral
    CG = "#C2185B"   # rose   – negative
    CB = "#B2D8E8"   # border
    CT = "#1B3F5E"   # text

    # ── Simple Action Plan ────────────────────────────────────────────────────
    st.markdown("### Simple Action Plan")
    c1, c2 = st.columns(2)
    with c1:
        if avg_sentiment > 0.7 and avg_likes > 5:
            _mpkp_card("Great Tourism Candidate", f"Very popular ({avg_likes:.1f} avg likes) and well-loved. MPKP should feature this shop in official tourism videos.", "star", CP)
        elif avg_sentiment > 0.7:
            _mpkp_card("Hidden Gem Found", f"High sentiment ({avg_sentiment:.2f}) but low reach. MPKP should help promote this shop.", "gem", "#2196F3")
        else:
            _mpkp_card("Needs Better Quality", "Low customer rating. The shop should improve before MPKP promotion.", "alert", "#9E9E9E")
    with c2:
        if avg_likes > 0 and (avg_replies / avg_likes) > 0.5:
            _mpkp_card("Viral Complaint Warning", "High comment-to-like ratio. MPKP should check if the shop has service issues.", "alert", CG)
        else:
            _mpkp_card("Positive Social Media Growth", "Calm, positive conversation. People are sharing menus and liking videos.", "trend", "#10b981")

    st.markdown("<hr style='border:0;border-top:1px solid #B2D8E8;margin:30px 0;'>", unsafe_allow_html=True)

    # ── Build influencer stats from dataset ───────────────────────────────────
    temp_df = filtered_df.copy()
    temp_df['username'] = (
        filtered_df['videoWebUrl'].astype(str)
        .str.extract(r'(@[\w.-]+)')[0]
        .fillna('Unknown')
    )

    stats = (
        temp_df.groupby('username')
        .agg(
            total_videos=('text', 'count'),
            avg_sentiment=('sentiment_score', 'mean'),
            total_likes=('diggCount', 'sum'),
            total_replies=('replyCommentTotal', 'sum'),
        )
        .reset_index()
        .sort_values('total_likes', ascending=False)
    )
    valid = stats[stats['username'] != 'Unknown']
    top3  = valid.head(3) if not valid.empty else stats.head(3)

    ext_svg = (
        '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-left:5px;">'
        '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>'
        '<polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>'
    )

    # ── Top Contributors Leaderboard ──────────────────────────────────────────
    st.markdown("### Top Contributors")
    if not top3.empty:
        cols = st.columns(min(len(top3), 3))
        for i, (_, row) in enumerate(top3.iterrows()):
            user   = row['username']
            likes  = int(row['total_likes'])
            vids   = int(row['total_videos'])
            avgl   = int(likes / vids) if vids > 0 else likes
            sent   = row['avg_sentiment']
            color  = CP if sent >= 0.6 else CN if sent >= 0.4 else CG
            status = "Positive" if sent >= 0.6 else "Balanced" if sent >= 0.4 else "Critical"

            av = _avatar_img(user, i, 60, 24)
            card = (
                f'<div style="border-top:4px solid {color};border:1px solid {CB};text-align:center;'
                f'padding:22px;border-radius:16px;background:#FFF;display:flex;flex-direction:column;'
                f'justify-content:space-between;height:100%;">'
                # rank badge
                f'<div style="margin-bottom:8px;">'
                f'<span style="background:{color}15;color:{color};padding:4px 12px;border-radius:20px;'
                f'font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.5px;">Rank #{i+1}</span></div>'
                # avatar
                f'<div style="margin:8px auto 14px auto;width:{60}px;height:{60}px;">{av}</div>'
                # username
                f'<h3 style="margin:0 0 14px 0;color:{CT};font-size:16px;font-weight:700;'
                f'overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{user}</h3>'

                # visit profile button
                f'<div style="margin-bottom:12px;">'
                f'<a href="https://www.tiktok.com/{user.strip()}" target="_blank" '
                f'style="background:{CT};color:white;padding:8px 18px;border-radius:20px;font-size:12px;'
                f'font-weight:600;text-decoration:none;display:inline-flex;align-items:center;'
                f'box-shadow:0 2px 8px rgba(27,63,94,.25);">Visit Profile {ext_svg}</a></div>'
                # footer
                f'<div style="display:flex;justify-content:space-between;font-size:13px;'
                f'padding-top:10px;border-top:1px solid #F1F5F9;">'
                f'<span style="color:#64748B;font-weight:600;"><strong>{vids}</strong> Videos</span>'
                f'<span style="color:{color};font-weight:600;">{status}</span></div>'
                f'</div>'
            )
            with cols[i]:
                st.markdown(card, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Deep-Dive by Influencer ───────────────────────────────────────────────
    st.markdown("### Deep-Dive by Influencer")
    options  = ["All Influencers"] + valid['username'].tolist()
    selected = st.selectbox("Select an influencer:", options=options)

    if selected == "All Influencers":
        fig = px.bar(
            valid.head(15), x='username', y='total_likes',
            color='avg_sentiment',
            color_continuous_scale=[CG, CN, CP],
            labels={'total_likes': 'Total Likes', 'username': 'Influencer'},
        )
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                          margin=dict(t=20, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    else:
        inf_df    = temp_df[temp_df['username'] == selected]
        inf_stats = stats[stats['username'] == selected]

        # Local dataset stats (always available)
        tot_vids  = int(inf_stats['total_videos'].iloc[0])  if not inf_stats.empty else 0
        tot_likes = int(inf_stats['total_likes'].iloc[0])   if not inf_stats.empty else 0
        tot_repl  = int(inf_stats['total_replies'].iloc[0]) if not inf_stats.empty else 0
        avg_lk    = int(tot_likes / tot_vids) if tot_vids > 0 else 0
        avg_sent  = float(inf_stats['avg_sentiment'].iloc[0]) if not inf_stats.empty else 0

        sent_label = "Positive" if avg_sent >= 0.6 else "Balanced View" if avg_sent >= 0.4 else "Critical Voice"
        sent_color = CP if avg_sent >= 0.6 else CN if avg_sent >= 0.4 else CG
        sent_pct   = int(avg_sent * 100)

        rank_pos = valid['username'].tolist().index(selected) if selected in valid['username'].tolist() else 3

        # Profile picture — browser fetches, no Python HTTP
        av_large = _avatar_img(selected, rank_pos, 110, 44)

        label_html = (
            f'<span style="background:{sent_color}15;padding:6px 14px;border-radius:20px;'
            f'color:{sent_color};font-weight:600;border:1px solid {sent_color}30;font-size:13px;">'
            f'{sent_label}</span>'
        )
        sent_bar = (
            f'<div style="margin-top:14px;text-align:left;width:100%;">'
            f'<div style="display:flex;justify-content:space-between;font-size:12px;color:#64748b;font-weight:600;margin-bottom:5px;">'
            f'<span>Sentiment Score</span>'
            f'<span style="color:{sent_color};font-weight:700;">{avg_sent:.2f}</span></div>'
            f'<div style="background:#F1F5F9;border-radius:99px;height:8px;overflow:hidden;">'
            f'<div style="background:{sent_color};width:{sent_pct}%;height:100%;border-radius:99px;"></div>'
            f'</div></div>'
        )
        ext_lg = (
            '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="3" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>'
            '<polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>'
        )

        # ── Profile card ──────────────────────────────────────────────────────
        # Note: Followers / TikTok total likes are from TikTok's servers — shown
        # via the profile link. Local dataset stats are always shown below.
        profile_html = (
            f'<div style="display:flex;gap:20px;flex-wrap:wrap;margin-bottom:30px;align-items:stretch;">'

            # ── Left: avatar card + link ──────────────────────────────────────
            f'<div style="flex:1;min-width:240px;display:flex;flex-direction:column;gap:16px;">'
            f'<div style="background:#FFF;border-radius:16px;border:1px solid {CB};padding:28px 20px;'
            f'box-shadow:0 8px 30px rgba(0,0,0,.04);display:flex;flex-direction:column;'
            f'align-items:center;justify-content:center;text-align:center;flex:1;">'
            f'<div style="margin-bottom:16px;width:110px;height:110px;">{av_large}</div>'
            f'<h2 style="margin:0 0 4px 0;color:{CT};font-size:22px;font-weight:800;letter-spacing:-.5px;">{selected}</h2>'
            f'<p style="margin:0 0 12px 0;color:#94a3b8;font-size:13px;font-weight:500;">TikTok Creator</p>'
            f'{label_html}{sent_bar}'
            f'</div>'
            f'<a href="https://www.tiktok.com/{selected.strip()}" target="_blank" '
            f'style="background:{CT};color:white;border-radius:16px;padding:15px;text-decoration:none;'
            f'font-weight:600;font-size:14px;display:flex;justify-content:center;align-items:center;'
            f'gap:10px;box-shadow:0 4px 15px rgba(0,0,0,.2);">View TikTok Profile {ext_lg}</a>'
            f'</div>'

            # ── Right: stats (pure flexbox rows) ─────────────────────────────
            f'<div style="flex:2;min-width:300px;display:flex;flex-direction:column;gap:16px;">'

            # Row A: dataset total likes (hero, full-width)
            f'<div style="background:#FFF;border-radius:16px;border:1px solid {CB};padding:24px;'
            f'box-shadow:0 8px 30px rgba(0,0,0,.04);text-align:center;'
            f'display:flex;flex-direction:column;align-items:center;justify-content:center;">'
            f'<div style="font-size:42px;font-weight:800;color:{CT};letter-spacing:-1px;">{tot_likes:,}</div>'
            f'<div style="font-size:12px;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:.8px;margin-top:4px;">Total Likes on Dataset</div>'
            f'</div>'

            # Row B: Videos | Avg Likes/Video (side by side)
            f'<div style="display:flex;gap:16px;">'

            f'<div style="background:#FFF;border-radius:16px;border:1px solid {CB};padding:20px;'
            f'box-shadow:0 8px 30px rgba(0,0,0,.04);flex:1;text-align:center;'
            f'display:flex;flex-direction:column;align-items:center;justify-content:center;">'
            f'<div style="font-size:30px;font-weight:800;color:{CT};">{tot_vids}</div>'
            f'<div style="font-size:11px;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:.6px;margin-top:4px;">Videos</div>'
            f'</div>'

            f'<div style="background:#FFF;border-radius:16px;border:1px solid {CB};padding:20px;'
            f'box-shadow:0 8px 30px rgba(0,0,0,.04);flex:1;text-align:center;'
            f'display:flex;flex-direction:column;align-items:center;justify-content:center;">'
            f'<div style="font-size:30px;font-weight:800;color:{CT};">{avg_lk:,}</div>'
            f'<div style="font-size:11px;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:.6px;margin-top:4px;">Avg Likes / Video</div>'
            f'</div>'

            f'</div>'  # end row B

            # Row C: Total Comments (full-width)
            f'<div style="background:#FFF;border-radius:16px;border:1px solid {CB};padding:20px;'
            f'box-shadow:0 8px 30px rgba(0,0,0,.04);text-align:center;'
            f'display:flex;flex-direction:column;align-items:center;justify-content:center;">'
            f'<div style="font-size:30px;font-weight:800;color:{CT};">{tot_repl:,}</div>'
            f'<div style="font-size:11px;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:.6px;margin-top:4px;">Total Comments</div>'
            f'</div>'

            f'</div>'  # end right column
            f'</div>'  # end outer flex
        )
        st.markdown(profile_html, unsafe_allow_html=True)

        # ── Sample Comments ───────────────────────────────────────────────────
        if not inf_df.empty:
            st.markdown("#### Sample Comments")
            feedbacks = [r for _, r in inf_df.head(3).iterrows()]
            ccols = st.columns(min(len(feedbacks), 3))
            for j, row in enumerate(feedbacks):
                p = str(row.get('place', ''))
                d = str(row.get('createTimeISO', ''))
                s = str(row.get('sentiment', '')).upper()
                t = str(row.get('text', ''))
                v = str(row.get('videoWebUrl', '#'))
                c = CP if s == "POSITIVE" else CG if s == "NEGATIVE" else CN
                card = (
                    f'<div style="background:#FFF;border-radius:14px;padding:20px;margin-bottom:20px;'
                    f'box-shadow:0 4px 20px rgba(0,0,0,.04);border:1px solid {CB};border-left:6px solid {c};'
                    f'display:flex;flex-direction:column;min-height:250px;height:100%;">'
                    f'<div style="display:flex;justify-content:space-between;align-items:flex-start;'
                    f'margin-bottom:14px;flex-wrap:wrap;gap:8px;">'
                    f'<div style="font-size:11px;font-weight:800;color:{c};background:{c}15;'
                    f'padding:4px 10px;border-radius:20px;border:1px solid {c}30;letter-spacing:.5px;">{s}</div>'
                    f'<div style="font-size:12px;color:#64748b;font-weight:600;display:flex;flex-direction:column;'
                    f'align-items:flex-end;gap:3px;"><span>{p}</span><span>{d}</span></div></div>'
                    f'<div style="font-size:15px;color:{CT};margin-bottom:18px;line-height:1.5;'
                    f'font-weight:500;font-style:italic;flex-grow:1;">"{t}"</div>'
                    f'<div style="display:flex;justify-content:center;margin-top:auto;">'
                    f'<a href="{v}" target="_blank" style="font-size:13px;background:{CT};color:white;'
                    f'padding:10px 0;width:100%;text-align:center;border-radius:8px;text-decoration:none;'
                    f'font-weight:600;display:inline-flex;align-items:center;justify-content:center;'
                    f'gap:8px;box-shadow:0 4px 15px rgba(0,0,0,.15);">Watch Video</a>'
                    f'</div></div>'
                )
                with ccols[j]:
                    st.markdown(card, unsafe_allow_html=True)
