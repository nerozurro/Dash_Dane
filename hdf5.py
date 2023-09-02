import dash
import dash_table
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
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

import vaex




# 1. ------ LEER LOS ARCHIVOS INDEPENDIENTES CSV Y CREAR UNO SOLO ------

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

# print('SUCCESFULLY LOADED SIPSA-DANE DATABASES')

# df.info(memory_usage='deep')

# print(df.head())
# file_path = 'big_file.csv'
# df.to_csv(file_path, index=False)
# print('csv finalizado')

# ---- ACABA 1---------




# 2 ------ LEER EL ARCHIVO FULL CSV Y TRANSFORMARLO A HDF5 ------



file_path = 'big_file.csv'
dv = vaex.from_csv(file_path, convert=True, chunk_size=5_000_000)
print('leido vaex from csv')
type(dv)

# ---ACABA 2------






# 3. ------ LEER EL ARCHIVO HDF5 ------

# # vaex.hdf5.dataset.Hdf5MemoryMapped

# dv = vaex.open('big_file.csv.hdf5')
# print('abierto vaex hdf5')
# suma = dv.cantidad_kg.sum()
# print(suma)

# -----------ACABA 3-------------