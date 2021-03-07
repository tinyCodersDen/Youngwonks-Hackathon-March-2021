import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
import urllib.request
import json
from dash.dependencies import Input, Output
meteor = pd.read_csv('meteorite-landings.csv')
meteor['year'] = meteor['year'].astype(str)
meteor['text'] = 'Name: '+meteor['name']+', Year: '+meteor['year']
px.set_mapbox_access_token('pk.eyJ1IjoiY29kZXJraWQiLCJhIjoiY2tseThwcGhwMDFvYTJ2cW1zbHR4dGNyMSJ9.IYT3RvLvFmnXESlPrwTLEA')
fig = px.scatter_mapbox(meteor,
                        lat=meteor['reclat'],
                        lon=meteor['reclong'],
                        hover_name="name",
                        zoom=1)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.H1("Space World Dashboard", style={'text-align': 'center'}),
    html.H3('By: Vihan Raval',style={'text-align':'center'}),
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'UFO Sightings', 'value': 'ufo'},
            {'label': 'Meteorite Crashes', 'value': 'meteor'},
            {'label': 'ISS Tracker', 'value': 'ISS'}
        ],
        value='UFO Sightings'
    ),
    html.Div(id='dd-output-container')
])
@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    if value=='meteor':
        meteor = pd.read_csv('meteorite-landings.csv')
        meteor['year'] = meteor['year'].astype(str)
        meteor['text'] = 'Name: '+meteor['name']+', Year: '+meteor['year']
        px.set_mapbox_access_token('pk.eyJ1IjoiY29kZXJraWQiLCJhIjoiY2tseThwcGhwMDFvYTJ2cW1zbHR4dGNyMSJ9.IYT3RvLvFmnXESlPrwTLEA')
        fig = px.scatter_mapbox(meteor,
                                lat=meteor['reclat'],
                                lon=meteor['reclong'],
                                hover_name="name",
                                zoom=1)
        fig.show()
    if value=='ufo':
        ufo = pd.read_excel('UFOs_coord.xls')
        px.set_mapbox_access_token('pk.eyJ1IjoiY29kZXJraWQiLCJhIjoiY2tseThwcGhwMDFvYTJ2cW1zbHR4dGNyMSJ9.IYT3RvLvFmnXESlPrwTLEA')
        dict1 = {}
        for t in ufo['State']:
            if t not in dict1.keys():
                dict1[t]=1
            else:
                dict1[t]+=1
        s,v = [],[]
        for t in dict1.keys():
            s.append(t)
        for t in dict1.values():
            v.append(t)
        dict2 = {'States':s,'Reports':v}
        df = pd.DataFrame(dict2)
        fig = px.scatter_mapbox(ufo,
                                lat=ufo['lat'],
                                lon=ufo['lng'],
                                hover_name='City')
        fig.show()
    if value=='ISS':
        req = urllib.request.urlopen("http://api.open-notify.org/iss-now.json")
        obj = json.loads(req.read())
        long = float(obj['iss_position']['longitude'])
        lat = float(obj['iss_position']['latitude'])
        dict1 = {'Latitude':lat,'Longitude':long}
        df = pd.DataFrame(dict1,index=[0])
        fig = px.scatter_mapbox(df,
                                lat='Latitude',
                                lon='Longitude')
        fig.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "sourceattribution": "United States Geological Survey",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ])
        fig.show()
if __name__=='__main__':
    app.run_server()