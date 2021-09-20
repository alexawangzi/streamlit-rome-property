"""
IconLayer
=========

Location of biergartens in Germany listed on OpenStreetMap as of early 2020.
"""

import pydeck as pdk
import pandas as pd
import streamlit as st

# Data from OpenStreetMap, accessed via osmpy
SITE_URL = "./datasets/italy/rome/tourist_site_rome.csv"

site = pd.read_csv(SITE_URL)
site["icon_data"] = None

'site', site

for i in site.index:
    site["icon_data"][i] = {
    # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
    # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
    "url": site['Icon_Path'][i],
    "width": 550,
    "height": 550,
    "anchorY": 550,
}
    
'site', site

view_state = pdk.data_utils.compute_view(site[["Longitude", "Latitude"]], 0.1)

icon_layer = pdk.Layer(
    type="IconLayer",
    data=site,
    get_icon="icon_data",
    get_size=4,
    size_scale=15,
    get_position=["Longitude", "Latitude"],
    pickable=True,
)

r = pdk.Deck(layers=[icon_layer], initial_view_state=view_state, tooltip={"text": "{Name}"})
st.write(r)