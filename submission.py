import streamlit as st
import pandas as pd
import pydeck as pdk
from sklearn.utils import shuffle
import urllib

COLOR_BREWER_BLUE_SCALE = [
    [240, 249, 232],
    [204, 235, 197],
    [168, 221, 181],
    [123, 204, 196],
    [67, 162, 202],
    [8, 104, 172],
]

COLOR_BREWER_RED_SCALE = [
    [244, 194, 194],
    [255, 105, 97],
    [255, 8, 0],
    [206, 32, 32],
    [164, 0, 0],
    [112, 28, 28],
]

st.write('# What kind of properties in Rome can earn you more money as a AirBnb host?')
st.write('#### AirDNA data for Rome')

month_map = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 
             'May': 5, 'June': 6, 'July': 7, 'August': 8, 
             'September': 9, 'October': 10, 'November': 11, 'December': 12}

year_selected = st.sidebar.selectbox('Year?', (2015, 2016, 2017, 2018, 2019))
# st.write('Year selected:', year_selected)
month_selected = st.sidebar.selectbox('Month?', ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'))
room_selected = st.sidebar.selectbox('Number of Bedrooms?', ('0.0', '1.0', '2.0', '3.0', '4.0', '>=5.0'),index=1)

@st.cache(persist=True)
def load_data():
    data = pd.read_csv('cleaned.csv')
    data = data[data['Available_Days']!=0]
    data['Reporting_Month'] = pd.to_datetime(data['Reporting_Month'])
    data['Profitability'] = data['Revenue_USD'] / (data['Available_Days'])
    data['Profitability'] = data['Profitability'].round(0)
    data = data.fillna(value=0)
    return data

def filter_rooms(room_selected):
    if room_selected in ['0.0', '1.0', '2.0', '3.0', '4.0']:
        return (test['Bedrooms'] == float(room_selected))
    else:
        return (test['Bedrooms'] >= 5.0)

test = load_data()
test = test[(test['Reporting_Month'].dt.month == month_map[month_selected]) & (test['Reporting_Month'].dt.year == year_selected) & filter_rooms(room_selected)]

# "Filtered AirDNA Data", test


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
        "Occupancy Rate-Screen Grid": pdk.Layer(
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
            get_weight="Occupancy_Rate",
        ),
        "RevPAP-Barchart": pdk.Layer(
            "HexagonLayer",
            data=test[['Longitude', 'Latitude', 'Profitability']],
            get_position=['Longitude', 'Latitude'],
            radius=10,
            elevation_scale=4,
            elevation_range=[0, 1000],
            extruded=True,
        ),
        "Property-Scatter Plot": pdk.Layer(
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
            get_line_color=[255, 105, 97],
        ),
        "ADR-Heatmap": pdk.Layer(
            "HeatmapLayer",
            data=test[['Longitude', 'Latitude', 'ADR_USD']],
            opacity=0.9,
            get_position=["Longitude", "Latitude"],
            aggregation=pdk.types.String("MEAN"),
            color_range=COLOR_BREWER_BLUE_SCALE,
            get_weight="ADR_USD",
            threshold=1,
            pickable=True,
        ),
        "Monthly Revenue-Screen Grid": pdk.Layer(
            "ScreenGridLayer",
            data=test[['Longitude', 'Latitude', 'Revenue_USD']],
            pickable=False,
            opacity=0.8,
            cell_size_pixels=20,
            color_range=[
            [0, 25, 25, 25],
            [0, 85, 85, 85],
            [0, 127, 127, 127],
            [0, 170, 170, 170],
            [0, 190, 190, 190],
            [0, 255, 255, 255],
            ],
            get_position=['Longitude','Latitude'],
            get_weight="Revenue_USD",
        ),
        "Show Tourist Attractions" : pdk.Layer(
            type="IconLayer",
            data=site,
            get_icon="icon_data",
            get_size=3,
            size_scale=10,
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
                                "longitude": 12.5, "zoom": 11, "pitch": 20},
            layers=selected_layers,
            tooltip={"text": "{Name}"}
        ))
    else:
        st.error("Please choose at least one layer above.")
except urllib.error.URLError as e:
    st.error("""
        **This demo requires internet access.**

        Connection error: %s
    """ % e.reason)
