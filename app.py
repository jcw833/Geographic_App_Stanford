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
from dash.dependencies import Input, Output, State

import plotly.figure_factory as ff

import numpy as np

import matplotlib.pyplot as plt
import pathlib
import os

# Load data

df = pd.read_csv(
    'appData.csv')
df = df[0:50]

# df2 = pd.read_csv(
#     'appdata2.csv')


# Load data


# df_lat_lon = pd.read_csv("CountyData.csv", encoding='cp1252')

# Load data

df_unemp = pd.read_csv('UnemploymentStats.csv')
df_unemp['State FIPS Code'] = df_unemp['State FIPS Code'].apply(lambda x: str(x).zfill(2))
df_unemp['County FIPS Code'] = df_unemp['County FIPS Code'].apply(lambda x: str(x).zfill(3))
df_unemp['FIPS'] = df_unemp['State FIPS Code'] + df_unemp['County FIPS Code']



# Initialize app

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
server = app.server

# server = flask.Flask(__name__)
# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], server=server)

colorscale = [
    "#f2fffb",
    "#bbffeb",
    "#98ffe0",
    "#79ffd6",
    "#6df0c8",
    "#69e7c0",
    "#59dab2",
    "#45d0a5",
    "#31c194",
    "#2bb489",
    "#25a27b",
    "#1e906d",
    "#188463",
    "#157658",
    "#11684d",
    "#10523e",
]

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

# Creates a list of dictionaries
# map_vals = ['2015 GDP per capita','2016 GDP per capita','2017 GDP per capita','2018 GDP per capita','2019 GDP per capita', '2020 Population', '2018 Population', 'Log 2020 Population', 'Log 2018 Population', 'Number of Universites Per State', 'Number of Universites Per State (No CA)']
# def get_map_options(map_vals):
#     map_options = []
#     for i in map_vals:
#         map_options.append({'label': i, 'value': i})
#     return map_options

# x_axis = ['2019 Project Count', '2018 Project Count', '2017 Project Count', 'Outliers Removed (NY, CA, TX, WA) Project Count 2019', '2018-2019 Change in Project Count (%)', '2017-2018 Change in Project Count (%)']
x_axis = ['2019 GDP per capita', '2018 GDP per capita', '2017 GDP per capita', '2016 GDP per capita', '2015 GDP per capita']
def get_xax_options(x_axis):
    x_axis_options = []
    for i in x_axis:
        x_axis_options.append({'label': i, 'value': i})
    return x_axis_options

# y_axis = ['Outliers Removed (NY, CA, TX, WA) USA GDP 2019', '2018-2019 Change in GDP (%)', '2017-2018 Change in GDP (%)', 'Number of Universites Per State', 'Number of Universites Per State (No CA)', '2020 Population', '2018 Population', 'Log 2020 Population', 'Log 2018 Population'
y_axis = ['2020 Population', '2018 Population', '2010 Population', 'Log 2020 Population', 'Log 2018 Population', 'Log 2010 Population']
def get_yax_options(y_axis):
    y_axis_options = []
    for i in y_axis:
        y_axis_options.append({'label': i, 'value': i})
    return y_axis_options


YEARS = [2015, 2016, 2017, 2018, 2019]

#######################################################################################


# App layout

app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.H4(children="USA Geographic Analysis Application"),
                html.P(
                    id="description",
                    children="† Graph Geographic Data Below:",
                ),
            ],
        ),

        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="mapdropdown-container",
                            children=[
                                dcc.Dropdown(
                                    id='Mapselect',
                                    options=[
                                       {'label': 'State GDP', 'value': 'GDP'},
                                       {'label': 'County Population', 'value': 'POP'},
                                       {'label': 'County Unemployment', 'value': 'Unemployment'},
                                       ],
                                     value=['Unemployment'],
                                     multi=False,
                                     className='MapSelector',
                                     style={'color': '#1E1E1E'}),
                                dcc.Checklist(
                                        id="checkbox",
                                        options=[
                                            {'label': 'State GDP', 'value': 'GDP'},
                                            {'label': 'County Population', 'value': 'POP'},
                                            {'label': 'County Unemployment', 'value': 'Unemployment'},
                                        ],
                                        value=['Unemployment']
                                        )]),

                        html.Div(
                            id="slider-container",
                            children=[
                                html.P(
                                    id="slider-text",
                                    children="Drag the slider to adjust year:",
                                ),
                                dcc.Slider(
                                    id="years-slider",
                                    min=min(YEARS),
                                    max=max(YEARS),
                                    value=min(YEARS),
                                    marks={
                                        str(year): {
                                            "label": str(year),
                                            "style": {"color": "#7fafdf"},
                                        }
                                        for year in YEARS
                                    },
                                ),
                            ],
                        ),

                        html.Div(
                            id="heatmap-container",
                            children=[
                                html.P(
                                    "Data Visualization".format(
                                        min(YEARS)
                                    ),
                                    id="heatmap-title",
                                ),
                                dcc.Graph(
                                    id="county-choropleth",
                                    figure=dict(
                                        layout=dict(
                                            mapbox=dict(
                                                layers=[],
                                                accesstoken=mapbox_access_token,
                                                style=mapbox_style,
                                                center=dict(
                                                    lat=38.72490, lon=-95.61446
                                                ),
                                                pitch=0,
                                                zoom=3.5,
                                            ),
                                            autosize=True,
                                        ),
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    id="graph-container",
                    children=[
                    html.P(id="chart-selector", children="Select Plot:"),
                    html.P('X-Axis for Scatterplot'),
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
                    html.P('Y-Axis for Scatterplot'),
                    dcc.Dropdown(id='Y-Axis Select',
                                    options=get_yax_options(y_axis),
                                    multi=False,
                                    value=[y_axis[0]],
                                    style={'backgroundColor': '#1E1E1E'},
                                    className='ScatterSelector'),

                        dcc.Graph(
                            id="Scatterplot",
                            figure=dict(
                                data=[dict(x=0, y=0)],
                                layout=dict(
                                    paper_bgcolor="#1E1E1E",
                                    plot_bgcolor="#1E1E1E",
                                    autofill=True,
                                    margin=dict(t=75, r=50, b=100, l=50),
                                ),
                            ),
                        ),
                    ],
                ),
            ],
        ),
        ])


