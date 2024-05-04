import dash
from dash import html, dcc, Input, Output
import pandas as pd
import statsmodels.api as sm
import tensorflow as tf
import joblib
from sklearn.preprocessing import MinMaxScaler

#Caragar archivo de disco
model = joblib.load("ACTD Proyecto 2/modelo.joblib")

#Crear la Dash app
app = dash.Dash(__name__)

x_vars = ["LIMIT_BAL", "SEX", "EDUCATION", "MARRIAGE", "AGE", "PAY_0", "PAY_1", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6",
              "BILL_AMT1", "BILL_AMT2", "BILL_AMT3", "BILL_AMT4", "BILL_AMT5", "BILL_AMT6", "PAY_AMT1", "PAY_AMT2", "PAY_AMT3",
              "PAY_AMT4", "PAY_AMT5", "PAY_AMT6",]

# Logo de la Universidad de Los Andes :)
logo_url = "https://images.ctfassets.net/wp1lcwdav1p1/32ZvbT2qtVDItdoxBhRHRf/ee5581294ae18385bf17cbccdcd74a79/LOGOS_Ingenieri__a_Uniandes_2018-_Color.png?q=60"

# definir el app layout con CSS styling (style = {})
app.layout = html.Div([
    html.Img(src=logo_url, style={'width': '300px', 'margin': 'auto'}),
    html.H1("Dashboard para el área de riesgo", style={'textAlign': 'center',"fontFamily":"Courier New"}),
    html.Label("Ingrese la información:", style={'textAlign': 'center', 'fontWeight': 'bold', "fontFamily":"Courier New"}),
    html.Div(
             [dcc.Input(id=f"x-{var}", type='number', placeholder=var, style={'margin': '5px'}) for var in x_vars],
               id='x-values-input', style={'width': '50%', 'margin': 'auto'}),
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

# Callback para generar las entradas de valores X
#@app.callback(
   # Output('x-values-input', 'children'),
   # [Input('submit-val', 'n_clicks')]
#)

#def update_x_values_input(n_clicks):
    # Crear componentes de entrada para cada variable X
   # inputs = [dcc.Input(id=f"x-{var}", type='number', placeholder=var, style={'margin': '5px'}) for var in x_vars]
    #print(inputs)
    #return inputs

# Callback pero para la regresión
@app.callback(
    Output('output-container-button', 'children'),
    Input('submit-val', 'n_clicks'),
    [Input("x-{}".format(var), "value") for var in x_vars], prevent_intial_call=True)
def update_output(n_clicks, *x_values_inputs):
    if n_clicks > 0:        
       # x_values = [float(input_elem['props']['value']) for input_elem in x_values_inputs if input_elem['props']['id'].startswith('x-')]
        #print(x_values_inputs[0])
        #if len(x_values) != len(x_vars):
         #   return "Por favor, ingrese todos los valores de entrada."
        
        # Hacer la predicción con el modelo cargado
        y_pred = model.predict([x_values_inputs])

        return f"Default payment next month: {y_pred[0]}"

print("GOING LIVE")
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)