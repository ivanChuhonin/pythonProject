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
        html.Label(['Choose 3 Partners to Compare:'],style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='cuisine_one',
            options=[{'label':x, 'value':x} for x in df_top20['Partner'].unique()],
            value='Germany',
            multi=False,
            disabled=False,
            clearable=True,
            searchable=True,
            placeholder='Choose Cuisine...',
            className='form-dropdown',
            style={'width':"90%"},
            persistence='string',
            persistence_type='memory'),

        dcc.Dropdown(id='cuisine_two',
            options=[{'label':x, 'value':x} for x in df_top20['Partner'].unique()],
            value='China',
            multi=False,
            clearable=False,
            persistence='string',
            persistence_type='session'),

        dcc.Dropdown(id='cuisine_three',
            options=[{'label':x, 'value':x} for x in df_top20['Partner'].unique()],
            value='Netherlands',
            multi=False,
            clearable=False,
            persistence='string',
            persistence_type='local')], className='three columns'),

    html.Div([
        dcc.Graph(figure={}, id='controls-and-graph'),
        html.Label(['Choose 3 Partners to Compare:'],style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='cuisine_first',
            options=[{'label':x, 'value':x} for x in manufactured_df3['Partner'].unique()],
            value='Netherlands',
            multi=False,
            disabled=False,
            clearable=True,
            searchable=True,
            placeholder='Choose Cuisine...',
            className='form-dropdown',
            style={'width':"90%"},
            persistence='string',
            persistence_type='memory'),

        dcc.Dropdown(id='cuisine_second',
            options=[{'label':x, 'value':x} for x in manufactured_df3['Partner'].unique()],
            value='Switzerland',
            multi=False,
            clearable=False,
            persistence='string',
            persistence_type='session'),

        dcc.Dropdown(id='cuisine_third',
            options=[{'label':x, 'value':x} for x in manufactured_df3['Partner'].unique()],
            value='Belgium',
            multi=False,
            clearable=False,
            persistence='string',
            persistence_type='local')], className='three columns'),   

    html.Div([
        dcc.Graph(id='our_graphs')], className='nine columns'),

    html.Div([
        html.Br(),
        html.Label(['Choose 3 Partners to Compare:'],style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='cuisine_num',
            options=[{'label':x, 'value':x} for x in sugar_df3['Partner'].unique()],
            value='Mongolia',
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
            value='China',
            multi=False,
            clearable=False,
            persistence='string',
            persistence_type='session'),

        dcc.Dropdown(id='cuisine_nums',
            options=[{'label':x, 'value':x} for x in sugar_df3['Partner'].unique()],
            value='Turkey',
            multi=False,
            clearable=False,
            persistence='string',
            persistence_type='local')], className='three columns')
])


@app.callback(
    Output('our_graph','figure'),
    [Input('cuisine_one','value'),
     Input('cuisine_two','value'),
     Input('cuisine_three','value'),
     Input(component_id='controls-and-radio-item', component_property='value')]
)

def build_graph(first_cuisine, second_cuisine, third_cuisine, col_chosen):
    dff=df_top20[(df_top20['Partner']==first_cuisine)|
           (df_top20['Partner']==second_cuisine)|
           (df_top20['Partner']==third_cuisine)]
    fig = px.line(dff, x="Year", y=col_chosen, color='Partner', height=600) # Trade Value (US$)
    fig.update_layout(yaxis={'title':'Trade Value (US$)'},
                      title={'text':'Trading history',
                      'font':{'size':28},'x':0.5,'xanchor':'center'})
    return fig


@app.callback(
     Output(component_id='controls-and-graph', component_property='figure'),
     [Input('cuisine_first','value'),
     Input('cuisine_second','value'),
     Input('cuisine_third','value')]
)

def build_graph(cuisine_first, cuisine_second, cuisine_third):
    df_manuf = manufactured_df3[(manufactured_df3['Partner']==cuisine_first)|
           (manufactured_df3['Partner']==cuisine_second)|
           (manufactured_df3['Partner']==cuisine_third)]
    fig = px.area(x=df_manuf["Year"], y=df_manuf["Trade Value (US$)"], color=df_manuf["Partner"],
                  line_group=df_manuf["Partner"], pattern_shape=df_manuf["Partner"], pattern_shape_sequence=[".", "x", "+"])
    fig.update_layout(yaxis={'title':'Trade Value (US$)'}, xaxis={'title':'Year'},
                      title={'text':'Trading manufactured goods', 'font':{'size':28},'x':0.5,'xanchor':'center'})
    return fig


@app.callback(
    Output('our_graphs','figure'),
    [Input('cuisine_num','value'),
     Input('cuisine_numer','value'),
     Input('cuisine_nums','value')]
)

def build_graph(cuisine_num, cuisine_numer, cuisine_nums):
    dff=sugar_df3[(sugar_df3['Partner']==cuisine_num)|
           (sugar_df3['Partner']==cuisine_numer)|
           (sugar_df3['Partner']==cuisine_nums)]

    fig = px.line(dff, x="Year", y="Trade Value (US$)", color='Partner', height=600)
    fig.update_layout(yaxis={'title':'Trade Value (US$)'},
                      title={'text':'Trading sugar',
                      'font':{'size':28},'x':0.5,'xanchor':'center'})
    return fig


#if __name__ == '__main__':
#app.run_server(debug=False)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8052, help="Port number")
    args = parser.parse_args()

    app.run_server(debug=True, port=args.port)    

