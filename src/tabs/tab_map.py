import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ==========================================
# MAP SETTINGS & COORDINATES
# ==========================================

# 1. EXACT OVERRIDES
# If you want to put a restaurant on its exact real-world street location,
# look up the coordinates on Google Maps and add them here.
EXACT_COORDINATES = {
    "Dusun Riffa Changlun": {"lat": 6.424054930383064, "lon": 100.47291850886107},
    "PotLepak Changlun": {"lat": 6.436173595802827, "lon": 100.42163062485562},
    "Cikjah Nasi Ayam Bakaq, Changlun": {"lat": 6.436961139990423, "lon":  100.44359789536735},
    "Dapoq Mak Kami, D' Dusun Papa, Bukit Wang, Jitra, Kedah": {"lat": 6.314010358529254, "lon":100.47696455521691},    
    "Nasi Lemak Kg Darat": {"lat": 6.446732304525118, "lon": 100.48223046837995},   
    "Dapoq Toksu Lijah": {"lat": 6.433723635130978, "lon": 100.43656731070902},   
    "Pahit Cafe": {"lat": 6.436757731448643, "lon": 100.44491657821057},
    "Santap Tokwan, Jalan Lama Sintok, Changlun, Kedah": {"lat": 6.438243833513633, "lon": 100.44691516653191},   
    "Kinkin, Changlun Kedah": {"lat": 6.447438330220291, "lon":  100.41552863954448},   
    "Cnw Jitra Manufacturing Area Iks Keda Napoh, Changlun, Kinkin, Changlun Kedah": {"lat": 6.363155250426487,"lon":   100.41949518372081}, 
    "Daud Grill Changlun": {"lat": 6.433503363703162, "lon": 100.43659720008556},  
    "Krua Rean Narm, Kampung Kubang Eriang, Jalan Pauh, 06010 Changlun, Kedah": {"lat": 6.4505228636105, "lon": 100.39616238372163},  
    "Lily Cafe": {"lat": 6.434610025316838, "lon":  100.43078643651597},  
    "Achik Steamboat & Shellout": {"lat": 6.275084895020331,"lon": 100.41974315506599},
    "Dekya Authentic Thai Jalan Changlun": {"lat": 6.4363159505549765, "lon": 100.41957314139228},
    "Rasa Rasa Vietnam Champa": {"lat": 6.434874663452185, "lon": 100.43769906653192},
    "The Beans Cafe, Jitra, Kedah": {"lat": 6.253164787642495, "lon": 100.42018055405006},
    "Warong D'Bonda, Sintok, Kedah": {"lat": 6.443648836893594, "lon": 100.47613342420281},
    "Restoran Pak Man": {"lat": 6.252597499936717, "lon": 100.42417143655106},
    "D'Aestate Cafe": {"lat": 6.435021224273659, "lon": 100.46358435590852},
    "Port Makan Bawah Titi Changlun": {"lat": 6.434260962057737, "lon": 100.42889878350277},
    "Lubuk Makan": {"lat": 6.43586883436354, "lon": 100.44097436653189},
    "Dekuki Cafe": {"lat": 6.443629603459455, "lon": 100.47818652892151},
    "Warung Che'Gu Ki": {"lat": 6.437649294915073, "lon": 100.44503185119032},
    "Bang Lie Nasi Ayam Lebuh Raya": {"lat": 6.32248452891879, "lon": 100.42051646653097},
    "Restoran Dua Rasa": {"lat": 6.434898714721676, "lon": 100.42735224464677},
    "Bagushi Steamboat & Grill Changlun": {"lat": 6.434035114863922, "lon": 100.43681859823764},
    "Zuma Apam Lambung": {"lat": 6.433020509538513, "lon": 100.43174363954437},
    "Restoran D'Warisan Changlun, Kedah": {"lat": 6.4000841992340645, "lon": 100.42687869721493},
    "Ayam Cili Kak Nab": {"lat": 6.448949017294722, "lon": 100.45867139536753},
    "Restoran Dekya Authentic Thai, Changlun": {"lat": 6.43639057903851, "lon":  100.41940148002573},
    "Kekanda Cafe": {"lat": 6.2043125468477, "lon": 100.41159753858513},
    "Grab & Bite Jitra, Kedah": {"lat": 6.238018961387211, "lon": 100.41909405589713},
    "Roti Canai Mak Tam": {"lat": 5.693156740387801, "lon": 100.47129643399468},
    "Md2 Botanic Cafe": {"lat": 6.428727906572304, "lon": 100.47416134241433},
    "Shamieda House Jitra, Kedah": {"lat": 6.243784328063803, "lon": 100.42043699536572},
    "Locamasta Cafe, Changlun, Kedah": {"lat": 6.43403154767675, "lon": 100.43689668187362},
    "Mak Anjang & Pak Anjang Tepung Talam, Jitra, Kedah": {"lat": 6.256111457575915, "lon": 100.419084037695},
    "Fariz Kridped, Changlun": {"lat": 6.41728966324673, "lon": 100.39390391070877},
    "Riposo Coffee, Caltex Jitra, Kedah": {"lat": 6.269061987325424, "lon": 100.41251796837838},
    "Ummi Kitchen Changlun": {"lat": 6.398426309731429, "lon": 100.42665405118998},
    "Le'Resto Changlun, Kedah": {"lat": 6.4286748272247225, "lon": 100.42909149823741},
    "Hillside Cafe Changlun": {"lat": 6.440890032566248, "lon": 100.45041053954442},
    "Kin Kin Changlun": {"lat": 6.447576922928944, "lon": 100.41547499536745},
    "D'Santai Ikan Bakar": {"lat": 6.429872836507913, "lon": 100.42853328002569},
    "Secret Flavor Bakery": {"lat": 6.413864042223499, "lon": 100.44276905303799},
    "Sup Kedah Nasi Ayam Tiga Rasa": {"lat": 6.4358939340625385, "lon": 100.43035220988374},
    "Warong Cafe, Tsp, Alor Setar": {"lat": 6.140466774073855, "lon": 100.35526063769399},
    "Celup Ranchak Taman Suria 2 Jitra": {"lat": 6.276869232433043, "lon": 100.4113330117222},
    "Sham Sup Tanah Merah Jitra": {"lat": 6.241491568113208, "lon": 100.42061435118866},
    "Phad Phed, Changlun, Kedah": {"lat": 6.441476976790481, "lon": 100.42861482235493},
    "Tasty Bites Jitra": {"lat": 6.2508626598292665, "lon": 100.42047889536579},
    "Cafe Uncle Man": {"lat": 6.25454284307131, "lon": 100.41934323769497},
    "Kopi Logika": {"lat": 6.261143279639096, "lon": 100.41931183954284},
    "Celapak Cafe": {"lat": 6.271869592300058, "lon": 6.271869592300058},
    "D'Kayangan Palace": {"lat": 6.2168697058688025, "lon": 100.41679659351762},
    "Ayra Cafe Medan Selera Kubang Pasu": {"lat": 6.276123478044077, "lon": 100.4202385205057},
    "Sup Trek Jitra": {"lat": 6.256527031229422, "lon": 100.42055182414539},
    "Sushi-Mo": {"lat": 6.253154263824069, "lon": 100.42928581255532},
    "Pak Man Cafe-Pasti": {"lat": 6.236513258062965, "lon": 100.42068951070726},
    "Nasi Lemak Panas Oh Tajul": {"lat": 6.285860558740045, "lon": 100.4201360395431},
    "Medan Selera Taman Sri Aman, Jitra": {"lat": 6.2541636233993945, "lon": 100.42694486653042},
    "Kafeteria By Lsh": {"lat": 6.273402750139136, "lon": 100.40875451070745},
    "Nenda Cafe": {"lat": 6.242841232834394, "lon": 100.42051698187184},
    "Sizzup Hm Delizioso Cafe": {"lat": 6.250899399601186, "lon": 100.42043195118869},
    "Rumah Lepak, Jitra": {"lat": 6.274823797578719, "lon": 100.40990468187226},
    "Thai Cafe House Aneka Jitra": {"lat": 6.261934114389062, "lon": 100.41851213954291},
    "Cool Licious Kafe": {"lat": 6.253659483617724, "lon": 100.42835147817628},
    "Mini Cafe, Jitra": {"lat": 6.269155740492361, "lon": 100.4232527953659},
}

