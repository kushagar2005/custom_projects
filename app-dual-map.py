import sys
import os 
#Adding the ml_package location 
sys.path.append('/home/kr/ml/ml_package')

import dash
from dash import Dash, Input, Output, State, html, dcc, dash_table, callback
from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import folium

#importing the list from sql database.

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Heatmap Application'),
    html.Iframe(id = 'map1', srcDoc = open('/home/kr/ml/result/heat_map_2022_02_18-03:46:29_PM.html', 'r').read(), width='50%', height='500'),

    html.H1('Interactive Map Visualisation'),
    html.Iframe(id = 'map2', srcDoc = open('/home/kr/ml/result/intercative_map_2022_02_18-03:45:48_PM.html', 'r').read(), width='50%', height='500'),

    html.Button('Refresh for latest data', id='click-1', n_clicks=0),
    html.Div(id='body-div')
])

@app.callback(
    Output(component_id='body-div', component_property='children'),
    Input(component_id='click-1', component_property='n_clicks')
)
def get_list(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else :
        #get list from database
        import pandas as pd
        from sqlalchemy import create_engine
        import psycopg2
        
        conn_string = 'postgresql://krml:password@localhost:5432/mldata'
        db = create_engine(conn_string)
        conn = db.connect()
        
        sql_command = "select tablename from pg_tables where schemaname='public';"
        df_sql = pd.read_sql(sql_command, conn)
        data = df_sql.to_dict('rows')
        columns =  [{"name": i, "id": i,} for i in (df_sql.columns)]
        return dash_table.DataTable(style_cell={'overflowX': 'auto'},
                                    style_table={'whiteSpace': 'normal','minWidth': '180px', 'width': '180px', 'maxWidth': '180px'},
            data=data, 
            columns=columns,
            row_selectable="multi")


if __name__ == "__main__":
    app.run_server(debug = True)


#Testing of metaflow application to make data pipeline.