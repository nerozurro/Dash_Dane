import dash
import dash_table
from dash.dependencies import Input, Output
import dash_core_components as dcc
from dash import html
# import dash_html_components as html
import dash_bootstrap_components as dbc

import numpy as np

import pandas as pd
import plotly           #(version 4.5.4) pip install plotly==4.5.4
import plotly.express as px

from urllib.request import urlopen
import json
#import geopandas as gpd
# import geojson

#import dash_pivottable

import colorlover

# import dash_design_kit as ddk
import dash_daq as daq

# greens = colorlover.scales['5']['seq']['Greens']
# colorlover.scales['5']['seq']['Greens']


########################
######################### COLORS HIGHLIGHTS (NOT USING AFTER PUNTUATION FIX)
########################

def discrete_background_color_bins(df, n_bins=5, columns='all'):
# This provides the numbers in tables are shown highlightes,
# now 5 levels but only top3 highlighted
 bounds = [i * (1.0 / n_bins) for i in range(n_bins+1)]
 if columns == 'all':
     if 'id' in df:
         df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
         #print("PRINT NUMERIC COLUMNS ", df_numeric_columns)
     else:
         df_numeric_columns = df.select_dtypes('number')
 else:
     df_numeric_columns = df[columns]
 df_max = df_numeric_columns.max().max()
 df_min = df_numeric_columns.min().min()
 ranges = [
     ((df_max - df_min) * i) + df_min
     for i in bounds
 ]
 styles = []
 legend = []
#  print("len bounds: ", len(bounds))
#  print("bounds ", bounds)
#  print("greens full scale ", colorlover.scales[str(n_bins+4)]['seq']['Greens'])
#  print("rdylgn full scale ", colorlover.scales[str(n_bins+4)]['div']['RdYlGn'])
 for i in range(1, len(bounds)):
     min_bound = ranges[i - 1]
     max_bound = ranges[i]
     if i <= 2:
         backgroundColor = 'rgb(255,255,255)'
     else:
        #backgroundColor = colorlover.scales[str(n_bins+4)]['seq']['Greens'][2:-2][i - 1]
        backgroundColor = colorlover.scales[str(n_bins+4)]['div']['RdYlGn'][2:-2][i - 1]
        # print("BACKGROUND COLOR : ", backgroundColor)
        backgroundColor = colorlover.scales[str(n_bins+4)]['seq']['Blues'][2:-2][i - 1]
        greens = colorlover.scales[str(n_bins+4)]['seq']['Greens'][2:-2][i - 1]
        # print("GREENS COLOR : ", greens)

     color = 'black'

     for column in df_numeric_columns:
         styles.append({
             'if': {
                 'filter_query': (
                     '{{{column}}} >= {min_bound}' +
                     (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                 ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                 'column_id': column
             },
             'backgroundColor': backgroundColor,
             'color': color
         })
     legend.append(
         html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
             html.Div(
                 style={
                     'backgroundColor': backgroundColor,
                     'borderLeft': '1px rgb(50, 50, 50) solid',
                     'height': '10px'
                 }
             ),
             html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
         ])
     )

 return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))


 #########################
 ######################### FINISH COLOR HIGHLIGHTS
 #########################

################# IMPORTING DATAFRAMES #################
import vaex
print('LOADING DATA FOR COLOMBIAN MARKETS')
# Dataframe mercados nomnre ciudad lat long

df_coor_merc = vaex.read_csv('coordenadas_mercados.csv',
                usecols=['destino_ciudad_mercado', 'lat_mercado', 'lon_mercado',
                        'destino_municipio', 'lat_destino_municipio', 'lon_destino_municipio']
                )


# df_coor_merc = pd.read_csv('coordenadas_mercados.csv',
#                 usecols=['destino_ciudad_mercado', 'lat_mercado', 'lon_mercado',
#                         'destino_municipio', 'lat_destino_municipio', 'lon_destino_municipio']
#                 )
print('SUCCESFULLY LOADED COLOMBIAN MARKETS')


# Dataframe municipios dpto, mpios, lat, long, codigos
print('LOADING DATA FOR COLOMBIAN CITIES.....')
columns_municipios = ['DPTO_CCDGO', 'MPIO_CCDGO', 'MPIO_CNMBR', 'MPIO_CDPMP', 'AREA',
       'LATITUD', 'LONGITUD']

# df_municipios_properties = vaex.read_csv('municipios_properties.csv',
#                 usecols=columns_municipios,
#                 encoding="utf8",
#                 dtype={
#                     'DPTO_CCDGO': str,
#                     'MPIO_CDPMP': str,
#                     'MPIO_CCDGO': str
#                 }
#     )

df_municipios_properties = pd.read_csv('municipios_properties.csv',
                usecols=columns_municipios,
                encoding="utf8",
                dtype={
                    'DPTO_CCDGO': str,
                    'MPIO_CDPMP': str,
                    'MPIO_CCDGO': str
                }
    )
print('SUCCESFULLY LOADED COLOMBIAN CITIES')


print('LOADING SIPSA-DANE DATABASES.....')
print('...Take a cup of coffee, this might take a while...')


df = vaex.open('big_file.csv.hdf5')

# all_files = ['data_cleaned_2013_step3.csv',
#             'data_cleaned_2014_step3.csv',
#             'data_cleaned_2015_step3.csv',
#             'data_cleaned_2016_step3.csv',
#             'data_cleaned_2017_step3.csv',
#             'data_cleaned_2018_step3.csv',
#             'data_cleaned_2019_step3.csv',
#             'data_cleaned_2020_step3.csv',
#             'data_cleaned_2021_step3.csv',
#             ]

# df = pd.concat((pd.read_csv(f, encoding="utf8",
#                  parse_dates=['fecha'],
#                  dtype={
#                     'destino_ciudad_mercado': str,
#                     'procedencia_codigo_departamento': str,
#                     'procedencia_codigo_municipio': str,
#                     'procedencia_departamento'	: str,
#                     'procedencia_municipio'	: str,
#                     'grupo'	: str,
#                     'alimento': str,
#                     'destino_nombre_mercado': str,
#                     'year': str,
#                     'month':int
#                  }
#                  )
#     for f in all_files))
# print('Creating month and year.....')
# df['month'] = ['%02d' % x for x in df.month]
# df['year_month'] = df.year+ '-' + df.month

print('SUCCESFULLY LOADED SIPSA-DANE DATABASES')

# print(df.head())

# column mapper change name to show in plots and datatables
column_mapper = {'destino_ciudad_mercado':'Mercado Destino',
                'procedencia_departamento': 'Departamento de procedencia',
                'procedencia_municipio' : 'Municipio de procedencia',
                'grupo' : 'Grupo alimenticio',
                'alimento' : 'Alimento (cultivo)',
                'cantidad_kg' : 'Cantidad de alimento (Kg)',
                'procedencia_pais' : 'País de procedencia',
                'destino_ciudad' : 'Ciudad Destino',
                'day': 'Día',
                'month': 'Mes',
                'year': 'Año',
                'year_month': 'Año + Mes',
                'agua_litros' : 'Agua (Litros)',
                'tierra_hectarias': 'Tierra usada (ha)'
 }
global df_grouped
global function_agg
#df_grouped=df.copy()

df_grouped = df.groupby(['procedencia_departamento'], agg = {'Sum_agg': vaex.agg.sum('cantidad_kg')})
# df_grouped.reset_index(inplace=True)

#######################################


global df_filtrado
df_filtrado = df.copy()

# marks for slider time filter
def getMarks(start, end, divisiones=12):
    ''' Returns the marks for labeling.
        With divisiones number of marks.
    '''
    multiplier = (end-start)/divisiones # se define cada cuanto habran marcas
    result = {}
    for i in range(start, end):
        decimal, entero = math.modf(i*multiplier) # parte entera
        for key, value in dict_slider.items():
            if(key == int(entero)):
                # Append value to dict
                result[key] = value

    result[end] = dict_slider[end]
    #print(dict_slider.values()[0])
    #result[key] = value
    # print(result)
    return result


import math

# options for all selectors
Options_timeSeries_ddn = [
    {'label':'Departartamento de procedencia', 'value':'procedencia_departamento'},
    {'label':'Municipio de procedencia', 'value': 'procedencia_municipio'},
    {'label':'Grupo alimenticio', 'value': 'grupo'},
    {'label':'Alimento', 'value': 'alimento'},
    {'label':'Municipio destino', 'value': 'destino_ciudad'},
    {'label':'Mercado destino', 'value': 'destino_ciudad_mercado'}
]

Options_mapBubbles_ddn = [
    {'label':'Municipio de procedencia', 'value': 'opMuO'},
    {'label':'Municipio destino', 'value': 'opMuD'},
    {'label':'Mercado destino', 'value': 'opMeD'},
    {'label':'Conexión Municipio - Municipio', 'value': 'opMuOMuD'},
    {'label':'Conexión Municipio - Mercado', 'value': 'opMuOMeD'}
]

