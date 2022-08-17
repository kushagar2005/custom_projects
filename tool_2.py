"""
This script loads all the reading data for the specific measurement station and plots it in Graphical and Tabular form
"""
#Importing Python Libraries
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import plotly
import sys
import requests 
import json 
import pandas as pd

#var1 - User Input 1 : Notation of the measurement station for which the reading is needed.
#var2 - user Input 2 : Date in YYYY-MM-DD format. Enter the date for which the reading of the mentioned measurement station notation should be loaded. 
var1 = str(sys.argv[1])
var2 = str(sys.argv[2])

print('Fetching data from API')
#API to get all the reading for a particular measurement staion 
string = 'https://environment.data.gov.uk/flood-monitoring/id/stations/' + var1 + '/readings?date=' + var2
response_api = requests.get(string)
json = response_api.json()

#Conversion of json to pandas dataframe for further usage of data
df = pd.DataFrame(json['items'])
df = df.drop(columns=['@id'])# Removal of unwanted column.
df['measure'] = df['measure'].str.replace('http://environment.data.gov.uk/flood-monitoring/id/measures/', '', regex=False)#Removal of Hyperlink and only string the type of measurement.

#Seperation of data based on the type of readings of the mentioned(var1) measurement station.
df_tidal_level = df.loc[df['measure'].str.contains("tidal_level", case=False)] #Data for the Tidal readings
df_stage_level = df.loc[df['measure'].str.contains("level-stage", case=False)] #Data for the Stage readings
df_downstage_level = df.loc[df['measure'].str.contains("level-downstage", case=False)] #Data for the Downstage reading
df_groundwater_level = df.loc[df['measure'].str.contains("level-groundwater", case=False)] #Data for Groundwater reading

for i in range(1,6): #For loop is used as the Qualifier parameter conatains integer values from 1-5 other than the above mentioned values
    string = str(var1+'-level-'+str(i))
    df_water_level = df.loc[df['measure'].str.contains(string, case=False)] #Data for water level reading.
    if not df_water_level.empty:
        break

#Data manipulation to change the values in the in df['measure'] column
df_tidal_level = df.loc[df['measure'].str.contains("tidal_level", case=False)]
df_tidal_level['measure'] = 'Tidal-level'
df_stage_level = df.loc[df['measure'].str.contains("level-stage", case=False)]
df_stage_level['measure'] = 'Stage-level'
df_downstage_level = df.loc[df['measure'].str.contains("level-downstage", case=False)]
df_downstage_level['measure'] = 'Downstage-level'
df_groundwater_level = df.loc[df['measure'].str.contains("level-groundwater", case=False)]
df_groundwater_level['measure'] = 'Groundwater-level'
for i in range(1,6):
    string = str(var1+'-level-'+str(i))
    df_water_level = df.loc[df['measure'].str.contains(string, case=False)]
    if not df_water_level.empty:
        break
        
df_water_level['measure'] = 'Water-Level'

#Combining all the data frames for different readings
frames = [df_tidal_level, df_stage_level, df_downstage_level, df_groundwater_level, df_water_level]
df = pd.concat(frames)

#Conversion to proper date time format.
df['dateTime'] =  pd.to_datetime(df['dateTime'])
df['Time']=df['dateTime'].dt.time #Adding seperate time Column.
df = df.drop(columns=['dateTime'])#dropping the date column as only single date is mentioned(var2).
df = df.sort_values(by="Time")#Sorting of time values for proper display of line plot

print('Plotting Graphs')
#Plotting of the reading as Line Plot.
fig = px.line(df, x='Time', y='value', color='measure', markers=True, title="Measurement values for "+var1+' Date '+var2)
plotly.offline.plot(fig, filename=str(var1)+'_'+str(var2)+'_graph.html') #Saving the plot as offline html file.

print('Creating Table')
#Associated Table creation of the readings.
fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df.measure, df.value, df.Time],
               fill_color='lavender',
               align='left'))
])

plotly.offline.plot(fig, filename=str(var1)+'_'+str(var2)+'_table.html') #offfline saving of the table as html file.