from PIL import Image
import pydeck as pdk
from folium.plugins import HeatMapWithTime
from branca.element import Figure
from folium.plugins import TimestampedGeoJson
import folium
import seaborn as sns
import pandas as pd
from pathlib import Path
import pandas as pd  # library for data analysis
import numpy as np
import json  # library to handle JSON files
from geopy.geocoders import Nominatim
# convert an address into latitude and longitude values
import requests  # library to handle requests

import streamlit as st  # creating an app
from streamlit_folium import folium_static
from shapely import wkt
import geopandas as gpd
import plotly.express as px


file = "final_mrged"
image = Image.open('coe1.png')
st.image(image, width=180)

st.write("""
# Crime Data Analysis Of Odisha
""")


@st.cache(suppress_st_warning=True)
def get_data(file):
    data = pd.read_csv(file)
    data.drop(['Unnamed: 0'], axis=1, inplace=True)
    return data


data_sll = get_data(file)

# df = st.cache(pd.read_csv)("Sll_final")
# df.drop(['Unnamed: 0'], axis=1, inplace=True)
is_check = st.checkbox("Display Whole Data")
st.write(" ")
st.write("👈 Select District & Type of Crime ")
st.write(" ")
if is_check:
    st.write(data_sll)
district_sll = st.sidebar.multiselect(
    "Enter district name", data_sll['District'].unique())
# st.write("Your input Districts", district)
variables_sll = st.sidebar.multiselect(
    "Enter the type of crimes", data_sll.columns)
# st.write("You selected these variables", variables)

baar_on = st.sidebar.multiselect(
    "Input For Bar Graph", data_sll.columns)

selected_district_data = data_sll[(data_sll['District'].isin(district_sll))]
two_clubs_data = selected_district_data[variables_sll]
club_data_is_check = st.checkbox("Display the data of selected districts")
if club_data_is_check:
    st.write(two_clubs_data)

bar_data = selected_district_data[baar_on]

if st.sidebar.checkbox("Show Analysis by State", True, key=2):
    st.markdown("## **District Level Analysis**")
    # st.markdown("#### Overall Confirmed, Active, Recovered and " +
    # "Deceased cases in %s yet" % (district_sll))
    st.write("👇 Uncheck For Bar Graph ")
    if not st.checkbox('Hide Graph', True, key=1):
        state_total_graph = px.bar(
            bar_data,
            x='District',
            y=baar_on,
            labels={'Number of cases': 'Number of cases in %s' % (
                district_sll)},
            color='District')
        st.plotly_chart(state_total_graph)


data = pd.read_csv('work')
data.drop(columns=['Unnamed: 0'], inplace=True)
data['geometry'] = data['geometry'].apply(wkt.loads)
my_geo_df = gpd.GeoDataFrame(data, geometry='geometry', crs='epsg:4326')


mymap = folium.Map(location=[20.509834585478302,
                             84.60220092022696], zoom_start=7)
folium.TileLayer('CartoDB positron', name="Light Map",
                 control=False).add_to(mymap)

mymap.choropleth(
    geo_data=my_geo_df,
    name='choropleth',
    data=my_geo_df,
    columns=['Id', 'Total Cognizable SLL crimes'],
    key_on='feature.properties.Id',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Total Cognizable SLL crimes'
)
folium.LayerControl().add_to(mymap)
st.markdown("## **Map of Odisha for SLL Crimes**")
if st.checkbox("Static Heat Map", False, key=3):
    folium_static(mymap)

# design for the app
#st.title('Map of Surabaya')


def style_function(x): return {'fillColor': '#ffffff',
                               'color': '#000000',
                               'fillOpacity': 0.1,
                               'weight': 0.1}


def highlight_function(x): return {'fillColor': '#000000',
                                   'color': '#000000',
                                   'fillOpacity': 0.50,
                                   'weight': 0.1}


NIL = folium.features.GeoJson(
    my_geo_df,
    style_function=style_function,
    control=False,
    highlight_function=highlight_function,
    tooltip=folium.features.GeoJsonTooltip(
        fields=['District', 'Total Cognizable SLL crimes'],
        aliases=['District Name: ', 'Total SLL Crimes : '],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
    )
)
mymap.add_child(NIL)
mymap.keep_in_front(NIL)
folium.LayerControl().add_to(mymap)


if st.checkbox("Interactive Heat Map", False, key=4):
    folium_static(mymap)


data_ipc = pd.read_csv('ipc')
data_ipc.rename(columns={'Unnamed: 0': 'Id'}, inplace=True)
# data.drop(columns=['Unnamed: 0'], inplace=True)
data_ipc['geometry'] = data_ipc['geometry'].apply(wkt.loads)
my_geo_df_ipc = gpd.GeoDataFrame(
    data_ipc, geometry='geometry', crs='epsg:4326')
add_select_ipc = st.sidebar.selectbox(
    "What data do you want to see in Ipc?", ("OpenStreetMap", "Stamen Terrain", "Stamen Toner"))
mymap_ipc = folium.Map(location=[20.509834585478302,
                                 84.60220092022696], zoom_start=7, tiles=add_select_ipc)
folium.TileLayer('CartoDB positron', name="Light Map",
                 control=False).add_to(mymap_ipc)

mymap_ipc.choropleth(
    geo_data=my_geo_df_ipc,
    name='choropleth',
    data=my_geo_df_ipc,
    columns=['Id', 'Total Cognizable IPC crimes'],
    key_on='feature.properties.Id',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Total Cognizable IPC crimes'
)
folium.LayerControl().add_to(mymap_ipc)
#
# folium_static(mymap_ipc)