Option_GroupBy = [
    {'label':' ', 'value':'empty'},
    {'label':'AÑO', 'value':'year'},
    {'label':'MES', 'value':'month'},
    {'label':'DIA', 'value':'day'},
    {'label':'AÑO + MES', 'value':'year_month'},
    {'label':'Departartamento de procedencia', 'value':'procedencia_departamento'},
    {'label':'Municipio de procedencia', 'value': 'procedencia_municipio'},
    {'label':'Grupo alimenticio', 'value': 'grupo'},
    {'label':'Alimento', 'value': 'alimento'},
    {'label':'Municipio destino', 'value': 'destino_ciudad'},
    {'label':'Mercado destino', 'value': 'destino_ciudad_mercado'}
]


# options for all selectors
lista_slider = sorted(df['year_month'].unique())
dict_slider = {i:yearmonth for i, yearmonth in enumerate(lista_slider)}

Optionpais_origen = [{'label': k, 'value': k} for k in sorted(df.procedencia_pais.unique())]
Optiondptos_origen = [{'label': k, 'value': k} for k in sorted(df.procedencia_departamento.unique())]
Optionmpios_origen = [{'label': k, 'value': k} for k in sorted(df.procedencia_municipio.unique())]
Optiongrupos = [{'label': k, 'value': k} for k in sorted(df.grupo.unique())]
Optionalimentos = [{'label': k, 'value': k} for k in sorted(df.alimento.unique())]
Optiondptos_dest = [{'label': k, 'value': k} for k in sorted(df.destino_ciudad_mercado.unique())]
Optionmpios_dest = [{'label': k, 'value': k} for k in sorted(df.destino_ciudad.unique())]
Optionmercado_dest = [{'label': k, 'value': k} for k in sorted(df.destino_ciudad_mercado.unique())]
Optionmeses = [{'label': k, 'value': k} for k in sorted(df.month.unique())]


print('')
print('Dashboard creado para el análisis de Flavio Bladimir Rodriguez Muñoz <flavio.rodriguez@uexternado.edu.co>')
print('')
print('Aplicación Web por: Anibal leonardo Rojas Carrillo <anibal.leonardo.rojas@gmail.com>')
print('                    Jhon Alexis Parra Abril <jhalpaab@gmail.com>')
print('')
print('')
print('STARTING WEB APP SERVICE .....')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}
                            ]
                )



##################################################################
#########################  LAYOUT  ###############################
##################################################################