# 2. GENERAL TOWN ZONES (Kubang Pasu / Kedah)
TOWN_COORDINATES = {
    "changlun": {"lat": 6.4385, "lon": 100.4300},
    "changloon": {"lat": 6.4385, "lon": 100.4300},
    "jitra": {"lat": 6.2692, "lon": 100.4183},
    "kodiang": {"lat": 6.3951, "lon": 100.3013},
    "bukit kayu hitam": {"lat": 6.5167, "lon": 100.4167},
    "sintok": {"lat": 6.4589, "lon": 100.5057},
    "alor setar": {"lat": 6.1248, "lon": 100.3678},
    "kepala batas": {"lat": 6.2081, "lon": 100.4072},
    "napoh": {"lat": 6.3575, "lon": 100.4186}
}

# 3. FALLBACK DEFAULT (General Central Kedah area)
DEFAULT_LAT = 6.2692  
DEFAULT_LON = 100.4183 

def get_coordinates(place_name):
    """Smart coordinate generator that matches town names to locations."""
    # Check exact overrides first
    if place_name in EXACT_COORDINATES:
        return EXACT_COORDINATES[place_name]
    
    place_lower = str(place_name).lower()
    
    # Check if a known town is mentioned in the restaurant name
    for town, coords in TOWN_COORDINATES.items():
        if town in place_lower:
            # We add a tiny bit of random math noise so pins in the same town don't stack directly on top of each other!
            np.random.seed(hash(place_name) % 4294967295) # Seed by name so it doesn't move when refreshed
            return {
                "lat": coords["lat"] + np.random.uniform(-0.02, 0.02), 
                "lon": coords["lon"] + np.random.uniform(-0.02, 0.02)
            }
            
    # Fallback to default area if no town is found
    np.random.seed(hash(place_name) % 4294967295)
    return {
        "lat": DEFAULT_LAT + np.random.uniform(-0.05, 0.05),
        "lon": DEFAULT_LON + np.random.uniform(-0.05, 0.05)
    }

