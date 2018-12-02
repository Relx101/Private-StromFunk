# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import sqlite3
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import json

Alle_Tabellen = []
with open('Config.json') as f:
    jsondata = json.load(f)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([

    # Configfelder
    html.Div([
        html.Label('setup_u_step'),
        dcc.Input(value=jsondata['setup_u_step'], type='number', id='setup_u_step'),
        html.Label('setup_u_start 1'),
        dcc.Input(value=jsondata['setup_u_start'][0], type='number', id='setup_u_start0'),
        html.Label('setup_u_start 2'),
        dcc.Input(value=jsondata['setup_u_start'][1], type='number', id='setup_u_start1'),
        html.Label('setup_u_start 3'),
        dcc.Input(value=jsondata['setup_u_start'][2], type='number', id='setup_u_start2'),
        html.Label('setup_u_ratio '),
        dcc.Input(value=jsondata['setup_u_ratio'], type='number', id='setup_u_ratio'),
        html.Label('setup_i_ratio 1'),
        dcc.Input(value=jsondata['setup_i_ratio'][0], type='number', id='setup_i_ratio0'),
        html.Label('setup_i_ratio 2'),
        dcc.Input(value=jsondata['setup_i_ratio'][1], type='number', id='setup_i_ratio1'),
        html.Label('setup_i_ratio 3'),
        dcc.Input(value=jsondata['setup_i_ratio'][2], type='number', id='setup_i_ratio2'),
        html.Label('setup u_max'),
        dcc.Input(value=jsondata['setup_u_max'], type='number', id='setup_u_max'),
        html.Label('setup i_max'),
        dcc.Input(value=jsondata['setup_i_max'], type='number', id='setup_i_max'),
    ], className='Setupflaechen'),
    html.Div([
        html.Label('control_i_target 1'),
        dcc.Input(value=jsondata['control_i_target'][0], type='number', id='control_i_target0'),
        html.Label('control_i_target  2'),
        dcc.Input(value=jsondata['control_i_target'][1], type='number', id='control_i_target1'),
        html.Label('control_i_target  3'),
        dcc.Input(value=jsondata['control_i_target'][2], type='number', id='control_i_target2'),
        html.Label('control_i_delta  1'),
        dcc.Input(value=jsondata['control_i_delta'][0], type='number', id='control_i_delta0'),
        html.Label('control_i_delta 2'),
        dcc.Input(value=jsondata['control_i_delta'][1], type='number', id='control_i_delta1'),
        html.Label('control_i_delta 3'),
        dcc.Input(value=jsondata['control_i_delta'][2], type='number', id='control_i_delta2'),

    ], className='Steuerflaechen'),
    # Achsenauswahlfelder

    html.Div([
        html.Label('Achse links'),
        dcc.Dropdown(
            id='Achse-links',
            options=[{'label': Tabelle[0], 'value': Tabelle[0]} for Tabelle in Alle_Tabellen],
        ), html.Label('Reihe'),
        dcc.Dropdown(
            id='Achse-links-Reihe',
            options=[
                {'label': 'Kanal 1', 'value': 'v_channel_0'},
                {'label': 'Kanal 2', 'value': 'v_channel_1'},
                {'label': 'Kanal 3', 'value': 'v_channel_2'},
                {'label': 'Kanal 4', 'value': 'v_channel_3'}
            ],
            value='v_channel_0'
        ),
    ], className='Achsenwahlfeld_links'),
    html.Div([
        html.Label('Achse Rechts'),
        dcc.Dropdown(
            id='Achse-rechts',
            options=[{'label': Tabelle[0], 'value': Tabelle[0]} for Tabelle in Alle_Tabellen],
        ), html.Label('Reihe'),
        dcc.Dropdown(
            id='Achse-rechts-Reihe',
            options=[
                {'label': 'Kanal 1', 'value': 'v_channel_0'},
                {'label': 'Kanal 2', 'value': 'v_channel_1'},
                {'label': 'Kanal 3', 'value': 'v_channel_2'},
                {'label': 'Kanal 4', 'value': 'v_channel_3'}
            ],
            value='v_channel_0',
        ),
    ], className='Achsenwahlfeld_rechts'),

    html.Div([
        dcc.Graph(id='maingraph')
    ], className='PrimaerGraph'),
    dcc.Interval(
        id='interval-update_Alle_Tabellen',
        interval=10 * 1000,  # in milliseconds -> alle 10 s
        n_intervals=0
    ),
    dcc.Interval(
        id='interval-update-Graph',
        interval=2 * 1000,  # in milliseconds -> alle 10 s
        n_intervals=0
    )
], className='Hauptdiv')