app.layout = dbc.Container([
html.Br(),
html.Br(),

    dbc.Row([  # Tittle
        dbc.Col(html.H1("CIRCUITOS ALIMENTARIOS DESTINO PROCEDENCIA",
                        className='text-center text-primary, mb-4'),
                width=12)
    ], no_gutters=False, justify='around', align='center'),

# FILTROS DROPDOWNS
    html.Br(),html.Br(),
    dbc.Row([dbc.Col( # slider filtering
            dcc.RangeSlider(id='my-slider',
                        min=0, #the first date
                    max=len(lista_slider)-1, #the last date
                    value=[len(lista_slider)-4, len(lista_slider)-1], #default: the first
                    marks=getMarks(0,len(lista_slider)-1),
                    pushable=2
                    ),width=11)
    ], no_gutters=False, justify='around', align='center'),

   html.Br(),html.Br(),html.Br(),


    dbc.Row([ # Start dropdowns selection
        # html.Br(),
        dbc.Col([

            # dbc.Row(html.H4("FILTROS", # Title for filtering
            #     className='text-center text-primary, mb-12')),

            dbc.Row([dbc.Col(html.H6("Meses",
                        className='text-center text-primary, mb-4'),xs=12, sm=12, md=12, lg=4, xl=4),
                    dbc.Col(dcc.Dropdown(
                        id='meses-dropdown',
                        options=Optionmeses,
                        value=[],
                        placeholder="vacío para seleccionar todos",
                        multi=True,
                        style=dict(
                            width='100%',
                            verticalAlign="middle"
                            )
                    ))
                    ]),
            html.Hr(),

            # dropdown select Nacional o importado
            dbc.Row([dbc.Col(html.H6("País de procedencia",
                        className='text-center text-primary, mb-4'),xs=12, sm=12, md=12, lg=4, xl=4),
                    dbc.Col(dcc.Dropdown(
                        id='pais-origen-dropdown',
                        options=Optionpais_origen,
                        value=['Colombia'],
                        placeholder="vacío para seleccionar todos",
                        multi=True,
                        style=dict(
                            width='100%',
                            verticalAlign="middle"
                            )
                    ))
                    ]),
            html.Hr(),
            # dropdown select departamento
            dbc.Row([dbc.Col(html.H6("Departamentos de procedencia",
                        className='text-center text-primary, mb-4'),xs=12, sm=12, md=12, lg=4, xl=4),
                    dbc.Col(dcc.Dropdown(
                        id='dptos-origen-dropdown',
                        options=Optiondptos_origen,
                        value=[],
                        placeholder="vacío para seleccionar todos",
                        multi=True,
                        style=dict(
                            width='100%',
                            verticalAlign="middle"
                            )
                    ))
                    ]),

            html.Hr(),
            # dropdown select municipio procedencia
            dbc.Row([dbc.Col(html.H6("Municipios de procedencia (incluye país)",
                        className='text-center text-primary, mb-4'),xs=12, sm=12, md=12, lg=4, xl=4),
                    dbc.Col(dcc.Dropdown(
                        id='mpios-origen-dropdown',
                        options=Optionmpios_origen,
                        value=[],
                        placeholder="vacío para seleccionar todos",
                        multi=True,
                        style=dict(
                            width='100%',
                            verticalAlign="middle"
                            )
                    ))
                    ]),

            html.Hr(),
            # dropdown select Grupos alimenticios
            dbc.Row([dbc.Col(html.H6("Grupos Alimenticios",
                        className='text-center text-primary, mb-4'),
                        xs=12, sm=12, md=12, lg=4, xl=4),
                    dbc.Col(dcc.Dropdown(
                        id='grupos-dropdown',
                        options=Optiongrupos,
                        value=['FRUTAS'],
                        placeholder="vacío para seleccionar todos",
                        multi=True,
                        style=dict(
                            width='100%',
                            verticalAlign="middle"
                            )
                    ))
                    ]),


            html.Hr(),
            # dropdown select alimentos
            dbc.Row([dbc.Col(html.H6("Alimentos",
                        className='text-center text-primary, mb-4'),xs=12, sm=12, md=12, lg=4, xl=4),
                    dbc.Col(dcc.Dropdown(
                        id='alimentos-dropdown',
                        options=Optionalimentos,
                        value=[],
                        placeholder="vacío para seleccionar todos",
                        multi=True,
                        style=dict(
                            width='100%',
                            verticalAlign="middle"
                            )
                    ))
                    ]),


            html.Hr(),

            # dropdown select Municipio destino
            dbc.Row([dbc.Col(html.H6("Municipio Destino",
                        className='text-center text-primary, mb-4'),xs=12, sm=12, md=12, lg=4, xl=4),
                    dbc.Col(dcc.Dropdown(
                        id='municipio-destino-dropdown',
                        options=Optionmpios_dest,
                        value=[],
                        placeholder="vacío para seleccionar todos",
                        multi=True,
                        style=dict(
                            width='100%',
                            verticalAlign="middle"
                            )
                    ))
                    ]),



            html.Hr(),
            # dropdown select Mercado destino
            dbc.Row([dbc.Col(html.H6("Mercados destino",
                        className='text-center text-primary, mb-4'),xs=12, sm=12, md=12, lg=4, xl=4),
                    dbc.Col(dcc.Dropdown(
                        id='mercado-destino-dropdown',
                        options=Optionmercado_dest,
                        value=[],
                        placeholder="vacío para seleccionar todos",
                        multi=True,
                        style=dict(
                            width='100%',
                            verticalAlign="middle"
                            )
                    ))
                    ]),

        ], #width = {'size': 5, 'offset':0}
            xs=12, sm=12, md=5, lg=4, xl=4
        ),

        dbc.Col([         # columna que contiene todos los outputs del filtrado


            # dbc.Row(html.H4("Realizar análisis por: ",
            #             className='text-center text-primary, mb-4'),
            #             no_gutters=False, justify='around', align='center'),

            # dbc.Card(
            # [
            #     dbc.RadioItems(
            #         options=[
            #             {'label': 'Cantidad Total kg', 'value': 'total_kg'},
            #             {'label': 'Cantidad Promedio (kg/viaje)', 'value': 'average_kg'},
            #             {'label': 'Número de registros', 'value': 'trips'},
            #             {'label': 'Tierra Total', 'value': 'total_land'},
            #             # {'label': 'Tierra Promedio', 'value': 'average_land'},
            #             {'label': 'Agua Total', 'value': 'total_water'},
            #             # {'label': 'Agua Promedio', 'value': 'water_average'}
            #         ],
            #         id="analize-selector",
            #         # className="btn-group",
            #         # labelClassName="btn btn-secondary",
            #         # labelCheckedClassName="active",
            #         inline=True,
            #         value='total_kg',
            #         style={'margin': 'auto'},
            #     #labelStyle={'display': 'inline-block'},
            #     #className='text-center text-primary, mb-4',
            #     ),
            # ],
            # className="radio-group",

            # ),

            dbc.Row(
            [
                dbc.RadioItems(
                    options=[
                        {'label': 'Cantidad Total kg', 'value': 'total_kg'},
                        {'label': 'Cantidad Promedio (kg/viaje)', 'value': 'average_kg'},
                        {'label': 'Número de registros', 'value': 'trips'},
                        {'label': 'Tierra Total', 'value': 'total_land'},
                        # {'label': 'Tierra Promedio', 'value': 'average_land'},
                        {'label': 'Agua Total', 'value': 'total_water'},
                        # {'label': 'Agua Promedio', 'value': 'water_average'}
                    ],
                    id="analize-selector",
                    # className="btn-group",
                    # labelClassName="btn btn-secondary",
                    # labelCheckedClassName="active",
                    inline=True,
                    value='total_kg',
                    style={'margin': 'auto'},
                #labelStyle={'display': 'inline-block'},
                #className='text-center text-primary, mb-4',
                ),
            ],
            no_gutters=False, justify='between', align='center'

            ),
            html.Br(),
            html.Br(),
            html.Hr(),
            html.Br(),


            # Tittle quantity filtering output
            # dbc.Row(html.H4("La selección hecha contiene: ",
            #             className='text-center text-primary, mb-4'),
            #             no_gutters=False, justify='around', align='center'),

            html.Br(),html.Br(),
            # slider filtering output
            dbc.Row([ # Fila que contiene todos los outputs del filtrado dentro de la columna derecha

                dbc.Col([
                        dbc.Row([
                            dbc.Col([dbc.Row(html.P('Periodo'),
                                # style={'textDecoration': 'underline'}),
                                no_gutters=False, justify='around', align='top'),
                            dbc.Row(html.H3(id='output-container-range-slider'),
                                 no_gutters=False, justify='around', align='bottom')])
                            ],
                            # className='text-center text-primary, mb-4'),
                            no_gutters=False, justify='around', align='top',
                            style=dict(
                                width='100%',
                                verticalAlign="middle")
                            )
                    ]),

                dbc.Col([
                        dbc.Row([
                            dbc.Col([dbc.Row(html.P('Departamentos de procedencia'),
                                # style={'textDecoration': 'underline'}),
                                no_gutters=False, justify='around', align='top'),
                            dbc.Row(html.H3(id='output-container-dptos-origen'),
                                 no_gutters=False, justify='around', align='top')])
                            ],
                            # className='text-center text-primary, mb-4'),
                            no_gutters=False, justify='around', align='top',
                            style=dict(
                                width='100%',
                                verticalAlign="middle")
                            )
                    ]),


                dbc.Col([
                        dbc.Row([
                            dbc.Col([dbc.Row(html.P('Municipios de procedencia'),
                                # style={'textDecoration': 'underline'}),
                                no_gutters=False, justify='around', align='top'),
                            dbc.Row(html.H3(id='output-container-mpios-origen'),
                                 no_gutters=False, justify='around', align='top')])
                            ],
                            # className='text-center text-primary, mb-4'),
                            no_gutters=False, justify='around', align='top',
                            style=dict(
                                width='100%',
                                verticalAlign="middle")
                            )
                    ]),
                ],
            no_gutters=False, justify='around', align='top'
            ),
            html.Br(),
            html.Br(),

            dbc.Row([

                dbc.Col([
                        dbc.Row([
                            dbc.Col([dbc.Row(html.P('Grupos alimenticios'),
                                #style={'textDecoration': 'underline'}),
                                no_gutters=False, justify='around', align='top'),
                            dbc.Row(html.H3(id='output-container-grupos'),
                                 no_gutters=False, justify='around', align='top')])
                            ],
                            # className='text-center text-primary, mb-4'),
                            no_gutters=False, justify='around', align='top',
                            style=dict(
                                width='100%',
                                verticalAlign="middle")
                            )
                    ]),

                dbc.Col([
                        dbc.Row([
                            dbc.Col([dbc.Row(html.P('Alimentos'),
                                # style={'textDecoration': 'underline'}),
                                no_gutters=False, justify='around', align='top'),
                            dbc.Row(html.H3(id='output-container-alimentos'),
                                 no_gutters=False, justify='around', align='top')])
                            ],
                            # className='text-center text-primary, mb-4'),
                            no_gutters=False, justify='around', align='top',
                            style=dict(
                                width='100%',
                                verticalAlign="middle")
                            )
                    ]),


                dbc.Col([
                        dbc.Row([
                            dbc.Col([dbc.Row(html.P('Municipios destino'),
                                # style={'textDecoration': 'underline'}),
                                no_gutters=False, justify='around', align='top'),
                            dbc.Row(html.H3(id='output-container-municipio-destino'),
                                 no_gutters=False, justify='around', align='top')])
                            ],
                            # className='text-center text-primary, mb-4'),
                            no_gutters=False, justify='around', align='top',
                            style=dict(
                                width='100%',
                                verticalAlign="middle")
                            )
                    ]),

                dbc.Col([
                        dbc.Row([
                            dbc.Col([dbc.Row(html.P('Mercados destino'),
                                # style={'textDecoration': 'underline'}),
                                no_gutters=False, justify='around', align='top'),
                            dbc.Row(html.H3(id='output-container-mercados-destino'),
                                 no_gutters=False, justify='around', align='top')])
                            ],
                            # className='text-center text-primary, mb-4'),
                            no_gutters=False, justify='around', align='top',
                            style=dict(
                                width='100%',
                                verticalAlign="middle")
                            )
                    ]),

                # dbc.Col([
                #         dbc.Row([
                #             dbc.Col([dbc.Row(html.P('TOTAL: '),
                #                 # style={'textDecoration': 'underline'}),
                #                 no_gutters=False, justify='around', align='top'),
                #             dbc.Row(html.H3(id='output-container-analizer'),
                #                  no_gutters=False, justify='around', align='top')])
                #             ],
                #             # className='text-center text-primary, mb-4'),
                #             no_gutters=False, justify='around', align='top',
                #             style=dict(
                #                 width='100%',
                #                 verticalAlign="middle")
                #             )
                #     ]),




            ],
            no_gutters=False, justify='around', align='top'
            ),

        dbc.Row([

            dbc.Col([
                        dbc.Row([
                            dbc.Col([dbc.Row(html.P('TOTAL: '),
                                # style={'textDecoration': 'underline'}),
                                no_gutters=False, justify='around', align='top'),
                            dbc.Row(html.H2(id='output-container-analizer'),
                                 no_gutters=False, justify='around', align='top')])
                            ],
                            # className='text-center text-primary, mb-4'),
                            no_gutters=False, justify='around', align='top',
                            style=dict(
                                width='100%',
                                verticalAlign="middle")
                            )
                    ]),
            ],
            no_gutters=False, justify='around', align='top'
            ),

            dbc.Row([
                html.Div(id='output-container-range-slider2')
            ]),


        ], xs=11, sm=11, md=6, lg=7, xl=7),


 # Acaba sistema de filtros
 # Inicia Datatable Groupby

    ], no_gutters=False, justify='around', align='center'),

#     ACABA FILTROS

##########################################################################

# INICIA SERIE DE TIEMPO
    html.Br(),
    html.Hr(),
    html.Br(),



    dbc.Row([  # Tittle
        dbc.Col(html.H3("SERIES DE TIEMPO GRUPO ALIMENTO",
                        className='text-center text-primary, mb-4'),
                width=12)
    ], no_gutters=False, justify='around', align='center'),

    dbc.Row(
        dbc.Col(dcc.Dropdown(
            id='time-series-dropdown',
            options=Options_timeSeries_ddn,
            value='grupo',
                        #placeholder="vacío para seleccionar todos",
            multi=False,
            clearable=False,
            style=dict(
                width='50%',
                verticalAlign="middle"
            )
        ), xs=10, sm=10, md=10, lg=10, xl=10)
        ,no_gutters=False, justify='around', align='left'
    ),

    dbc.Row(
        dbc.Col(dcc.Graph(id='time-series-fig'), xs=10, sm=10, md=10, lg=10, xl=10)
    ,no_gutters=False, justify='around', align='center'
    ),


# ACABA SERIE DE TIEMPO

######################################################################################

# INICIA MAPA
    html.Br(),
    html.Hr(),
    html.Br(),


    dbc.Row([  # Tittle
        dbc.Col(html.H3("MAPA PROCEDENCIA DESTINO",
                        className='text-center text-primary, mb-4'),
                width=12)
    ], no_gutters=False, justify='around', align='center'),

    html.Br(),

    dbc.Row([

        html.Br(),

        dbc.Col(dcc.Dropdown(
            id='mapBubbles-dropdown',
            options=Options_mapBubbles_ddn,
            value='opMeD',
                        #placeholder="vacío para seleccionar todos",
            multi=False,
            clearable=False,
            style=dict(
                width='50%',
                verticalAlign="middle"
            )
        ), xs=10, sm=6, md=10, lg=10, xl=6),

        html.Br(),

        # dbc.Col(
        #     dbc.Button(
        #     "Mostrar Conexiones",
        #     color="primary",
        #     id="map-lines",
        #     className="mr-1",
        #     n_clicks=0,
        # ), xs=10, sm=6, md=4, lg=4, xl=4),

    ]
    ,no_gutters=False, justify='around', align='left'
    ),
    html.Br(),
    html.Br(),

    dbc.Row(
        dbc.Col(
            dcc.Graph(id='mapa-Colombia', figure={})
            , xs=11, sm=11, md=11, lg=11, xl=6)
    ,no_gutters=False, justify='around', align='center'
    ),




# ACABA MAPA

#############################################################################



# INICIA GROUP BY TABLE
    html.Br(),
    html.Br(),
    html.Hr(),
    html.Br(),
    html.Br(),

    dbc.Row([  # Tittle
        dbc.Col(html.H3("TABLAS GRUPO ALIMENTO",
                        className='text-center text-primary, mb-4'),
                width=12)
    ], no_gutters=False, justify='around', align='center'),

    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='agrupador-dropdown-1',
            options=Option_GroupBy,
            value='grupo',
            multi = False,
            clearable=False,
            style=dict(
                width='100%',
                verticalAlign="middle"
            )
        ), xs=10, sm=7, md=5, lg=3, xl=2),

        dbc.Col(dcc.Dropdown(
            id='agrupador-dropdown-2',
            options=Option_GroupBy,
            value='empty',
            multi = False,
            clearable=False,
            style=dict(
                width='100%',
                verticalAlign="middle"
            )
        ), xs=10, sm=7, md=5, lg=3, xl=2),

        dbc.Col(dcc.Dropdown(
            id='agrupador-dropdown-3',
            options=Option_GroupBy,
            value='empty',
            multi = False,
            clearable=False,
            style=dict(
                width='100%',
                verticalAlign="middle"
            )
        ), xs=10, sm=7, md=5, lg=3, xl=2),

        dbc.Col(dcc.Dropdown(
            id='agrupador-dropdown-4',
            options=Option_GroupBy,
            value='empty',
            multi = False,
            clearable=False,
            style=dict(
                width='100%',
                verticalAlign="middle"
            )
        ), xs=10, sm=7, md=5, lg=3, xl=2)]
         ,no_gutters=False, justify='center', align='center'),

        dbc.Row([

            dbc.Col(
                dcc.Graph(id='bar-group-fig', figure={})
                , xs=12, sm=12, md=11, lg=11, xl=10),
        ],no_gutters=False, justify='center', align='center'),




        # ], #width = {'size': 5}
        #     xs=12, sm=12, md=8, lg=10, xl=10
        #  ),

        # ,no_gutters=False, justify='center', align='center'),



    html.Br(),
    html.Br(),



    dbc.Row([

        dbc.Col([
            dash_table.DataTable(
                id='datatable_id',
                #data=df_grouped.to_dict('records'),
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": False} for i in df_grouped.columns
                ],
                editable=False,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                row_selectable="multi",
                row_deletable=False,
                selected_rows=[],
                page_action="native",  #
                page_current= 0,  #
                page_size= 15,  #
                #style_data_conditional = styles,

                # page_action='none',
                # style_cell={
                # 'whiteSpace': 'normal'
                # },
                # fixed_rows={ 'headers': True, 'data': 0 },
                # virtualization=False,



                # style_cell_conditional=[
                #     {'if': {'column_id': 'procedencia_departamento'},
                #     'width': '40%', 'textAlign': 'left'},
                #     {'if': {'column_id': 'grupo'},
                #     'width': '30%', 'textAlign': 'left'},
                # ],
            ),

            html.Br(),
            html.Button("Download CSV", id="btn_csv"),
            dcc.Download(id="download-dataframe-csv")
        ], xs=12, sm=12, md=12, lg=12, xl=11
        ),
    ], no_gutters=False, justify='around', align='center'
    ),

    html.Br(),
    html.Br(),

        # dbc.Col(
        #     dbc.Row([html.Button("Download CSV", id="btn_csv"),
        #     dcc.Download(id="download-dataframe-csv")], no_gutters=False, justify='around', align='center'),
        #     xs=12, sm=12, md=12, lg=12, xl=12)]


    # ,no_gutters=False, justify='around', align='center'),