from src.tabs.tab_initiatives import calculate_aspect_score, INFRA_KEYWORDS, calculate_sentiment_health_score, get_top_keywords

def render(df, selected_place):
    st.markdown("## 🗺️ Geographical Sentiment Analysis")
    st.markdown("Explore the spatial distribution of sentiment and infrastructure health across Kubang Pasu.")
    
    if df.empty:
        st.warning("⚠️ No data available to display on the map.")
        return



    # Prepare Map Data
    map_data = []
    places_to_show = [selected_place] if selected_place != "All Places" else df['place'].unique()
    
    for place in places_to_show:
        place_df = df[df['place'] == place]
        if place_df.empty: continue
            
        coords = get_coordinates(place)
        
        # Sentiment Metrics
        health = calculate_sentiment_health_score(place_df)
        infra = calculate_aspect_score(place_df, INFRA_KEYWORDS)
        
        # Determine Color Category based on Sentiment
        score_val = health
            
        if score_val >= 70.0:
            status = "Good (Positive)"
        elif score_val >= 50.0:
            status = "Okay (Neutral)"
        else:
            status = "Critical (Warning)"
            
        # Hover info
        pos_words = get_top_keywords(place_df, 'positive')
        pos_str = ', '.join(pos_words) if pos_words else "No data"
            
        map_data.append({
            "Place": place,
            "Latitude": coords["lat"],
            "Longitude": coords["lon"],
            "Status": status,
            "Score": f"{score_val:.1f}%",
            "ActualScore": score_val,
            "Total Reviews": len(place_df),
            "Top Praise": pos_str,
            "Infra Score": f"{infra:.1f}%" if infra is not None else "N/A"
        })
        
    map_df = pd.DataFrame(map_data)
    
    if map_df.empty:
        st.info("No spatial data generated.")
        return

    st.markdown("---")
    
    import folium
    from streamlit_folium import st_folium
    
    folium_color_map = {
        "Good (Positive)": "green",
        "Okay (Neutral)": "orange",
        "Critical (Warning)": "red"
    }
    
    tile_style = "OpenStreetMap"

    # Determine center of the map
    if selected_place == "All Places":
        center_lat = map_df["Latitude"].mean()
        center_lon = map_df["Longitude"].mean()
        zoom_level = 10
    else:
        center_lat = map_df["Latitude"].iloc[0]
        center_lon = map_df["Longitude"].iloc[0]
        zoom_level = 15

    # Create Folium Map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_level, tiles=tile_style)

    for i, row in map_df.iterrows():
        status_color = folium_color_map.get(row["Status"], "blue")
        
        # We need to extract the video URL from df for this place that matches a top praise
        place_df_original = df[df['place'] == row['Place']]
        
        video_link_html = ""
        top_praise_str = str(row["Top Praise"])
        
        # Google Maps Search Link
        import urllib.parse
        encoded_place = urllib.parse.quote(row["Place"] + " Kedah")
        gmaps_url = f"https://www.google.com/maps/search/?api=1&query={encoded_place}"
        gmaps_link_html = f"""
        <div style="margin-top: 10px; background: #4285F4; padding: 8px; border-radius: 6px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <a href="{gmaps_url}" target="_blank" rel="noopener noreferrer" style="font-size: 13px; font-weight: bold; color: #fff; text-decoration: none; display: block;">
                📍 View on Google Maps
            </a>
        </div>
        """

        # Find ANY review with a valid tiktok link
        if 'videoWebUrl' in place_df_original.columns:
            valid_videos = place_df_original[
                place_df_original['videoWebUrl'].notna() &
                (place_df_original['videoWebUrl'].astype(str) != '')
            ]
            if not valid_videos.empty:
                video_url = valid_videos.iloc[0]['videoWebUrl']
                video_link_html = f"""
                <div style="margin-top: 8px; background: #000; padding: 8px; border-radius: 6px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <a href="{video_url}" target="_blank" rel="noopener noreferrer" style="font-size: 13px; font-weight: bold; color: #fff; text-decoration: none; display: block;">
                        <span style="color: #fe2c55;">🎵</span> Watch a TikTok Review
                    </a>
                </div>
                """
        
        popup_html = f'''
        <div style="font-family: Arial, sans-serif; min-width: 240px; padding: 5px;">
            <h4 style="margin-top: 0; margin-bottom: 10px; color: #0f172a; font-size: 17px; font-weight: 900; letter-spacing: 0.5px;">{row["Place"]}</h4>
            <div style="margin-bottom: 5px; font-size: 13px;"><b>Status:</b> <span style="color: {status_color}; font-weight: bold;">{row["Status"]}</span></div>
            <div style="margin-bottom: 5px; font-size: 13px;"><b>Score:</b> {row["Score"]}</div>
            <div style="margin-bottom: 5px; font-size: 13px;"><b>Infra Score:</b> {row["Infra Score"]}</div>
            <div style="margin-bottom: 5px; font-size: 13px;"><b>Reviews:</b> {row["Total Reviews"]}</div>
            <div style="margin-top: 8px; font-size: 12px; color: #666; background: #f9f9f9; padding: 6px; border-radius: 4px;"><b>Top Praise:</b><br>{top_praise_str}</div>
            <div style="display: flex; flex-direction: column; gap: 2px;">
                {gmaps_link_html}
                {video_link_html}
            </div>
        </div>
        '''
        
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{row['Place']} - {row['Status']}",
            icon=folium.Icon(color=status_color, icon="info-sign")
        ).add_to(m)

    # Render it!
    st_folium(m, height=680, use_container_width=True, returned_objects=[])
    

    
    # Additional Context Box
    if selected_place == "All Places":
        st.info("💡 **Tip:** The map pins are placed automatically based on the town name mentioned in the restaurant. You can manually adjust any pin's exact street location in `tab_map.py`.")
