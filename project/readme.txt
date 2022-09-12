Project - Tool for selection and viewing the data for individual measurement station in Real Time flood-monitoring API provided by the UK’s Environmental Agency.

Usage of the Tool - 

python3 tool_1.py
python3 tool_2.py 'base station notation' 'Date in YYYY-MM-DD format' 

Select the individual measurement station using tool map_interactive.html and map_all_station.html based on below parameters
Location 
Status 
Qualifier
Measurement Station parameters

Once the measurement station is selected/chosen. The value of all reading is viewed in table and graph by running the script tool_2.py with entering user parameters. It will generate output as html web pages showing the table and graphs of the readings.

Environment Setup - 

requirements.txt - It can be used to install all python dependences for setting up python environment.

environment.yml - If using Anaconda Python environment. It can be used to install all dependencies and create conda environment.


Folder Description -
 
The project folder consist of 3 sub folders which are explained below. 

Scripts - It consist of 2 scripts named tool_1.py and tool_2.py

tool_1.py : It is the script developed in python for generating html pages which provides interactivity for selection of individual measurement station. Files generated are map_interactive.html and map_all_station.htm

tool_2.py - By running the script it will fetch all the reading of individual measurement station based on the qualifier and parameter values. To run the script 2 user inputs are required when executing the script in python.
User Input 1 : Notation of the selected measurement station 
User Input 2 : Date for the which data is to be fetched in YYYY-MM-DD format.

Files generated are 'notation'_'date'_table.html
Files generated are 'notation'_'date'_graph.html

Visualisation - It contains main tool for selection of individual measurement station.

map_all_station.html  :

It visualises all the measurement station fetched from the API provided by the UK’s Environmental Agency.

Markers - Represent the individual measurement station upon hovering mouse cursor over each marker, It will show the label name and notation of individual measurement station.
On clicking the marker it will further provide the information about the measurement station.
Label Name, Notation, Latitude, Longitude.

Color of the marker represent the status of measurement station -
Green - Active status 
Red - Closed Status 
Blue - statusukcmf 
Orange - Suspended Status
Gray - nan Status (None value)


map_interactive.html :

It visualises the measurement station as markers and give more control to select a specific type of station.
By hovering over the right corner of the map it will open the checkbox menu.
Checkbox shows the Different parameters and qualifiers of the measurement stations.
Select single checkbox to represent the station of that specific Qualifier or Parameter.

Red color markers represents the measurement station based on Parameters.
Green color marker represents the measurement stations based on the qualifier. 

Measurement station notation can be seen when hovering mouse cursor over the marker.

sample -

755900B_2022-08-02_table.html, 755900B_2022-08-02_graph.html - Table and Graphs for all the reading from the measurement station with notation 755900B for the date 02-08-2022.

755900B - Screenshot showing the location of the measurement station.