# ACABAN GROUPBY TABLE

######################################################################################

#############################################################################



# INICIA PIVOT TABLE
    html.Hr(),
    html.Br(),
    dbc.Row([  # Tittle
        dbc.Col(html.H3("TABLA DINÁMICA",
                        className='text-center text-primary, mb-4'),
                width=12)
    ], no_gutters=False, justify='around', align='center'),

    daq.BooleanSwitch(
        id='daq-pivot-switch',
        # label=['No Actualizar', 'Actualizar'],
        # style={'width': '250px', 'margin': 'auto'},
        on=False,
        label="Actualizar",
        labelPosition="top"
    ),

    html.Br(),
    html.Br(),

    dbc.Row([


        dbc.Col(dcc.Dropdown(
            id='pivot-dropdown-2',
            options=Option_GroupBy,
            value='year',
            multi = False,
            clearable=False,
            style=dict(
                width='100%',
                verticalAlign="middle"
            )
        ), xs=10, sm=6, md=4, lg=2, xl=2)]

        ,no_gutters=False, justify='center', align='center'),


    dbc.Row([

        dbc.Col(dcc.Dropdown(
            id='pivot-dropdown-1',
            options=Option_GroupBy,
            value='grupo',
            multi = False,
            clearable=False,
            style=dict(
                width='100%',
                verticalAlign="middle"
            )
        ), xs=10, sm=6, md=3, lg=2, xl=2),

        dbc.Col([

            dcc.Graph(id='bar-pivot-fig', figure={})




        ], #width = {'size': 5}
            xs=12, sm=12, md=8, lg=10, xl=10
         ),


    ], no_gutters=False, justify='around', align='center'
    ),

    html.Br(),

    dbc.Row([



        dbc.Col([

            dash_table.DataTable(
                id='pivot-table-id',
                #data=df_grouped.to_dict('records'),
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": False} for i in df_grouped.columns
                ],
                # editable=False,
                # filter_action="native",
                # sort_action="native",
                # sort_mode="multi",
                # row_selectable="multi",
                # row_deletable=False,
                # selected_rows=[],
                # page_action="native",  #
                #page_current= 0,  #
                #page_size= 15,  #

            ),
            html.Br(),
            html.Button("Download CSV", id="btn2_csv"),
            dcc.Download(id="download-pivot-csv")
            # dcc.Graph(id='bar-pivot-fig', figure={})
        ], xs=12, sm=12, md=12, lg=12, xl=11
        ),

    ], no_gutters=False, justify='around', align='center'
    ),



# ACABAN GROUPBY TABLE

######################################################################################

######################################################################################

# INICIA DIAGRAMA DE SINKEY

    html.Div(id='display-selected-values'),
    html.Hr(),
    html.Div(id='display-selected-alimentos'),
    html.Hr(),
    html.Div(id='display-selected-alimentos2'),
    html.Hr(),
    html.Div(id='dummy_display')
], fluid=True)

@app.callback(  # Callback actualizar sistema de filtros y mostrar selecciones
    dash.dependencies.Output('meses-dropdown', 'options'),
    dash.dependencies.Output('pais-origen-dropdown', 'options'),
    dash.dependencies.Output('dptos-origen-dropdown', 'options'),
    dash.dependencies.Output('mpios-origen-dropdown', 'options'),
    dash.dependencies.Output('grupos-dropdown', 'options'),
    dash.dependencies.Output('alimentos-dropdown', 'options'),
    dash.dependencies.Output('municipio-destino-dropdown', 'options'),
    dash.dependencies.Output('mercado-destino-dropdown', 'options'),
    dash.dependencies.Output('output-container-range-slider', 'children'),
    # dash.dependencies.Output('output-container-range-slider2', 'children'),
    dash.dependencies.Output('output-container-dptos-origen', 'children'),
    dash.dependencies.Output('output-container-mpios-origen', 'children'),
    dash.dependencies.Output('output-container-grupos', 'children'),
    dash.dependencies.Output('output-container-alimentos', 'children'),
    dash.dependencies.Output('output-container-municipio-destino', 'children'),
    dash.dependencies.Output('output-container-mercados-destino', 'children'),
    dash.dependencies.Output('output-container-analizer', 'children'),
    dash.dependencies.Output('mapBubbles-dropdown', 'value'),
    [dash.dependencies.Input('my-slider', 'value'),
     dash.dependencies.Input('meses-dropdown', 'value'),
     dash.dependencies.Input('pais-origen-dropdown', 'value'),
     dash.dependencies.Input('dptos-origen-dropdown', 'value'),
     dash.dependencies.Input('mpios-origen-dropdown', 'value'),
     dash.dependencies.Input('grupos-dropdown', 'value'),
     dash.dependencies.Input('alimentos-dropdown', 'value'),
     dash.dependencies.Input('municipio-destino-dropdown', 'value'),
     dash.dependencies.Input('mercado-destino-dropdown', 'value'),
     dash.dependencies.Input("analize-selector", 'value')
     ])
    #  options=[
    #                     {'label': 'Total kg', 'value': 'total_kg'},
    #                     {'label': 'Promedio kg', 'value': 'average_kg'},
    #                     {'label': 'Viajes', 'value': 'trips'},
    #                     {'label': 'Tierra', 'value': 'total_land'},
    #                     {'label': 'Tierra Promedio', 'value': 'average_land'}
                        # {'label': 'Agua', 'value': 'total_water'}
                        # {'label': 'Agua Promedio', 'value': 'water_average'}
    #                 ],
