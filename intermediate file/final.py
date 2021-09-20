import streamlit as st
import pandas as pd
import pydeck as pdk
from sklearn.utils import shuffle
import urllib

year_selected = st.number_input("Select year of overview", 2015, 2019)
month_selected = st.number_input("Select month of overview", 1, 12)
COLOR_BREWER_RED_SCALE = [
    [244, 194, 194],
    [255, 28, 0],
    [204, 0, 0],
    [128, 0, 0],
]
@st.cache(persist=True)
def load_data():
    data = pd.read_csv('cleaned.csv')
    data['Reporting_Month'] = pd.to_datetime(data['Reporting_Month'])
    data['price'] = data['Revenue_USD'] / (data['Occupancy_Rate'] * 30)
    data['price'] = data['price'].round(0)
    data = data.fillna(value=0)
    return data

test = load_data()
test = test[(test['Reporting_Month'].dt.month == month_selected) & (test['Reporting_Month'].dt.year == year_selected)]
"test_data", test


# Data from OpenStreetMap, accessed via osmpy
SITE_URL = "./datasets/italy/rome/tourist_site_rome.csv"

site = pd.read_csv(SITE_URL)
site["icon_data"] = None
for i in site.index:
    site["icon_data"][i] = {
    # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
    # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
    "url": site['Icon_Path'][i],
    "width": 550,
    "height": 550,
    "anchorY": 550,
}
    


try:
    ALL_LAYERS = {
        "price": pdk.Layer(
            "HexagonLayer",
            data=test[['Longitude', 'Latitude', 'price']],
            get_position=['Longitude', 'Latitude'],
            radius=100,
            elevation_scale=2,
            elevation_range=[0, 2000],
            extruded=True,
        ),
        "Property":pdk.Layer(
            "ScatterplotLayer",
            data=test[['Longitude', 'Latitude', 'Property_ID']],
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=6,
            radius_min_pixels=1,
            radius_max_pixels=100,
            line_width_min_pixels=1,
            get_position=['Longitude', 'Latitude'],
            get_radius="exits_radius",
            get_fill_color=[255, 140, 0],
            get_line_color=[255,105,97],
        ),
        "occupancy" : pdk.Layer(
            "ScreenGridLayer",
            data=test[['Longitude', 'Latitude', 'Occupancy_Rate']],
            pickable=False,
            opacity=0.8,
            cell_size_pixels=20,
            color_range=[
                [0, 25, 0, 25],
                [0, 85, 0, 85],
                [0, 127, 0, 127],
                [0, 170, 0, 170],
                [0, 190, 0, 190],
                [0, 255, 0, 255],
            ],
            get_position=['Longitude','Latitude'],
            get_weight='Occupancy_Rate',
        ),
        "Heat Map": pdk.Layer(
            "HeatmapLayer",
            data=test[['Longitude', 'Latitude', 'ADR_USD']],
            opacity=0.9,
            get_position=["Longitude", "Latitude"],
            aggregation=pdk.types.String("MEAN"),
            color_range=COLOR_BREWER_RED_SCALE,
            threshold=1,
            get_weight="ADR_USD",
            pickable=True,
        ),
        "icon" : pdk.Layer(
            type="IconLayer",
            data=site,
            get_icon="icon_data",
            get_size=4,
            size_scale=15,
            get_position=["Longitude", "Latitude"],
            pickable=True,
        ),
    }
    st.sidebar.markdown('### Map Layers')
    selected_layers = [
        layer for layer_name, layer in ALL_LAYERS.items()
        if st.sidebar.checkbox(layer_name, True)]
    if selected_layers:
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={"latitude": 41.9,
                                "longitude": 12.5, "zoom": 11,"pitch": 20},
            layers=selected_layers,
        ))
    else:
        st.error("Please choose at least one layer above.")
except urllib.error.URLError as e:
    st.error("""
        **This demo requires internet access.**

        Connection error: %s
    """ % e.reason)