 # My Python App

## Setup

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output

import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
from numpy.polynomial.polynomial import polyfit
from dash.dependencies import Input, Output

import matplotlib.pyplot as plt

# Load data

df = pd.read_csv(
    'appData.csv')
df = df[0:50]

df2 = pd.read_csv(
    'appdata2.csv')


# print(type(df2['USA GDP 2019']))


# Initialize the app

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

# Creates a list of dictionaries
map_vals = ['2015 GDP per capita','2016 GDP per capita','2017 GDP per capita','2018 GDP per capita','2019 GDP per capita', '2020 Population', '2018 Population', 'Log 2020 Population', 'Log 2018 Population', 'Number of Universites Per State', 'Number of Universites Per State (No CA)']
def get_map_options(map_vals):
    map_options = []
    for i in map_vals:
        map_options.append({'label': i, 'value': i})
    return map_options

x_axis = ['2019 Project Count', '2018 Project Count', '2017 Project Count', 'Outliers Removed (NY, CA, TX, WA) Project Count 2019', '2018-2019 Change in Project Count (%)', '2017-2018 Change in Project Count (%)']
def get_xax_options(x_axis):
    x_axis_options = []
    for i in x_axis:
        x_axis_options.append({'label': i, 'value': i})
    return x_axis_options

y_axis = ['2019 GDP per capita', '2018 GDP per capita', '2017 GDP per capita', 'Outliers Removed (NY, CA, TX, WA) USA GDP 2019', '2018-2019 Change in GDP (%)', '2017-2018 Change in GDP (%)', 'Number of Universites Per State', 'Number of Universites Per State (No CA)', '2020 Population', '2018 Population', 'Log 2020 Population', 'Log 2018 Population']
def get_yax_options(y_axis):
    y_axis_options = []
    for i in y_axis:
        y_axis_options.append({'label': i, 'value': i})
    return y_axis_options


app.layout = html.Div(children=[
             html.Div(className='row',  # Define the row element
                      children=[
                      html.Div(className='four columns div-user-controls',
                                    children=[
                                       html.H1('3D Printing Community Python App'),
                                       html.P('''Use dropdown menu to plot values'''),
                                       html.H2('United States Geographic Map:'),
                                       html.Div(className='div-for-dropdown',
                                            children=[
                                                dcc.Dropdown(id='Map Selection',
                                                   options=get_map_options(map_vals),
                                                   multi=False,
                                                   value=[map_vals[0]],
                                                   style={'backgroundColor': '#1E1E1E'},
                                                   className='MapSelector')
                                                  ],
                                                    style={'color': '#1E1E1E'}),

                                       html.H2('ScatterPlot:'),
                                       html.H2('X-Axis for Scatterplot'),
                                       html.Div(className='X-Axis',
                                             children=[
                                                 dcc.Dropdown(id='X-Axis Select',
                                                    options=get_xax_options(x_axis),
                                                    multi=False,
                                                    value=[x_axis[0]],
                                                    style={'backgroundColor': '#1E1E1E'},
                                                    className='ScatterSelector')
                                                   ],
                                                     style={'color': '#1E1E1E'}),

                                       html.H2('Y-Axis for Scatterplot'),
                                       html.Div(className='Y-Axis',
                                             children=[
                                                 dcc.Dropdown(id='Y-Axis Select',
                                                    options=get_yax_options(y_axis),
                                                    multi=False,
                                                    value=[y_axis[0]],
                                                    style={'backgroundColor': '#1E1E1E'},
                                                    className='ScatterSelector')
                                                   ],
                                                     style={'color': '#1E1E1E'})]

                                                     ),


                    html.Div(className='eight columns div-for-charts bg-grey',
                                    children=[
                                    dcc.Graph(id = "Map"),
                                    dcc.Graph(id='Scatterplot',config={'displayModeBar': False},animate=False)] ,
                                    style={"border":"6px black solid"})
                                         ])
                                     ])

###################################

# Callback for Map
@app.callback(Output('Map', 'figure'),
              [Input('Map Selection', 'value')])