def update_filtered_dataframe(dates, mesesO, paisO, dptoO, mpioO, grupos, alimentos, mpioD, mercD, analizer):
    global function_agg
    global column_agg
    global pivotfunc
    global plot_label1
    global text_analizer

    print('Updating filters....')

    if analizer == 'total_kg':
        function_agg = vaex.agg.sum('cantidad_kg')
        pivotfunc=np.sum
        column_agg = 'cantidad_kg'
        pre_text = 'Total (kg)'
        post_text = ' kg de alimento'
        text_analizer = "Totales kg de alimentos"
        plot_label1 = 'Cantidad Total (kg)'

    elif analizer == 'average_kg':
        function_agg = vaex.agg.mean('cantidad_kg')
        pivotfunc=np.mean
        post_text = ' kg/viaje de alimento'
        column_agg = 'cantidad_kg'
        text_analizer = "Promedio kg de alimentos por registro"
        plot_label1 = 'Promedio Transportado (kg/registro)'

    elif analizer == 'trips':
        function_agg = vaex.agg.count('cantidad_kg')
        pivotfunc= 'count'
        post_text = ' registros'
        column_agg = 'cantidad_kg'
        text_analizer = "Cantidad de viajes o registros"
        plot_label1 = 'Cantidad de registros'

    elif analizer == 'total_land':
        function_agg = vaex.agg.sum('tierra_hectarias')
        pivotfunc=np.sum
        post_text = ' Hectáreas'
        column_agg = 'tierra_hectarias'
        text_analizer = "Total hectáreas utilizadas"
        plot_label1 = 'Total Tierra (ha)'

    elif analizer == 'average_land':
        function_agg = vaex.agg.mean('tierra_hectarias')
        pivotfunc=np.mean
        column_agg = 'tierra_hectarias'
        text_analizer = "Promedio tierras alimentos"
        plot_label1 = 'Promedio Tierra (ha/registro)'

    elif analizer == 'total_water':
        function_agg = vaex.agg.sum('agua_litros')
        pivotfunc=np.sum
        column_agg = 'agua_litros'
        post_text = ' Litros de Agua'
        text_analizer = "Total Litros de agua"
        plot_label1 = 'Total Agua (L)'

    elif analizer == 'water_average':
        function_agg = vaex.agg.mean('agua_litros')
        pivotfunc=np.mean
        column_agg = 'agua_litros'
        text_analizer = "Promedio Litros de agua por registro"
        plot_label1 = 'Promedio Agua (L/registro)'


    global df_grouped
    global df_filtrado
    # print("Entramos al filtrado COMPLETO")
    df_filtrado = df.copy()

    months_selected = [dict_slider[x] for x in range(dates[0], dates[1]+1)]
    df_filtrado=df_filtrado[df_filtrado.year_month.isin(months_selected)]

    list_meses_unique = sorted(df_filtrado.month.unique())
    Optionmeses = [{'label': k, 'value': k} for k in list_meses_unique]

    if len(mesesO) != 0:
        df_aux_filtrado = df_filtrado[df_filtrado.month.isin(mesesO)]
        if len(df_aux_filtrado) != 0:
            df_filtrado= df_aux_filtrado
    df_aux_filtrado = []
    list_procPais_unique = sorted(df_filtrado.procedencia_pais.unique())
    OptionPais_origen = [{'label': k, 'value': k} for k in list_procPais_unique]

    if len(paisO) != 0:
        df_aux_filtrado = df_filtrado[df_filtrado.procedencia_pais.isin(paisO)]
        if len(df_aux_filtrado) != 0:
            df_filtrado = df_aux_filtrado
    df_aux_filtrado = []
    list_procDpto_unique = sorted(df_filtrado.procedencia_departamento.unique())
    OptionDpto_origen = [{'label': k, 'value': k} for k in list_procDpto_unique]

    if len(dptoO) != 0:
        df_aux_filtrado = df_filtrado[df_filtrado.procedencia_departamento.isin(dptoO)]
        if len(df_aux_filtrado) != 0:
            df_filtrado=df_aux_filtrado
    df_aux_filtrado=[]
    list_procMpio_unique = sorted(df_filtrado.procedencia_municipio.unique())
    Optionmpios_origen = [{'label': k, 'value': k} for k in list_procMpio_unique]

    if len(mpioO) != 0:
        df_aux_filtrado = df_filtrado[df_filtrado.procedencia_municipio.isin(mpioO)]
        if len(df_aux_filtrado) != 0:
            df_filtrado=df_aux_filtrado
    df_aux_filtrado=[]
    list_grupo_unique = sorted(df_filtrado.grupo.unique())
    Optiongrupos = [{'label': k, 'value': k} for k in list_grupo_unique]

    if len(grupos) != 0:
        df_aux_filtrado = df_filtrado[df_filtrado.grupo.isin(grupos)]
        if len(df_aux_filtrado) != 0:
            df_filtrado= df_aux_filtrado

    list_alimento_unique = sorted(df_filtrado.alimento.unique())
    Optionalimentos = [{'label': k, 'value': k} for k in list_alimento_unique]

    if len(alimentos) != 0:
        df_aux_filtrado = df_filtrado[df_filtrado.alimento.isin(alimentos)]
        if len(df_aux_filtrado) != 0:
            df_filtrado=df_aux_filtrado

    list_munDestino_unique = sorted(df_filtrado.destino_ciudad.unique())
    Optionmpios_destino = [{'label': k, 'value': k} for k in list_munDestino_unique]
    #if len(dptoD) != 0:
    #    df_filtrado=df_filtrado[df_filtrado.grupo.isin(dptoD)]
    if len(mpioD) != 0:
        df_aux_filtrado = df_filtrado[df_filtrado.destino_ciudad.isin(mpioD)]
        if len (df_aux_filtrado) != 0:
            df_filtrado=df_aux_filtrado

    list_mercDestino_unique = sorted(df_filtrado.destino_ciudad_mercado.unique())
    Optionmercados = [{'label': k, 'value': k} for k in list_mercDestino_unique]

    if len(mercD) != 0:
        df_aux_filtrado = df_filtrado[df_filtrado.destino_ciudad_mercado.isin(mercD)]
        if len (df_aux_filtrado) != 0:
            df_filtrado= df_aux_filtrado

    list_procDpto_unique = sorted(df_filtrado.procedencia_departamento.unique())
    list_procMpio_unique = sorted(df_filtrado.procedencia_municipio.unique())
    list_grupo_unique = sorted(df_filtrado.grupo.unique())
    list_alimento_unique = sorted(df_filtrado.alimento.unique())
    list_munDestino_unique = sorted(df_filtrado.destino_ciudad.unique())
    list_mercDestino_unique = sorted(df_filtrado.destino_ciudad_mercado.unique())

    if analizer == 'average_kg':
        total = df_filtrado[column_agg].mean()
    elif analizer == 'trips':
        total = df_filtrado[column_agg].count()
    else:
        total = df_filtrado[column_agg].sum()

    mapa_opcion_default = 'opMeD'
    print('Filters updated!')
    print('')
    return [Optionmeses, OptionPais_origen, OptionDpto_origen, Optionmpios_origen, Optiongrupos, Optionalimentos, Optionmpios_destino, Optionmercados,
            '{} - {}'.format(dict_slider[dates[0]], dict_slider[dates[1]]),
            # 'Todos los meses son "{}"'.format(months_selected),
            # '{:.0f} {}'.format(total,post_text),
            len(list_procDpto_unique),
            len(list_procMpio_unique),
            len(list_grupo_unique),
            len(list_alimento_unique),
            len(list_munDestino_unique),
            len(list_mercDestino_unique),
            '{:,.0f} {}'.format(total,post_text),
            mapa_opcion_default
            ]



@app.callback( # update time series chart
    dash.dependencies.Output('time-series-fig', 'figure'),
    [dash.dependencies.Input('time-series-dropdown', 'value'),
    dash.dependencies.Input('output-container-range-slider', 'children'),
    dash.dependencies.Input('output-container-dptos-origen', 'children'),
    dash.dependencies.Input('output-container-mpios-origen', 'children'),
    dash.dependencies.Input('output-container-grupos', 'children'),
    dash.dependencies.Input('output-container-alimentos', 'children'),
    dash.dependencies.Input('output-container-mercados-destino', 'children'),
    ])
