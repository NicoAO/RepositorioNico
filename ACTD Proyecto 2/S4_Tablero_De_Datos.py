import dash
from dash import html, dcc, Input, Output
import pandas as pd
import statsmodels.api as sm

#Bases de datos 
data = pd.read_csv("datosproyecto2")

#Crear la Dash app
app = dash.Dash(__name__)