def update_map(selected_dropdown_value):

        mapval = df['2019']

        if selected_dropdown_value == '2015 GDP per capita':
          mapval = df['2015']

        elif selected_dropdown_value == '2016 GDP per capita':
          mapval = df['2016']

        elif selected_dropdown_value == '2017 GDP per capita':
          mapval = df['2017']

        elif selected_dropdown_value == '2018 GDP per capita':
          mapval = df['2018']

        elif selected_dropdown_value == '2019 GDP per capita':
          mapval = df['2019']

        elif selected_dropdown_value == '2020 Population':
          mapval = df['Pop2020']

        elif selected_dropdown_value == '2018 Population':
          mapval = df['Pop2018']

        elif selected_dropdown_value == 'Log 2020 Population':
          mapval = df['Log Pop 2020']

        elif selected_dropdown_value == 'Log 2018 Population':
          mapval = df['Log Pop 2018']

        elif selected_dropdown_value == 'Number of Universites Per State':
            mapval = df['Number of Universites Per State']

        elif selected_dropdown_value == 'Number of Universites Per State (No CA)':
            mapval = df['Number of Universites Per State (No CA)']

        figure = go.Figure(
            data=go.Choropleth(
            locations=df['GeoName'], # Spatial coordinates
            z = mapval, # Data to be color-coded
            locationmode = 'USA-states', # set of locations match entries in `locations`
            colorscale = 'Reds',
            colorbar_title = "Density"),
            layout = go.Layout(geo=dict(bgcolor= 'rgba(0,0,0,0)', lakecolor='#1E1E1E',
              landcolor='rgba(51,17,0,0.2)',
              subunitcolor='black'),
              title = 'Geographic Data: ' + str( selected_dropdown_value ),
              font = {"size": 9, "color":"White"},
              titlefont = {"size": 15, "color":"White"},
              geo_scope='usa',
              margin={"r":0,"t":40,"l":0,"b":0},
              paper_bgcolor='#1E1E1E',
              plot_bgcolor='#1E1E1E',
              )
              )
        return figure


# Callback for Map
@app.callback(Output('Scatterplot', 'figure'),
              [Input('X-Axis Select', 'value'),
               Input('Y-Axis Select','value')])

def update_scatter(x1,y1):

    xval = 'Project Count 2019'
    yval = 'USA GDP 2019'

    if x1 == '2019 Project Count':
      xval = 'Project Count 2019'

    elif x1  == '2018 Project Count':
      xval = 'Project Count 2018'

    elif x1 == '2017 Project Count':
      xval = 'Project Count 2017'

    elif x1 == 'Outliers Removed (NY, CA, TX, WA) Project Count 2019':
      xval = 'Outliers Removed (NY, CA, TX, WA) Project Count 2019'

    elif x1 == '2018-2019 Change in Project Count (%)':
          xval = '2018-2019 Change in Project Count (%)'

    elif x1 == '2017-2018 Change in Project Count (%)':
         xval = '2017-2018 Change in Project Count (%)'

    if y1 == '2019 GDP per capita':
      yval = 'USA GDP 2019'

    elif y1 == '2018 GDP per capita':
      yval = 'USA GDP 2018'

    elif y1 == '2017 GDP per capita':
      yval = 'USA GDP 2017'

    elif y1 == 'Outliers Removed (NY, CA, TX, WA) USA GDP 2019':
      yval = 'Outliers Removed (NY, CA, TX, WA) USA GDP 2019'

    elif y1 == '2017-2018 Change in GDP (%)':
         yval = '2017-2018 Change in GDP (%)'

    elif y1 == '2018-2019 Change in GDP (%)':
        yval = '2018-2019 Change in GDP (%)'

    elif y1 == 'Number of Universites Per State':
        yval = 'Number of Universites Per State'

    elif y1 == 'Number of Universites Per State (No CA)':
        yval = 'Number of Universites Per State (No CA)'

    elif y1 == '2020 Population':
      yval = 'Pop2020'

    elif y1 == '2018 Population':
          yval = 'Pop2018'

    elif y1 == 'Log 2020 Population':
          yval = 'Log Pop 2020'

    elif y1 == 'Log 2018 Population':
          yavl = 'Log Pop 2018'

    # b, m = polyfit(xval, yval, 1)

    figure = go.Figure(
      data=px.scatter(df2,
           x=xval,
           y=yval,
           text="Location",
           title="United States Data Comparison",
           template='plotly_dark',
           trendline = 'ols'))


    figure.layout.plot_bgcolor = '#1E1E1E'
    figure.layout.paper_bgcolor = '#1E1E1E'


    return figure


      # figure.plot(xval, b + m * xval, '-', label= 'y=' + str(m) + 'x' + '+' + str(b))
      # figure.legend()

if __name__ == "__main__":
    app.run_server(debug=True)