def update_time_series(time_series_selection, sl, dpt, mpio, gr, alim, merD):
    print('')
    print('Calculating Time-Series Data...')
    columns_plot_time=['year_month', time_series_selection]
    df_grouped_time = df_filtrado.groupby(time_series_selection, agg = {column_agg: function_agg})

    df_grouped_time = df_grouped_time.sort([column_agg], ascending=False)

    # df_grouped_time.reset_index(inplace=True)

    top_list = df_grouped_time[time_series_selection][0:10].unique()
    df_grouped_time = df_filtrado[df_filtrado[time_series_selection].isin(top_list)]
    # print(df_grouped_time.head(20))
    df_grouped_time = df_grouped_time.groupby(columns_plot_time, agg = {column_agg: function_agg})
    df_grouped_time = df_grouped_time.sort(['year_month'], ascending=True)

    #print(df_grouped_time.sort_values(by='cantidad_kg', ascending=False))
    #df_grouped_time.reset_index(inplace=True)
    print(df_grouped_time.head(20))
    print('Time-series succesfully updated')
    print('Rendering Time-series chart')
    print('')
    # df_grouped_time.
    df_grouped_time = df_grouped_time.to_pandas_df()
    time_chart = px.line(
        data_frame=df_grouped_time,
        x='year_month',
        y=column_agg,
        color=time_series_selection,
        title = text_analizer,
        labels={'year_month':'Año', column_agg:plot_label1},
        )
    time_chart.update_layout(uirevision='foo')

    return(time_chart)


@app.callback( #update map bubbles
    dash.dependencies.Output('mapa-Colombia', 'figure'),
    [dash.dependencies.Input('mapBubbles-dropdown', 'value'),
    dash.dependencies.Input('output-container-range-slider', 'children'),
    dash.dependencies.Input('output-container-dptos-origen', 'children'),
    dash.dependencies.Input('output-container-mpios-origen', 'children'),
    dash.dependencies.Input('output-container-grupos', 'children'),
    dash.dependencies.Input('output-container-alimentos', 'children'),
    dash.dependencies.Input('output-container-mercados-destino', 'children'),
    ])

def update_map(map_bubble_selection, sl, dpt, mpio, gr, alim, merD):
    #print(df_mapa.procedencia_codigo_municipio.unique())
    #print(df_municipios_properties.head(6))
    df_mapa=[]
    df_mapa2=[]
    df_coor_merc_copy = df_coor_merc.copy()
    df_municipios_properties_copy = df_municipios_properties.copy()

    print('Calculating geographical data...')
    if  (map_bubble_selection=='opMuO'): #municipio origen
        columns_procedencia = ['procedencia_codigo_municipio', 'procedencia_municipio']
        columns_destino = []
        origen = 1
        destino=0

        df_mapa = df_filtrado.groupby(columns_procedencia, agg = {column_agg: function_agg})
        #df_mapa.reset_index(inplace=True)
        df_mapa = df_mapa.to_pandas_df()
        df_mapa = pd.merge(df_mapa, df_municipios_properties, how="left", left_on=["procedencia_codigo_municipio"], right_on=["MPIO_CDPMP"])
        map_latitud = "LATITUD"
        map_longitud = "LONGITUD"
        map_hoover = "MPIO_CNMBR"
        df_mapa = df_mapa.assign(Ubicacion="Procedencia")
        df_mapa = df_mapa[[map_latitud, map_longitud, map_hoover, 'Ubicacion', column_agg]]

    if  (map_bubble_selection=='opMuD'): #municipio Destino
        columns_procedencia = []
        columns_destino = ['destino_municipio', "lat_destino_municipio", "lon_destino_municipio"]
        origen = 0
        destino=1

        # df_mapa = pd.merge(df_filtrado, df_coor_merc, how="left", left_on=['destino_ciudad_mercado'], right_on=['destino_ciudad_mercado'])
        # df_mapa.reset_index(inplace=True)
        # df_mapa = df_mapa.groupby(columns_destino)[[column_agg]].agg(function_agg)

        df_mapa = df_filtrado.join(df_coor_merc_copy, how="left", on='destino_ciudad_mercado')
        df_mapa = df_mapa.groupby(columns_destino, agg = {column_agg: function_agg})

        #df_mapa = pd.merge(df_mapa, df_coor_merc, how="left", left_on=['destino_ciudad_mercado'], right_on=['destino_ciudad_mercado'])
        #df_mapa = pd.merge(df_mapa, df_municipios_properties, how="left", left_on=["destino_municipio"], right_on=["MPIO_CDPMP"])
        #df_mapa.reset_index(inplace=True)
        map_latitud = "lat_destino_municipio"
        map_longitud = "lon_destino_municipio"
        map_hoover = "destino_municipio"
        df_mapa = df_mapa.to_pandas_df()
        df_mapa = df_mapa.assign(Ubicacion="Destino")
        df_mapa = df_mapa[[map_latitud, map_longitud, map_hoover, 'Ubicacion', column_agg]]



    if  (map_bubble_selection=='opMeD'): #  MERCADO DESTINO
        columns_procedencia = []
        columns_destino = ['destino_ciudad_mercado']
        origen = 0
        destino=1
        df_mapa = df_filtrado.groupby(columns_destino, agg = {column_agg: function_agg})
        # df_mapa.reset_index(inplace=True)
        # df_mapa = pd.merge(df_mapa, df_coor_merc, how="left", left_on=['destino_ciudad_mercado'], right_on=['destino_ciudad_mercado'])
        df_mapa = df_mapa.join(df_coor_merc_copy, how="left", on='destino_ciudad_mercado')
        map_latitud = "lat_mercado"
        map_longitud = "lon_mercado"
        map_hoover = "destino_ciudad_mercado"
        df_mapa = df_mapa.to_pandas_df()
        df_mapa = df_mapa.assign(Ubicacion="Destino")
        df_mapa = df_mapa[[map_latitud, map_longitud, map_hoover, 'Ubicacion', column_agg]]

    if  (map_bubble_selection=='opMuOMuD'): # Municipio origen a Municipio Destino
        columns_procedencia = ['procedencia_codigo_municipio', 'procedencia_municipio']
        columns_destino = ['destino_municipio', "lat_destino_municipio", "lon_destino_municipio"]
        origen = 1
        destino=1

        df_mapa = df_filtrado.groupby(columns_procedencia, agg = {column_agg: function_agg})
        # df_mapa.reset_index(inplace=True)
        df_mapa = df_mapa.to_pandas_df()
        # df_municipios_properties.rename('MPIO_CDPMP', 'procedencia_codigo_municipio')
        df_mapa = pd.merge(df_mapa, df_municipios_properties, how="left", left_on=["procedencia_codigo_municipio"], right_on=["MPIO_CDPMP"])
        # df_mapa = df_mapa.join(df_municipios_properties, how="left", on='procedencia_codigo_municipio')
        # df_mapa = df_mapa.to_pandas_df()
        df_mapa = df_mapa.assign(Ubicacion="Procedencia")
        df_mapa.rename(columns={'procedencia_municipio': 'nombre'}, inplace=True)
        df_mapa = df_mapa[['nombre', column_agg, 'LATITUD', 'LONGITUD', 'Ubicacion']]
        # df_mapa2 = pd.merge(df_filtrado, df_coor_merc, how="left", left_on=['destino_ciudad_mercado'], right_on=['destino_ciudad_mercado'])
        df_mapa2 = df_filtrado.join(df_coor_merc_copy, how="left", on='destino_ciudad_mercado')
        # df_mapa2 = df_mapa2[['destino_municipio', "lat_destino_municipio", "lon_destino_municipio", column_agg]]
        df_mapa2 = df_mapa2.groupby(columns_destino, agg = {column_agg: function_agg})
        # df_mapa2.reset_index(inplace=True)
        df_mapa2 = df_mapa2.to_pandas_df()
        df_mapa2.rename(columns={'destino_municipio': 'nombre', "lat_destino_municipio":'LATITUD', "lon_destino_municipio":"LONGITUD" }, inplace=True)
        df_mapa2 = df_mapa2.assign(Ubicacion="Destino")

        map_latitud = "LATITUD"
        map_longitud = "LONGITUD"
        map_hoover = "nombre"
        df_mapa2 = df_mapa2[[map_hoover, column_agg, map_latitud, map_longitud, 'Ubicacion']]

        frames = [df_mapa, df_mapa2]
        df_mapa = pd.concat(frames)
        df_mapa.reset_index(inplace=True)
        df_mapa2=[]

        # df_mapa2 = pd.merge(df_filtrado, df_coor_merc, how="left", left_on=['destino_ciudad_mercado'], right_on=['destino_ciudad_mercado'])
        # df_mapa2.reset_index(inplace=True)
        df_mapa2 = df_filtrado.join(df_coor_merc_copy, how="left", on='destino_ciudad_mercado')
        df_mapa2 = df_mapa2.to_pandas_df()
        columns_df_mapa2_lines = ['procedencia_codigo_municipio', 'procedencia_municipio', 'destino_municipio', "lat_destino_municipio", "lon_destino_municipio"]
        df_mapa2 = df_mapa2[columns_df_mapa2_lines]
        df_mapa2 = df_mapa2.groupby(columns_df_mapa2_lines).count()
        df_mapa2.reset_index(inplace=True)
        df_mapa2 = pd.merge(df_mapa2, df_municipios_properties, how="left", left_on=["procedencia_codigo_municipio"], right_on=["MPIO_CDPMP"])
        #df_mapa2 = pd.merge(df_mapa2, df_coor_merc, how="left", left_on=["destino_ciudad_mercado"], right_on=["destino_ciudad_mercado"])
        df_mapa2 = df_mapa2.dropna(subset=['MPIO_CDPMP'])
        df_mapa2['new_id']= df_mapa2.index
        df_mapa2['new_id']= df_mapa2.index

        df_up = df_mapa2[['new_id','LATITUD', 'LONGITUD', 'destino_municipio']]
        df_down = df_mapa2[['new_id',"lat_destino_municipio", "lon_destino_municipio", 'destino_municipio']]
        df_down.columns = ['new_id','LATITUD', 'LONGITUD', 'destino_municipio']
        df_mapa2 = pd.concat([df_up, df_down]).reset_index()
        df_mapa2.head(7)
        color_line='destino_municipio'


    if  (map_bubble_selection=='opMuOMeD'): # Municipio Origen a MercadoDestino
        columns_procedencia = ['procedencia_codigo_municipio', 'procedencia_municipio']
        columns_destino = ['destino_ciudad_mercado']
        origen = 1
        destino=1

        df_mapa = df_filtrado.groupby(columns_procedencia, agg = {column_agg: function_agg})
        df_mapa = df_mapa.to_pandas_df()
        # df_mapa = pd.merge(df_mapa, df_municipios_properties, how="left", left_on=["procedencia_codigo_municipio"], right_on=["MPIO_CDPMP"])

        # df_mapa.reset_index(inplace=True)
        df_mapa = pd.merge(df_mapa, df_municipios_properties, how="left", left_on=["procedencia_codigo_municipio"], right_on=["MPIO_CDPMP"])
        df_mapa = df_mapa.assign(Ubicacion="Procedencia")
        df_mapa.rename(columns={'procedencia_municipio': 'nombre'}, inplace=True)
        df_mapa = df_mapa[['nombre', column_agg, 'LATITUD', 'LONGITUD', 'Ubicacion']]

        df_mapa2 = df_filtrado.groupby(columns_destino, agg = {column_agg: function_agg})
        # df_mapa2 = df_mapa2.to_pandas_df()
        # df_mapa2.reset_index(inplace=True)
        # df_mapa2 = pd.merge(df_mapa2, df_coor_merc, how="left", left_on=['destino_ciudad_mercado'], right_on=['destino_ciudad_mercado'])
        df_mapa2 = df_mapa2.join(df_coor_merc_copy, how="left", on='destino_ciudad_mercado')
        df_mapa2 = df_mapa2.to_pandas_df()
        df_mapa2 = df_mapa2.assign(Ubicacion="Destino")
        df_mapa2.rename(columns={'destino_ciudad_mercado': 'nombre', "lat_mercado":'LATITUD', "lon_mercado":"LONGITUD" }, inplace=True)
        map_latitud = "LATITUD"
        map_longitud = "LONGITUD"
        map_hoover = "nombre"
        df_mapa2 = df_mapa2[[map_hoover, column_agg, map_latitud, map_longitud, 'Ubicacion']]
        
        # print("DENTRO DE IF MAPA: ", df_mapa)
        # print("DENTRO DE IF MAPA 2: ", df_mapa2)

        frames = [df_mapa, df_mapa2]
        df_mapa = pd.concat(frames)
        df_mapa.reset_index(inplace=True)
        df_mapa2=[]
        df_mapa2 = df_filtrado[['procedencia_codigo_municipio', 'procedencia_municipio', 'destino_ciudad_mercado']]
        df_mapa2 = df_mapa2.groupby(['procedencia_codigo_municipio', 'procedencia_municipio', 'destino_ciudad_mercado'],agg={ 'cnt' : vaex.agg.count() } )
        df_mapa2 = df_mapa2.to_pandas_df()
        df_mapa2 = pd.merge(df_mapa2, df_municipios_properties, how="left", left_on=["procedencia_codigo_municipio"], right_on=["MPIO_CDPMP"])
        df_coor_merc_copy =  df_coor_merc_copy.to_pandas_df()
        df_mapa2 = pd.merge(df_mapa2, df_coor_merc_copy, how="left", left_on=["destino_ciudad_mercado"], right_on=["destino_ciudad_mercado"])
        df_mapa2 = df_mapa2.dropna(subset=['MPIO_CDPMP'])
        df_mapa2['new_id']= df_mapa2.index
        df_mapa2['new_id']= df_mapa2.index
        df_up = df_mapa2[['new_id','LATITUD', 'LONGITUD', 'destino_ciudad_mercado']]
        df_down = df_mapa2[['new_id','lat_mercado', 'lon_mercado', 'destino_ciudad_mercado']]
        df_down.columns = ['new_id','LATITUD', 'LONGITUD', 'destino_ciudad_mercado']
        df_mapa2 = pd.concat([df_up, df_down]).reset_index()
        df_mapa2.head(7)
        color_line='destino_ciudad_mercado'

    # print("MAPA DESPUES DE IF: ", df_mapa)
    max_value = df_mapa[column_agg].max()

    df_mapa['bubble'] = (40 * df_mapa[column_agg]/max_value)+2.5
    print('Geographical Data successfully calculated!')
    print('Calculating rendering Map')
    mapa = px.scatter_mapbox(df_mapa,
                        lat=map_latitud,
                        lon=map_longitud,
                        size='bubble',
                        hover_name=map_hoover,
                        hover_data= {map_latitud:False, map_longitud:False, 'bubble':False, column_agg:True},
                        labels={column_agg:plot_label1},
                        title = text_analizer,
                        color='Ubicacion',
                        # color_continuous_scale=px.colors.cyclical.IceFire,
                        size_max=35,
                        opacity = 0.6,
                        zoom=18)

