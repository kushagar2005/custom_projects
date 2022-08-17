#Importing Python Libraries
import requests 
import json 
import pandas as pd
import folium 
import os
from folium.plugins import MarkerCluster, Search
from folium import FeatureGroup, LayerControl, Map, Marker
from folium.plugins import Search

#Varible Definition for using custom API to get the Data values based on Parameter and Qualifier.
level_api = 'parameter=level'
flow_api = 'parameter=flow'
temperature_api = 'parameter=temperature'

stage_api = 'qualifier=Stage'
downstream_stage_api = 'qualifier=Downstream+Stage'
groundwater_api = 'qualifier=Groundwater'
tidal_level_api = 'qualifier=Tidal+Level'


def api_definition(api_parameter):
    """ 
    API request to get the data for all the measuring station with the mentioned qualifier or parameter.
    The function is used to access data and store it in specific pandas datafarme.
    Parameter - 
    api_parameter : string
    
    Returns -
    df - Pandas dataframe object
    pnadas python Dataframe"""

    response_api = requests.get('https://environment.data.gov.uk/flood-monitoring/id/stations?' + api_parameter)
    json = response_api.json()
    df = pd.DataFrame(json['items'])
    df = df[['lat', 'long', 'notation']]
    df = df.dropna(subset=['lat'])
    
    return df


#Api request to Get the deatils about all the measuring stations.
print('Loading All Measurement Station Data')
response_api = requests.get('http://environment.data.gov.uk/flood-monitoring/id/stations')
json = response_api.json()

#Data conversion from json format to pandas dataframe for further usage in python.
df = pd.DataFrame(json['items']) #Main dataframe contain all measuring stations details 

print('Fetching Data based on Qualifiers and Parameters')
df_parameter_level = api_definition(level_api) #Dataframe of Measuring stations with Level measurement
df_parameter_flow = api_definition(flow_api) #Dataframe of Measuring stations with Flow measurement
df_parameter_temperature = api_definition(temperature_api) #Dataframe of Measuring stations with Temperature measurement

#Dataframe consisiting with data of measurement stations based on various Qualifier
df_qualifier_stage = api_definition(stage_api) #Qualifier: Stage
df_qualifier_downstream_stage = api_definition(downstream_stage_api) #Qualifier: Downstream
df_qualifier_groundwater = api_definition(groundwater_api) #Qualifier: Groundwater
df_qualifier_tidal_level = api_definition(tidal_level_api) #Qualifier: Tidal level

#Removal of unwanted columns from pandas dataframe
df = df.drop(columns=[
                 '@id',
                 'dateOpened', 
                 'easting', 
                 'measures', 
                 'northing',
                 'stageScale',  
                 'stationReference',
                 'wiskiID',
                 'datumOffset',
                 'gridReference',
                 'downstageScale'])

#String manipulation to remove the hyper link from the Status column of main dataframe.
df['status'] = df['status'].str.replace('http://environment.data.gov.uk/flood-monitoring/def/core/', '', regex=False)
df = df.dropna(subset=['lat']) #Removal of measuring stations from dataframe whose latitude and longitude are not available.

#Map tool creation 
#Map tool 1
#mapobj displays all the measuring stations.
#Latitude, Longitude - [51.509865, -0.118092] # start the map with taking UK central location GPS coordinates.
mapobj = folium.Map([51.509865, -0.118092], zoom_start=6)
print('Generating Map Tool - All Stations')
# Add interactivity to display multiple map tiles
folium.TileLayer('stamentoner').add_to(mapobj)
folium.TileLayer('stamenwatercolor').add_to(mapobj)
folium.TileLayer('cartodbpositron').add_to(mapobj)
folium.TileLayer('openstreetmap').add_to(mapobj)

# color coding to show different colors for diffrent types of Status of measuring stations
def marker_color(STATUS):
        if STATUS=='statusActive':
                  return 'green' #Green is active
        elif STATUS=='statusClosed'  :
            return 'red' #Red if closed
        elif STATUS == 'statusukcmf':
            return 'blue' #Blue if status = statusukcmf
        elif STATUS == 'statusSuspended':
            return 'orange' #Orange is suspended
        else:
            return 'gray' #Gray if status value is nan
        

mCluster = MarkerCluster(name="ALL Measuring Stations").add_to(mapobj) #Clustering of measuring station markers to view map tool neatly.

#Adding each measuring station on the map using markers.
#Popup - shows information about the Measuring station when clicked on the specific marker
         #Label, Notation, Latitude, Longitude, Status
