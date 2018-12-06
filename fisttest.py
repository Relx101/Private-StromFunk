# -*- coding: utf-8 -*-
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import sqlite3
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import json


with open('Config.json') as f:
    jsondata = json.load(f)
db = sqlite3.connect("./hochstrom.db")
INITqery = pd.read_sql_query("select * from abcdefabcdef;", db)
db.close()

# Globale Variablen
Alle_Tabellen = []  # Alle Tabellennamen in der DB
HauptG_linie1_daten = INITqery
HauptG_linie1_dbname = 'leer'
HauptG_linie1_reihe = 'leer'
HauptG_linie2_daten = INITqery
HauptG_linie2_dbname = 'leer'
HauptG_linie2_reihe = 'leer'
#----------------


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        dcc.Link(html.Img(src='http://www.theta-dresden.de/index_html_files/395.jpg', className='Bildrechts'), href='http://www.theta-dresden.de/', style={'float': 'right'}),
        html.H1('Hochstromregelung')
    ], className='Titeldiv'),

    html.Div([
        html.H2('Setup', style={'clear': 'both'}),
        # Configfelder
        html.Div([

            html.Div([
                html.H5('Startspannung'),
                html.Label('L1 Spannung [V]'),
                dcc.Input(value=jsondata['setup_u_start'][0], type='number', id='setup_u_start0'),
                html.Label('L2 Spannung [V]'),
                dcc.Input(value=jsondata['setup_u_start'][1], type='number', id='setup_u_start1'),
                html.Label('L3 Spannung [V]'),
                dcc.Input(value=jsondata['setup_u_start'][2], type='number', id='setup_u_start2'),
            ], className='Setupflaechendreier'),
            html.Div([
                html.H5('Strom Verhältnis'),
                html.Label('L1 '),
                dcc.Input(value=jsondata['setup_i_ratio'][0], type='number', id='setup_i_ratio0'),
                html.Label('L2'),
                dcc.Input(value=jsondata['setup_i_ratio'][1], type='number', id='setup_i_ratio1'),
                html.Label('L3'),
                dcc.Input(value=jsondata['setup_i_ratio'][2], type='number', id='setup_i_ratio2'),
            ], className='Setupflaechendreier'),
            html.Div([
                html.Label('Spannung Schrittweite [V]'),
                dcc.Input(value=jsondata['setup_u_step'], type='number', id='setup_u_step'),
                html.Label('Spannung Verhältnis '),
                dcc.Input(value=jsondata['setup_u_ratio'], type='number', id='setup_u_ratio'),
                html.Label('Maximalspannung [V]'),
                dcc.Input(value=jsondata['setup_u_max'], type='number', id='setup_u_max'),
                html.Label('Maximalstrom [A]'),
                dcc.Input(value=jsondata['setup_i_max'], type='number', id='setup_i_max'),
            ], className='Setupflaechenvierer'),

        ]),
        html.H2('Control'),
        html.Div([
            html.Div([
                html.H5('Strom soll'),
                html.Label('L1 [A]'),
                dcc.Input(value=jsondata['control_i_target'][0], type='number', id='control_i_target0'),
                html.Label('L2 [A]'),
                dcc.Input(value=jsondata['control_i_target'][1], type='number', id='control_i_target1'),
                html.Label('L3 [A]'),
                dcc.Input(value=jsondata['control_i_target'][2], type='number', id='control_i_target2'),
            ], className='Setupflaechendreier'),

            html.Div([
                html.H5('Strom diff.'),
                html.Label('L1'),
                dcc.Input(value=jsondata['control_i_delta'][0], type='number', id='control_i_delta0'),
                html.Label('L2'),
                dcc.Input(value=jsondata['control_i_delta'][1], type='number', id='control_i_delta1'),
                html.Label('L3'),
                dcc.Input(value=jsondata['control_i_delta'][2], type='number', id='control_i_delta2'),
            ], className='Setupflaechendreier')
        ]),
    ], className='Setupflaechenzweier'),

    # Achsenauswahlfelder
    html.H2('LIVE Daten', style={'clear': 'both'}),

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
        html.Div([
            html.Label('y1 min'),
            dcc.Input(value=0, type='number', id='y1_min'),
            html.Label('y1 max'),
            dcc.Input(value=2, type='number', id='y1_max'),
        ], className='yminmax'),
    ], className='Achsenwahlfeld_links'),
    html.Div([
        html.Label('Achse rechts'),
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
        html.Div([
            html.Label('y2 min'),
            dcc.Input(value=0, type='number', id='y2_min'),
            html.Label('y2 max'),
            dcc.Input(value=2, type='number', id='y2_max'),
        ], className='yminmax'),

    ], className='Achsenwahlfeld_rechts'),
    html.Div([
        html.Label('Anz. Datenpunkte'),
        dcc.Input(value=100, type='number', id='datenps_Haupt'),
    ], className='centert'),
    html.Div([
        dcc.Graph(id='maingraph')
    ], className='PrimaerGraph'),

    dcc.Interval(
        id='interval-update_Alle_Tabellen',
        interval=60 * 1000,  # in milliseconds -> alle 10 s
        n_intervals=0
    ),
    dcc.Interval(
        id='interval-update-Graph',
        interval=2 * 1000,  # in milliseconds -> alle 10 s
        n_intervals=0
    ),
    html.Div([
        html.Label('Tabelle'),
        dcc.Dropdown(
            id='Tabellen_view',
            options=[{'label': Tabelle[0], 'value': Tabelle[0]} for Tabelle in Alle_Tabellen],
        )], className='Achsenwahlfeld_links'),
    html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in INITqery.columns],
            data=[],
            editable=True
        )
    ], className='Tabelle'),
    html.Div(id='hidden_div', style={'display': 'none'}),
    html.Div(id='hidden_test', style={'display': 'none'})
], className='Hauptdiv')