# mapbox_style (str (default 'basic', needs Mapbox API token)) – Identifier of base map style,
# some of which require a Mapbox API token to be set using plotly.express.set_mapbox_access_token().
# Allowed values which do not require a Mapbox API token are 'open-street-map', 'white-bg', 'carto-positron',
# 'carto-darkmatter', 'stamen- terrain', 'stamen-toner', 'stamen-watercolor'.
# Allowed values which do require a Mapbox API token are
# 'basic', 'streets', 'outdoors', 'light', 'dark', 'satellite', 'satellite- streets'.

    mapa.update_layout(mapbox_zoom=5.3,
                        mapbox_style="open-street-map",
                        mapbox_center = {"lat": 4.570868, "lon": -74.2973328},
                        margin=dict(l=20, r=20, t=20, b=20),
                        #width='100%'
                        height=900
                        ),
    print("Map Lines calculated, start rendering, IF too many lines, render may crash")
    print('')

    if (origen+destino==2):
        print('Rendering map-lines...')
        mapa2 = px.line_mapbox(df_mapa2,
            #mode = "markers+lines",
            mapbox_style="stamen-terrain",

            lat='LATITUD',
            lon='LONGITUD',
            zoom=3,
            height=300,
            line_group='new_id',
            color=color_line
            )

        mapa2.update_layout(mapbox_zoom=4, mapbox_center_lat = 4.570868,
        margin={"r":0,"t":0,"l":0,"b":0})
        print('Finished Rendering map-lines')

        [mapa.add_trace(x) for x in mapa2.data]
    print('Successfully calculated geographical data')
    df_mapa=[]
    df_mapa2=[]
    return(mapa)

@app.callback( # update groupby table
    dash.dependencies.Output('datatable_id', 'data'),
    dash.dependencies.Output('datatable_id', 'columns'),
    dash.dependencies.Output('datatable_id', 'style_data_conditional'),
    dash.dependencies.Output('bar-group-fig', 'figure'),
    [# dash.dependencies.Input('agrupador-dropdown', 'value'),
    dash.dependencies.Input('agrupador-dropdown-1', 'value'),
    dash.dependencies.Input('agrupador-dropdown-2', 'value'),
    dash.dependencies.Input('agrupador-dropdown-3', 'value'),
    dash.dependencies.Input('agrupador-dropdown-4', 'value'),
    dash.dependencies.Input('output-container-range-slider', 'children'),
    dash.dependencies.Input('output-container-dptos-origen', 'children'),
    dash.dependencies.Input('output-container-mpios-origen', 'children'),
    dash.dependencies.Input('output-container-grupos', 'children'),
    dash.dependencies.Input('output-container-alimentos', 'children'),
    dash.dependencies.Input('output-container-mercados-destino', 'children'),
    ])