#Tooltip - Show the Label and notation of the specific measuring station when hover the cursor over the marker.
for i in range(len(df)):
    Popup="Label:"+str(df.iloc[i]['label'])+"\n"+"Notation:"+str(df.iloc[i]['notation'])+"\n"+"Latitude:"+str(df.iloc[i]['lat'])+"\n"+"Longitude:"+str(df.iloc[i]['long'])+"\n"+"Status:"+str(df.iloc[i]['status'])
    Tooltip=str(df.iloc[i]['label'])+","+"Notation:"+str(df.iloc[i]['notation'])
    ic=marker_color(df.iloc[i]['status'])
    folium.Marker(location=[df.iloc[i]['lat'], df.iloc[i]['long']], popup=Popup, tooltip=Tooltip, icon=folium.Icon(color=ic,icon_color='#FFFF00',icon='sensor')).add_to(mCluster)
    
folium.LayerControl().add_to(mapobj)

mapobj.save("map_all_station.html") # Save the map tool as html file. 

#Map Tool 2
#It Provides facility of checkboxes to dispay the measuring stations according to the different Qualifier and Parameter values.
#Latitude, Longitude - [51.509865, -0.118092] # start the map with taking UK central location GPS coordinates.
m = folium.Map(location=[51.509865, -0.118092],zoom_start=6)
print('Generating Map Tool - Interactive Control Measurement Stations')
mcg = folium.plugins.MarkerCluster(control=False)
m.add_child(mcg)
#Map Layer definition based on Parameter.
g1 = folium.plugins.FeatureGroupSubGroup(mcg, 'Level Measuring Stations')
m.add_child(g1)

g2 = folium.plugins.FeatureGroupSubGroup(mcg, 'Flow Measuring Stations')
m.add_child(g2)

g3 = folium.plugins.FeatureGroupSubGroup(mcg, 'Temperature Measuring Stations')
m.add_child(g3)

#Map Layer definition based on Qualifier.
g4 = folium.plugins.FeatureGroupSubGroup(mcg, 'Stage Qualifier')
m.add_child(g4)

g5 = folium.plugins.FeatureGroupSubGroup(mcg, 'Downstream Stage Qualifier')
m.add_child(g5)

g6 = folium.plugins.FeatureGroupSubGroup(mcg, 'Groundwater Qualifier')
m.add_child(g6)

g7 = folium.plugins.FeatureGroupSubGroup(mcg, 'Tidal Level Qualifier')
m.add_child(g7)


#Addition of map Layers to the map object
for i in range(len(df_parameter_level)):
    folium.Marker(location=[df_parameter_level.iloc[i]['lat'], df_parameter_level.iloc[i]['long']], tooltip=str(df_parameter_level.iloc[i]['notation']), icon=folium.Icon(color='red',icon='sensor')).add_to(g1)
    
for i in range(len(df_parameter_flow)):
    folium.Marker(location=[df_parameter_flow.iloc[i]['lat'], df_parameter_flow.iloc[i]['long']], tooltip=str(df_parameter_flow.iloc[i]['notation']), icon=folium.Icon(color='red',icon='sensor')).add_to(g2)
    
for i in range(len(df_parameter_temperature)):
    folium.Marker(location=[df_parameter_temperature.iloc[i]['lat'], df_parameter_temperature.iloc[i]['long']], tooltip=str(df_parameter_temperature.iloc[i]['notation']), icon=folium.Icon(color='red',icon='sensor')).add_to(g3)

for i in range(len(df_qualifier_stage)):
    folium.Marker(location=[df_qualifier_stage.iloc[i]['lat'], df_qualifier_stage.iloc[i]['long']], tooltip=str(df_qualifier_stage.iloc[i]['notation']), icon=folium.Icon(color='green',icon='sensor')).add_to(g4)

for i in range(len(df_qualifier_downstream_stage)):
    folium.Marker(location=[df_qualifier_downstream_stage.iloc[i]['lat'], df_qualifier_downstream_stage.iloc[i]['long']], tooltip=str(df_qualifier_downstream_stage.iloc[i]['notation']), icon=folium.Icon(color='green',icon='sensor')).add_to(g5)

for i in range(len(df_qualifier_groundwater)):
    folium.Marker(location=[df_qualifier_groundwater.iloc[i]['lat'], df_qualifier_groundwater.iloc[i]['long']], tooltip=str(df_qualifier_groundwater.iloc[i]['notation']), icon=folium.Icon(color='green',icon='sensor')).add_to(g6)

for i in range(len(df_qualifier_tidal_level)):
    folium.Marker(location=[df_qualifier_tidal_level.iloc[i]['lat'], df_qualifier_tidal_level.iloc[i]['long']], tooltip=str(df_qualifier_tidal_level.iloc[i]['notation']), icon=folium.Icon(color='green',icon='sensor')).add_to(g7)

folium.LayerControl().add_to(m)

m.save("map_interactive.html") # Save the map tool as html file.