@app.callback(
    dash.dependencies.Output('hidden_div', 'title'),  # Callback ohne output geht nicht oder auf einen der inputs vom callback
    [dash.dependencies.Input('setup_u_step', 'value'),
     dash.dependencies.Input('setup_u_start0', 'value'),
     dash.dependencies.Input('setup_u_start1', 'value'),
     dash.dependencies.Input('setup_u_start2', 'value'),
     dash.dependencies.Input('setup_u_ratio', 'value'),
     dash.dependencies.Input('setup_i_ratio0', 'value'),
     dash.dependencies.Input('setup_i_ratio1', 'value'),
     dash.dependencies.Input('setup_i_ratio2', 'value'),
     dash.dependencies.Input('setup_u_max', 'value'),
     dash.dependencies.Input('setup_i_max', 'value'),
     dash.dependencies.Input('control_i_target0', 'value'),
     dash.dependencies.Input('control_i_target1', 'value'),
     dash.dependencies.Input('control_i_target2', 'value'),
     dash.dependencies.Input('control_i_delta0', 'value'),
     dash.dependencies.Input('control_i_delta1', 'value'),
     dash.dependencies.Input('control_i_delta2', 'value')
     ])
def check_to_update_json(u_step,
                         u_start0,
                         u_start1,
                         u_start2,
                         u_ratio,
                         i_ratio0,
                         i_ratio1,
                         i_ratio2,
                         u_max,
                         i_max,
                         i_target0,
                         i_target1,
                         i_target2,
                         i_delta0,
                         i_delta1,
                         i_delta2):
    # Geht nicht ist Output auf eine Input Klasse ändert nicht den wert im UI
    # if float(Wert) <= -1000:
    #     print('ueberschreibe...')
    #     return 1234
    update_json_file(u_step, 'setup_u_step')
    update_json_file_indexed(u_start0, 'setup_u_start', 0)
    update_json_file_indexed(u_start1, 'setup_u_start', 1)
    update_json_file_indexed(u_start2, 'setup_u_start', 2)
    update_json_file(u_ratio, 'setup_u_ratio')
    update_json_file_indexed(i_ratio0, 'setup_i_ratio', 0)
    update_json_file_indexed(i_ratio1, 'setup_i_ratio', 1)
    update_json_file_indexed(i_ratio2, 'setup_i_ratio', 2)
    update_json_file(u_max, 'setup_u_max')
    update_json_file(i_max, 'setup_i_max')
    update_json_file_indexed(i_target0, 'control_i_target', 0)
    update_json_file_indexed(i_target1, 'control_i_target', 1)
    update_json_file_indexed(i_target2, 'control_i_target', 2)
    update_json_file_indexed(i_delta0, 'control_i_delta', 0)
    update_json_file_indexed(i_delta1, 'control_i_delta', 1)
    update_json_file_indexed(i_delta2, 'control_i_delta', 2)
    pass


def update_json_file(Wert, Name):
    if Wert != jsondata[Name]:
        jsondata[Name] = float(Wert)
        with open('Config.json', 'w') as f:
            json.dump(jsondata, f, sort_keys=False, indent=4, ensure_ascii=False)
    pass


def update_json_file_indexed(Wert, Name, index):
    if Wert != jsondata[Name][index]:
        jsondata[Name][index] = float(Wert)
        with open('Config.json', 'w') as f:
            json.dump(jsondata, f, sort_keys=False, indent=4, ensure_ascii=False)
    pass


@app.callback(
    dash.dependencies.Output('hidden_test', 'title'),
    [dash.dependencies.Input('maingraph', 'figure')])
def update_main_graph(test):
    # print(test)
    pass


@app.callback(
    dash.dependencies.Output('maingraph', 'figure'),
    [dash.dependencies.Input('interval-update-Graph', 'n_intervals'),
     dash.dependencies.Input('Achse-links', 'value'),
     dash.dependencies.Input('Achse-links-Reihe', 'value'),
     dash.dependencies.Input('Achse-rechts', 'value'),
     dash.dependencies.Input('Achse-rechts-Reihe', 'value'),
     dash.dependencies.Input('y1_min', 'value'),
     dash.dependencies.Input('y1_max', 'value'),
     dash.dependencies.Input('y2_min', 'value'),
     dash.dependencies.Input('y2_max', 'value'),
     dash.dependencies.Input('datenps_Haupt', 'value')
     ])