def update_group_table(agrupador1, agrupador2, agrupador3, agrupador4,
                         sl, dpt, mpio, gr, alim, merD):
    global df_grouped
    print('Calculating GroupBy table...')
    lista_agrupadores = list(np.unique([agrupador1, agrupador2, agrupador3, agrupador4]))
    if 'empty' in lista_agrupadores:
        lista_agrupadores.remove('empty')

    if len(lista_agrupadores)==0:
        lista_agrupadores='grupo'
    df_grouped = df_filtrado.groupby(lista_agrupadores, agg = {column_agg: function_agg})
    df_grouped = df_grouped.sort([column_agg], ascending=False)
    # df_grouped.sort_values(by=[column_agg], ascending=False, inplace=True)
    # df_grouped.reset_index(inplace=True)
    df_grouped = df_grouped.to_pandas_df()
    grouped_columns=[{"name": column_mapper[i], "id": i, "deletable": False, "selectable": False} for i in df_grouped.columns]


    (styles, legend) = discrete_background_color_bins(df_grouped, columns = [column_agg])
    df_grouped[column_agg] = df_grouped[column_agg].apply('{:,.0f}'.format)
    # {:,.0f}

    if agrupador1 == 'empty':
        print('entra agrupador1 es empty')
        agrupador1='grupo'
    if agrupador2=='empty':
        agrupador2='year'


    df_grouped_graph = df_filtrado.groupby(agrupador1, agg = {column_agg: function_agg})
    df_grouped_graph = df_grouped_graph.sort([column_agg], ascending=False)
    # df_grouped_pivot_graph.reset_index(inplace=True)
    top_list = df_grouped_graph[agrupador1][0:20].unique()
    df_grouped_graph = df_filtrado[df_filtrado[agrupador1].isin(top_list)]
    df_grouped_graph = df_grouped_graph.groupby([agrupador1, agrupador2], agg = {column_agg: function_agg})
    df_grouped_graph = df_grouped_graph.sort([column_agg], ascending=False)
    df_grouped_graph = df_grouped_graph.sort([agrupador2], ascending=True)
    df_grouped_graph = df_grouped_graph.to_pandas_df()

    # df_grouped_graph = df_grouped_graph.sort_values([agrupador2], ascending=True)
    # df_grouped_graph = df_grouped_graph.sort_values([agrupador1], ascending=False)
    df_grouped_graph[agrupador1] = df_grouped_graph[agrupador1].astype('string')
    df_grouped_graph[agrupador2] = df_grouped_graph[agrupador2].astype('string')

    group_chart = px.bar(
        data_frame=df_grouped_graph,
        y = agrupador1,
        x = column_agg,
        color = agrupador2,
        opacity = 0.9, 
        # title = text_analizer,
        labels = {agrupador1:column_mapper[agrupador1], column_agg:plot_label1},
#        orientation = v,
        barmode= 'relative', #'overlay' #relative, group,
        # labels,
        # title
        # template
        )
    return [df_grouped.to_dict('records'), grouped_columns, styles, group_chart]


@app.callback( # update pivot table
    dash.dependencies.Output('pivot-table-id', 'data'),
    dash.dependencies.Output('pivot-table-id', 'columns'),
    dash.dependencies.Output('pivot-table-id', 'style_data_conditional'),
    dash.dependencies.Output('bar-pivot-fig', 'figure'),
    [dash.dependencies.Input('pivot-dropdown-1', 'value'),
    dash.dependencies.Input('pivot-dropdown-2', 'value'),
    dash.dependencies.Input('output-container-range-slider', 'children'),
    dash.dependencies.Input('output-container-dptos-origen', 'children'),
    dash.dependencies.Input('output-container-mpios-origen', 'children'),
    dash.dependencies.Input('output-container-grupos', 'children'),
    dash.dependencies.Input('output-container-alimentos', 'children'),
    dash.dependencies.Input('output-container-mercados-destino', 'children'),
    dash.dependencies.Input('daq-pivot-switch', 'on')
    ])
def update_pivot_table(pivotSelector1, pivotSelector2,
                         sl, dpt, mpio, gr, alim, merD, pivot_switch):
    
    if(pivot_switch):
        global table
        print('Calculating Pivot table...')
        if pivotSelector1 == pivotSelector2:
            pivotSelector1='grupo'
        if pivotSelector1 == pivotSelector2:
            pivotSelector1='year'

        columns_pivot = ['procedencia_departamento', 'procedencia_municipio', 'grupo',
                            'alimento', 'cantidad_kg', 'procedencia_pais', 'destino_ciudad',
                            'destino_ciudad_mercado', 'day', 'month', 'year', 'year_month']

        table = df_filtrado.to_pandas_df()

        table = table[['procedencia_departamento', 'procedencia_municipio', 'grupo',
                            'alimento', 'cantidad_kg', 'procedencia_pais', 'destino_ciudad',
                            'destino_ciudad_mercado', 'day', 'month', 'year', 'year_month', column_agg]]

        for mycolumn in columns_pivot:
            print(mycolumn)
            table[mycolumn]=table[mycolumn].astype('string')
            # table[mycolumn].astype('string')
        table[column_agg] = table[column_agg].astype(float)

        # table = df_filtrado.to_pandas_df()
        # table.reset_index(inplace=True)
        table = pd.pivot_table(table, values=column_agg, index=[pivotSelector1],
                columns=[pivotSelector2], aggfunc=pivotfunc, fill_value=0)

        table = table.loc[:,~table.columns.duplicated()]
        pivot_columnas_temporal = [{"name": column_mapper[pivotSelector1], "id": pivotSelector1}]

        for column_name in table.columns:
            table[column_name] = table[column_name].apply('{:,.1f}'.format)

        pivot_columns = [{"name": i, "id": i, "deletable": False, "selectable": False} for i in table.columns]
        pivot_columns = pivot_columnas_temporal + pivot_columns

        pivot_index = [{"name": i, "id": i, "deletable": False, "selectable": False} for i in table.index]
        df_grouped_pivot_graph = df_filtrado.groupby(pivotSelector1, agg = {column_agg: function_agg})

        df_grouped_pivot_graph = df_grouped_pivot_graph.sort([column_agg], ascending=False)
        df_grouped_pivot_graph = df_grouped_pivot_graph.to_pandas_df()
        df_grouped_pivot_graph[pivotSelector1] = df_grouped_pivot_graph[pivotSelector1].astype('string')
        #df_grouped_pivot_graph[pivotSelector2] = df_grouped_pivot_graph[pivotSelector2].astype('string')
        top_list = df_grouped_pivot_graph[pivotSelector1][0:15].unique()
        df_grouped_pivot_graph = df_filtrado[df_filtrado[pivotSelector1].isin(top_list)]
        df_grouped_pivot_graph = df_grouped_pivot_graph.groupby([pivotSelector1, pivotSelector2], agg = {column_agg: function_agg})
        # df_grouped_pivot_graph.reset_index(inplace=True)
        df_grouped_pivot_graph = df_grouped_pivot_graph.to_pandas_df()
        # df_grouped_pivot_graph.reset_index(inplace=True)
        df_grouped_pivot_graph=df_grouped_pivot_graph.sort_values([pivotSelector1], ascending=True)
        # df_grouped_pivot_graph.reset_index(inplace=True)
        df_grouped_pivot_graph[pivotSelector1] = df_grouped_pivot_graph[pivotSelector1].astype('string')
        df_grouped_pivot_graph[pivotSelector2] = df_grouped_pivot_graph[pivotSelector2].astype('string')
 
        print('Sucessfully calculated Pivot Table data')
        print('')

        bar_chart = px.bar(
            data_frame=df_grouped_pivot_graph,
            y = pivotSelector1,
            x = column_agg,
            color = pivotSelector2,
            opacity = 0.9,
            # title = text_analizer,
            labels = {pivotSelector1:column_mapper[pivotSelector1], column_agg:plot_label1},
    #        orientation = v,
            barmode= 'relative', #'overlay' #relative, group,
            # labels,
            # title
            # template
            ),
        bar_chart.update_layout(
            yaxis = list(categoryarray = sorted(top_list), categoryorder = "array")
        )

        #cols = ['02', '03', '04', '05']
        #cols = list(table.columns)
        (styles, legend) = discrete_background_color_bins(table, columns = 'all')
        return [table.reset_index().to_dict('records'), pivot_columns, styles, bar_chart]
    #return [df_grouped.to_dict('records'), grouped_columns]

    else:
        raise dash.exceptions.PreventUpdate

###############################################################
@app.callback( #click export datatable
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df_grouped.to_csv, "tabla_agrupada.csv")

###############################################################
@app.callback( #click export pivotTable
    Output("download-pivot-csv", "data"),
    Input("btn2_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(table.to_csv, "tabla_pivot.csv")

##################################################################
########################  RUN SERVER  ############################
##################################################################

if __name__ == '__main__':
    app.run_server(debug=False)