@app.callback(
    dash.dependencies.Output('setup_i_max', 'value'),
    [dash.dependencies.Input('setup_u_step', 'value')])
def update_setup_u_step(Wert):
    print(jsondata['setup_u_step'])
    if int(Wert) <= -1000:
        print('ueberschreibe...')
        return 1234
    elif Wert != jsondata['setup_u_step']:
        jsondata['setup_u_step'] = int(Wert)
        with open('Config.json', 'w') as f:
            json.dump(jsondata, f, sort_keys=False, indent=4, ensure_ascii=False)
    pass


@app.callback(
    dash.dependencies.Output('maingraph', 'figure'),
    [dash.dependencies.Input('interval-update-Graph', 'n_intervals'),
     dash.dependencies.Input('Achse-links', 'value'),
     dash.dependencies.Input('Achse-links-Reihe', 'value'),
     dash.dependencies.Input('Achse-rechts', 'value'),
     dash.dependencies.Input('Achse-rechts-Reihe', 'value')])
def update_main_graph(n_intervals, Axlinks, ReiheL, Axrechts, ReiheR):
    # print(len(ReiheR))
    # print(ReiheL)
    if (Axlinks != None and ReiheL != None):
        db = sqlite3.connect("./hochstrom.db")
        Dataquery = pd.read_sql_query("select time, {} from {};" .format(ReiheL, Axlinks), db)
        xdata1 = Dataquery['time']
        ydata1 = Dataquery[ReiheL]
    else:
        xdata1 = []
        ydata1 = []
    if (Axrechts != None and ReiheR != None):
        db = sqlite3.connect("./hochstrom.db")
        Dataquery = pd.read_sql_query("select time, {} from {};" .format(ReiheR, Axrechts), db)
        xdata2 = Dataquery['time']
        ydata2 = Dataquery[ReiheR]
    else:
        xdata2 = []
        ydata2 = []
    trace1 = go.Scatter(
        x=xdata1,
        y=ydata1,
        name='yaxis data'
    )
    trace2 = go.Scatter(
        x=xdata2,
        y=ydata2,
        name='yaxis2 data',
        yaxis='y2'
    )
    data = [trace1, trace2]

    layout = go.Layout(
        showlegend=False,
        yaxis=dict(
            title='yaxis title'
        ),
        yaxis2=dict(
            title='yaxis2 title',
            titlefont=dict(
                color='rgb(148, 103, 189)'
            ),
            tickfont=dict(
                color='rgb(148, 103, 189)'
            ),
            overlaying='y',
            side='right',
            showgrid=False
        )
    )
    return go.Figure(data=data, layout=layout)


@app.callback(
    dash.dependencies.Output('Achse-links', 'options'),
    [dash.dependencies.Input('interval-update_Alle_Tabellen', 'n_intervals')]
)
def update_date_dropdown_left(n_clicks):
    db = sqlite3.connect("./hochstrom.db")
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    Alle_Tabellen = cursor.fetchall()
    return [{'label': Tabelle[0], 'value': Tabelle[0]} for Tabelle in Alle_Tabellen]


@app.callback(
    dash.dependencies.Output('Achse-rechts', 'options'),
    [dash.dependencies.Input('interval-update_Alle_Tabellen', 'n_intervals')]
)
def update_date_dropdown_right(n_clicks):
    db = sqlite3.connect("./hochstrom.db")
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    Alle_Tabellen = cursor.fetchall()
    return [{'label': Tabelle[0], 'value': Tabelle[0]} for Tabelle in Alle_Tabellen]


if __name__ == '__main__':
    # bevor Programm Startet hole  Alle Tabellennamen
    db = sqlite3.connect("./hochstrom.db")
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    Alle_Tabellen = cursor.fetchall()
 #   for Tabelle in Alle_Tabellen:
 #       print(Tabelle[0])
    app.run_server(debug=False, host='0.0.0.0')
