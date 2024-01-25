import pandas as pd
import warnings
import numpy as np
from zipfile import ZipFile
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input


df_top20 = pd.read_csv("/workspaces/pythonProject/df_top20.csv")
manufactured_df3 = pd.read_csv("/workspaces/pythonProject/manufactured_df3.csv")
manufactured_df444 = pd.read_csv("/workspaces/pythonProject/manufactured_df444.csv")
sugar_df3 = pd.read_csv("/workspaces/pythonProject/sugar_df3.csv")


app = dash.Dash(__name__)


app.layout = html.Div([

    html.Div([
        dcc.Graph(id='our_graph')], className='nine columns'),

    html.Div([
        dcc.RadioItems(options=['Trade Value (US$)', 'Qty'], value='Trade Value (US$)', id='controls-and-radio-item'),
        html.Br(),
        html.Label(['Choose year to display:'],style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='cuisine_one',
            options=[{'label':x, 'value':x} for x in df_top20['Year'].unique()],
            value=2007,
            multi=False,
            disabled=False,
            clearable=True,
            searchable=True,
            placeholder='Choose partner...',
            className='form-dropdown',
            style={'width':"90%"},
            persistence='string',
            persistence_type='memory')
        ]),

    html.Div(children='Top 20 countries in trading manufactured goods'),
    html.Hr(),
    dcc.Graph(figure={}, id='controls-and-graph'),
    dcc.Dropdown(id='cuisine_first',
            options=[{'label':x, 'value':x} for x in manufactured_df3['Partner'].unique()],
            value='Kazakhstan',
            multi=False,
            disabled=False,
            clearable=True,
            searchable=True,
            placeholder='Choose year...',
            className='form-dropdown',
            style={'width':"90%"},
            persistence='string',
            persistence_type='memory'),


    html.Div([
        dcc.Graph(id='graph')], className='nine columns'),

    html.Div([
        html.Div(children='Top 20 countries in trading sugar'),
        html.Hr(),
        html.Br(),
        html.Label(['Choose 3 Partners to Compare:'],style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='cuisine_num',
            options=[{'label':x, 'value':x} for x in sugar_df3['Partner'].unique()],
            value='Kazakhstan',
            multi=False,
            disabled=False,
            clearable=True,
            searchable=True,
            placeholder='Choose Partner...',
            className='form-dropdown',
            style={'width':"90%"},
            persistence='string',
            persistence_type='memory'),

        dcc.Dropdown(id='cuisine_numer',
            options=[{'label':x, 'value':x} for x in sugar_df3['Partner'].unique()],
            value='Belarus',
            multi=False,
            clearable=False,
            persistence='string',
            persistence_type='session'),

        dcc.Dropdown(id='cuisine_nums',
            options=[{'label':x, 'value':x} for x in sugar_df3['Partner'].unique()],
            value='Ukraine',
            multi=False,
            clearable=False,
            persistence='string',
            persistence_type='local')], className='three columns')
])


@app.callback(
    Output('our_graph','figure'),
    [Input('cuisine_one','value'),
     Input(component_id='controls-and-radio-item', component_property='value')])


def build_graph(first_cuisine, col_chosen):
    dff=df_top20[(df_top20['Year']==first_cuisine)]
    fig = px.histogram(dff, x="Partner", y=col_chosen, color='Partner', color_discrete_sequence=px.colors.qualitative.Dark24, height=600)
    fig.update_layout(yaxis={'title':'Trade Value (US$)'},
                      title={'text':'Trading history',
                      'font':{'size':28},'x':0.5,'xanchor':'center'})
    return fig


@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input('cuisine_first','value')
)

def build_graph(cuisine_first):
    df_man = manufactured_df3[(manufactured_df3['Partner']==cuisine_first)]
    fig = px.area(x=df_man["Year"], y=df_man["Trade Value (US$)"], color_discrete_sequence=['green'],
                  pattern_shape_sequence=["x"], labels={'x':'Year', 'y':'Trade Value (US$)'})      # ".", "x", "+"
    return fig


@app.callback(
    Output('graph','figure'),
    [Input('cuisine_num','value'),
     Input('cuisine_numer','value'),
     Input('cuisine_nums','value')]
)

def build_graph(cuisine_num, second_cuisine, third_cuisine):
    dff=sugar_df3[(sugar_df3['Partner']==cuisine_num)|
           (sugar_df3['Partner']==second_cuisine)|
           (sugar_df3['Partner']==third_cuisine)]

    fig = px.line(dff, x="Year", y="Trade Value (US$)", color='Partner', height=600)
    fig.update_layout(yaxis={'title':'Trade Value (US$)'},
                      title={'text':'Trading sugar',
                      'font':{'size':28},'x':0.5,'xanchor':'center'})
    return fig


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8051, help="Port number")
    args = parser.parse_args()

    app.run_server(debug=True, port=args.port)    