def update_main_graph(n_intervals, Axlinks, ReiheL, Axrechts, ReiheR, y1min, y1max, y2min, y2max, datenpunkte):
    # print(len(ReiheR))
    # print(ReiheL)
    # print('jetzt')
    global HauptG_linie1_daten
    global HauptG_linie1_dbname
    global HauptG_linie1_reihe
    if (Axlinks != None and ReiheL != None):
        startTime = time.time()  # Debug
        if(len(HauptG_linie1_daten.time) == 0 or HauptG_linie1_dbname != Axlinks or HauptG_linie1_reihe != ReiheL):  # Wenn keine Daten da sind holne neue oder ander gewünscht sind
            HauptG_linie1_dbname = Axlinks
            HauptG_linie1_reihe = ReiheL
            print("{} {} {}".format(len(HauptG_linie1_daten.time), datenpunkte, len(HauptG_linie1_daten.time) != datenpunkte))
            db = sqlite3.connect("./hochstrom.db")
            #Dataquery = pd.read_sql_query("select time, {} from {};" .format(ReiheL, Axlinks), db)
            HauptG_linie1_daten = pd.read_sql_query("select time, {} from {} order by time desc limit {};" .format(ReiheL, Axlinks, datenpunkte), db)
        else:  # Wenn daten da sind hole nur neue und hänge an
            db = sqlite3.connect("./hochstrom.db")
            print(INITqery.tail(1).time.values[0])
            Dataquery = pd.read_sql_query("select time, {} from {} where 'time' <=  '{}';".format(ReiheL, Axlinks, INITqery.tail(1).time.values[0]), db)  # schaue nach ob aktuellere Daten da sind als letzter datrenpunkt
            print(Dataquery)
            if(len(Dataquery.time) != 0):  # wenn was da ist
                print("Hänge an")
                HauptG_linie1_daten.append(Dataquery)  # haenge an
                if(len(HauptG_linie1_daten.time) >= datenpunkte):  # wenn mehr als gewuenscht
                    print("Lösche zuviel: {}".format(len(HauptG_linie1_daten.time) - datenpunkte))
                    HauptG_linie1_daten = HauptG_linie1_daten.iloc[len(HauptG_linie1_daten.time) - datenpunkte:]  # loesche die ersten
        db.close()
        xdata1 = HauptG_linie1_daten['time']
        ydata1 = HauptG_linie1_daten[ReiheL]
        # Debug
        elapsedTime = time.time() - startTime
        print('finished in {} ms'.format(int(elapsedTime * 1000)))
    else:
        xdata1 = []
        ydata1 = []
    if (Axrechts != None and ReiheR != None):
        db = sqlite3.connect("./hochstrom.db")
        #Dataquery = pd.read_sql_query("select time, {} from {};" .format(ReiheR, Axrechts), db)
        Dataquery = pd.read_sql_query("select time, {} from {} order by time desc limit {};" .format(ReiheR, Axrechts, datenpunkte), db)
        xdata2 = Dataquery['time']
        ydata2 = Dataquery[ReiheR]
        db.close()
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
        xaxis=dict(
            fixedrange=True,
        ),

        yaxis=dict(
            range=[y1min, y1max],
            title=Axlinks,
            fixedrange=True,
        ),
        yaxis2=dict(
            range=[y2min, y2max],
            title=Axrechts,
            fixedrange=True,
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
    dash.dependencies.Output('table', 'data'),
    [dash.dependencies.Input('Tabellen_view', 'value')]
)
def update_date_dropdown_right(Tabellenname):
    if(Tabellenname != None):
        db = sqlite3.connect("./hochstrom.db")
        Dataqery = pd.read_sql_query("select * from {};" .format(Tabellenname), db)
        data = Dataqery.to_dict("rows")
        db.close()
    else:
        data = []

    return data


@app.callback(
    dash.dependencies.Output('Tabellen_view', 'options'),
    [dash.dependencies.Input('interval-update_Alle_Tabellen', 'n_intervals')]
)
def update_date_dropdown_left(n_clicks):
    db = sqlite3.connect("./hochstrom.db")
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    Alle_Tabellen = cursor.fetchall()
    db.close()
    return [{'label': Tabelle[0], 'value': Tabelle[0]} for Tabelle in Alle_Tabellen]


@app.callback(
    dash.dependencies.Output('Achse-links', 'options'),
    [dash.dependencies.Input('interval-update_Alle_Tabellen', 'n_intervals')]
)
def update_date_dropdown_left(n_clicks):
    db = sqlite3.connect("./hochstrom.db")
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    Alle_Tabellen = cursor.fetchall()
    db.close()
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
    db.close()
    return [{'label': Tabelle[0], 'value': Tabelle[0]} for Tabelle in Alle_Tabellen]


if __name__ == '__main__':
    # bevor Programm Startet hole  Alle Tabellennamen
    db = sqlite3.connect("./hochstrom.db")
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    Alle_Tabellen = cursor.fetchall()
    db.close()
 #   for Tabelle in Alle_Tabellen:
 #       print(Tabelle[0])
    app.run_server(debug=True)  # , host='0.0.0.0')