# st.title('Map of Surabaya')
st.markdown("## **Map of Odisha for IPC Crimes**")
if st.checkbox("Static Heat Map", False, key=5):
    folium_static(mymap_ipc)


def style_function(x): return {'fillColor': '#ffffff',
                               'color': '#000000',
                               'fillOpacity': 0.1,
                               'weight': 0.1}


def highlight_function(x): return {'fillColor': '#000000',
                                   'color': '#000000',
                                   'fillOpacity': 0.50,
                                   'weight': 0.1}


NIL = folium.features.GeoJson(
    my_geo_df_ipc,
    style_function=style_function,
    control=False,
    highlight_function=highlight_function,
    tooltip=folium.features.GeoJsonTooltip(
        fields=['District', 'Total Cognizable IPC crimes'],
        aliases=['District Name: ', 'Total IPC Crimes : '],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
    )
)
mymap_ipc.add_child(NIL)
mymap_ipc.keep_in_front(NIL)
folium.LayerControl().add_to(mymap_ipc)
# folium_static(mymap_ipc)
if st.checkbox("Interactive Heat Map", False, key=6):
    folium_static(mymap_ipc)


data1 = pd.read_csv('new')
data1.drop(columns=['Unnamed: 0', 'People_Affected',
           'People__Affected'], inplace=True)
data1['DateTime'] = pd.to_datetime(data1['DateTime'])
data1['hour'] = data1['DateTime'].apply(lambda x: x.hour+1)


lat_long_list = []
for i in range(1, 25):
    temp = []
    for index, instance in data1[data1['hour'] == i].iterrows():
        temp.append([instance['Latitude'], instance['Longitude']])
    lat_long_list.append(temp)
fig7 = Figure(width=800, height=400)
m7 = folium.Map(location=[20.44, 85.8327], zoom_start=10)
fig7.add_child(m7)
HeatMapWithTime(lat_long_list, radius=6.5, auto_play=True,
                position='bottomright').add_to(m7)
# folium_static(m7)
st.markdown("## **Map of Bhubaneswar Crime Analysis**")
st.write("Animation Of Heatmap Showing Crime Location In Bhubaneswar On Hourly Basis")
folium_static(m7)

# Define a layer to display on a map

locs_map = folium.Map(location=[20.290838, 85.845339],
                      zoom_start=13, tiles="OpenStreetMap")

feature_th = folium.FeatureGroup(name='Theft')
feature_gh = folium.FeatureGroup(name='Grievous Hurt')
feature_rob = folium.FeatureGroup(name='Robbery')
feature_cbt = folium.FeatureGroup(name='Criminal Breach of Trust')
feature_assault = folium.FeatureGroup(name='Assault')
feature_ua = folium.FeatureGroup(name='Unlawful Assembly')
feature_ex = folium.FeatureGroup(name='Extortion')

for i, v in data1.iterrows():
    popup = """
    case_list : <b>%s</b><br>
    PeopleAffected : <b>%d</b><br>
    """ % (v['case_list'],  v['PeopleAffected'])

    if v['case_list'] == 'Theft':
        folium.CircleMarker(location=[v['Latitude'], v['Longitude']],
                            radius=4,
                            tooltip=popup,
                            color='#FFFF00',
                            fill_color='#FFBA00',
                            fill=True).add_to(feature_th)
    elif v['case_list'] == 'Grievous Hurt':
        folium.CircleMarker(location=[v['Latitude'], v['Longitude']],
                            radius=4,
                            tooltip=popup,
                            color='#087FBF',
                            fill_color='#087FBF',
                            fill=True).add_to(feature_gh)
    elif v['case_list'] == 'Robbery':
        folium.CircleMarker(location=[v['Latitude'], v['Longitude']],
                            radius=4,
                            tooltip=popup,
                            color='#FF0700',
                            fill_color='#FF0700',
                            fill=True).add_to(feature_rob)
    elif v['case_list'] == 'Criminal Breach of Trust':
        folium.CircleMarker(location=[v['Latitude'], v['Longitude']],
                            radius=4,
                            tooltip=popup,
                            color='#00FF00',
                            fill_color='#FF0700',
                            fill=True).add_to(feature_cbt)
    elif v['case_list'] == 'Assault':
        folium.CircleMarker(location=[v['Latitude'], v['Longitude']],
                            radius=4,
                            tooltip=popup,
                            color='#9900FF',
                            fill_color='#FF0700',
                            fill=True).add_to(feature_assault)
    elif v['case_list'] == 'Unlawful Assembly':
        folium.CircleMarker(location=[v['Latitude'], v['Longitude']],
                            radius=4,
                            tooltip=popup,
                            color='#FF6600',
                            fill_color='#FF0700',
                            fill=True).add_to(feature_ua)
    elif v['case_list'] == 'Extortion':
        folium.CircleMarker(location=[v['Latitude'], v['Longitude']],
                            radius=4,
                            tooltip=popup,
                            color='#993300',
                            fill_color='#FF0700',
                            fill=True).add_to(feature_ex)


feature_th.add_to(locs_map)
feature_gh.add_to(locs_map)
feature_rob.add_to(locs_map)
feature_cbt.add_to(locs_map)
feature_assault.add_to(locs_map)
feature_ua.add_to(locs_map)
feature_ex.add_to(locs_map)
folium.LayerControl(collapsed=False).add_to(locs_map)

st.markdown("## **Geo Location Of Crimes In Bhubaneswar **")
folium_static(locs_map)
