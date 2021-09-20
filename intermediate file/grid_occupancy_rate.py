# -*- coding: utf-8 -*-
# Copyright 2018-2019 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""An example of showing geographic data."""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

# LOADING DATA
DATE_TIME = "reporting_month"
DATA_URL = (
    './cleaned.csv'
)

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data

data = load_data(200)
'data', data

# CREATING FUNCTION FOR MAPS

def map(data, weight):
    layer = pdk.Layer(
    "ScreenGridLayer",
    df,
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
    get_position=['longitude','latitude'],
    get_weight=weight,
    )
    
    # Set the viewport location
    view_state = pdk.ViewState(latitude=41.9028, longitude= 12.4964, zoom=11, bearing=0, pitch=0)
    
    # Render
    r = pdk.Deck(layers=[layer], initial_view_state=view_state)
    st.write(r)


# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.beta_columns((2,3))

with row1_1:
    st.title("Rome AirDNA Data")
    month_selected = st.number_input("Select month:", 1, 12)

with row1_2:
    st.write(
    """
    ##
    Examining how AirBnb reservations in Rome changes.
    """)

# FILTERING DATA BY HOUR SELECTED
data = data[data[DATE_TIME].dt.month == month_selected]

# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row2_1, row2_2, row2_3, row2_4 = st.columns((2,1,1,1))


with row2_1:
    st.write("**All reservations in month %i" % (month_selected))
    field = 'occupancy_rate'
    df = data[~data[field].isna()]
    df = data[data[field]!=0]
    'df', df
    map(data, field)
