import dash
from dash import html, dcc, Input, Output
import pandas as pd
import statsmodels.api as sm

#Bases de datos 
data = pd.read_csv("ACTD Proyecto 2/datosproyecto2")

#Crear la Dash app
app = dash.Dash(__name__)

# Logo de la Universidad de Los Andes :)
logo_url = "https://images.ctfassets.net/wp1lcwdav1p1/32ZvbT2qtVDItdoxBhRHRf/ee5581294ae18385bf17cbccdcd74a79/LOGOS_Ingenieri__a_Uniandes_2018-_Color.png?q=60"

# definir el app layout con CSS styling (style = {})
app.layout = html.Div([
    html.Img(src=logo_url, style={'width': '300px', 'margin': 'auto'}),
    html.H1("Dashboard para el área de riesgo", style={'textAlign': 'center',"fontFamily":"Courier New"}),
    html.Label("Ingrese la información:", style={'textAlign': 'center', 'fontWeight': 'bold', "fontFamily":"Courier New"}),
    html.Div(id='x-values-input', style={'width': '50%', 'margin': 'auto'}),
    html.Button('Calcular', id='submit-val', n_clicks=0, style={'margin': '20px auto', 'display': 'block'}),
    html.Div(id='output-container-button', style={'textAlign': 'center', 'fontSize': '20px'}),
    html.Div([
            dcc.Graph(id='correlation-matrix'),
        ], className='six columns'),
        html.Div([
            dcc.Graph(id='boxplot'),
        ], className='six columns'),
        html.Div([
            dcc.Graph(id='line-chart'),
        ], className='twelve columns'),

    # Foto background watermark
    html.Div([
        html.Div(style={'position': 'absolute', 'top': '0', 'left': '0', 'width': '100%', 'height': '100%',
                        'background-image': 'url("https://www.elpais.com.co/resizer/W5OWOK0-li_y4FcdfLkYw0WEiG4=/1280x720/smart/filters:format(jpg):quality(80)/cloudfront-us-east-1.images.arcpublishing.com/semana/26W6AB74KVBZVKBUUHVHRPOPEE.jpg")',
                        'opacity': '0.4', 'z-index': '-1'}),
        html.Div(style={'position': 'relative', 'z-index': '0'})   
    ])
])


print("GOING LIVE")
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)