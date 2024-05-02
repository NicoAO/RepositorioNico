import dash
from dash import html, dcc, Input, Output
import pandas as pd
import statsmodels.api as sm

#Bases de datos 
data = pd.read_csv("datosproyecto2")

#Crear la Dash app
app = dash.Dash(__name__)

# Logo de la Universidad de Los Andes :)
logo_url = "https://images.ctfassets.net/wp1lcwdav1p1/32ZvbT2qtVDItdoxBhRHRf/ee5581294ae18385bf17cbccdcd74a79/LOGOS_Ingenieri__a_Uniandes_2018-_Color.png?q=60"