###################################


@app.callback(
    Output("county-choropleth", "figure"),
    [Input("years-slider", "value")],
    [Input("checkbox", "value")],
    [State("county-choropleth", "figure")],
)
def display_map(year, checkbox, figure):

    if checkbox == ['Unemployment']:

        print(checkbox)
        print(year)

        endpts = list(np.linspace(1, 12, len(colorscale) - 1))
        fips = df_unemp['FIPS'].tolist()
        values = df_unemp['Unemployment Rate '+str(year)+' (%)'].tolist()


        fig = ff.create_choropleth(
            fips=fips, values=values, scope=['usa'],
            binning_endpoints=endpts, colorscale=colorscale,
            show_state_data=False,
            show_hover=True,
            asp = 2.9,
            legend_title = '% unemployed '+str(year)
        )


        fig.layout.paper_bgcolor="#252b33"
        fig.layout.plot_bgcolor="#252b33"

        return fig

    elif checkbox == ['POP']:

        print(checkbox)
        print(year)

        endpts = list(np.linspace(10000, 1000000, len(colorscale) - 1))
        fips = df_unemp['FIPS'].tolist()
        values = df_unemp['Pop '+str(year)].tolist()


        fig = ff.create_choropleth(
            fips=fips, values=values, scope=['usa'],
            binning_endpoints=endpts, colorscale=colorscale,
            show_state_data=False,
            show_hover=True,
            asp = 2.9,
            legend_title = 'County Population '+str(year)
        )


        fig.layout.paper_bgcolor="#252b33"
        fig.layout.plot_bgcolor="#252b33"

        return fig

    elif checkbox == ['GDP']:

            print(checkbox)
            print(year)

            endpts = list(np.linspace(40000, 100000, len(colorscale) - 1))
            fips = df_unemp['FIPS'].tolist()
            values = df_unemp['GDP '+str(year)].tolist()


            fig = ff.create_choropleth(
                fips=fips, values=values, scope=['usa'],
                binning_endpoints=endpts, colorscale=colorscale,
                show_hover=True,
                asp = 2.9,
                legend_title = 'GDP '+str(year)
            )


            fig.layout.paper_bgcolor="#252b33"
            fig.layout.plot_bgcolor="#252b33"

            return fig



    else:

        endpts = list(np.linspace(1, 12, len(colorscale) - 1))
        fips = df_unemp['FIPS'].tolist()
        values = df_unemp['Unemployment Rate '+str(year)+' (%)'].tolist()


        fig = ff.create_choropleth(
            fips=fips, values=values, scope=['usa'],
            binning_endpoints=endpts, colorscale=colorscale,
            show_state_data=False,
            show_hover=True,
            asp = 2.9,
            legend_title = '% unemployed '+str(year)
        )


        fig.layout.paper_bgcolor="#252b33"
        fig.layout.plot_bgcolor="#252b33"

        return fig




# Callback for Map
@app.callback(Output('Scatterplot', 'figure'),
              [Input('X-Axis Select', 'value'),
               Input('Y-Axis Select','value')])

def update_scatter(x1,y1):

    xval = '2019 GDP per capita'
    yval = '2020 Population'

    if x1 == '2019 GDP per capita':
      xval = '2019 GDP per capita'

    elif x1 == '2018 GDP per capita':
      xval = '2018 GDP per capita'

    elif x1 == '2017 GDP per capita':
      xval = '2017 GDP per capita'

    elif x1 == '2016 GDP per capita':
      xval = '2016 GDP per capita'

    elif x1 == '2015 GDP per capita':
      xval = '2015 GDP per capita'



    if y1 == '2020 Population':
        yval = '2020 Population'

    elif y1 == '2018 Population':
        yval = '2018 Population'

    elif y1 == '2010 Population':
        yval = '2010 Population'

    elif y1 == 'Log 2020 Population':
          yval = 'Log 2020 Population'

    elif y1 == 'Log 2018 Population':
          yavl = 'Log 2018 Population'

    elif y1 == 'Log 2010 Population':
         yavl = 'Log 2010 Population'



    figure = go.Figure(
      data=px.scatter(df,
           x=xval,
           y=yval,
           text="GeoName",
           title="United States Data Comparison",
           template='plotly_dark',
           trendline = 'ols'))



    figure.layout.paper_bgcolor="#252b33"
    figure.layout.plot_bgcolor="#252b33"


    return figure



if __name__ == "__main__":
    app.run_server(debug=True)
