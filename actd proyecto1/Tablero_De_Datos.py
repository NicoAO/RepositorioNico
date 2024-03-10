import dash
from dash import html, dcc, Input, Output
import pandas as pd
import statsmodels.api as sm

#Bases de datos 
sewing_data = pd.read_csv("datosproyecto1")
finishing_data = pd.read_csv("finishing_datos")

#Crear la Dash app
app = dash.Dash(__name__)

# Logo de la Universidad de Los Andes :)
logo_url = "https://images.ctfassets.net/wp1lcwdav1p1/32ZvbT2qtVDItdoxBhRHRf/ee5581294ae18385bf17cbccdcd74a79/LOGOS_Ingenieri__a_Uniandes_2018-_Color.png?q=60"


# definir el app layout con CSS styling!
app.layout = html.Div([
    html.Img(src=logo_url, style={'width': '300px', 'margin': 'auto'}),
    html.H1("Dashboard para el departamento de Producción", style={'textAlign': 'center',"fontFamily":"Courier New"}),
    html.Label("Seleccione el departamento a evaluar:", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='department-dropdown',
        options=[
            {'label': 'Sewing Department', 'value': 'sewing'},
            {'label': 'Finishing Department', 'value': 'finishing'}
        ],
        value='sewing',
        style={'width': '50%', 'margin': 'auto'}
    ),
    html.Label("Ingrese los valores:", style={'textAlign': 'center',"fontFamily":"Courier New"}),
    html.Div(id='x-values-input', style={'width': '50%', 'margin': 'auto'}),
    html.Button('Submit', id='submit-val', n_clicks=0, style={'margin': '20px auto', 'display': 'block'}),
    html.Div(id='output-container-button', style={'textAlign': 'center', 'fontSize': '20px'}),

    # Acá se incluye --> background watermark
    html.Div([
        html.Div(style={'position': 'absolute', 'top': '0', 'left': '0', 'width': '100%', 'height': '100%',
                        'background-image': 'url("https://img.freepik.com/premium-photo/computer-aided-manufacturing-hd-wallpaper-photographic-image_993236-3155.jpg")',
                        'opacity': '0.4', 'z-index': '-1'}),
        html.Div(style={'position': 'relative', 'z-index': '0'})  #Note to self: No cambiar el z-index para que se mantenga la imagen al fondo 
    ])
])


# Callback para que se seleccione correctamente cada departamento
@app.callback(
    Output('x-values-input', 'children'),
    Input('department-dropdown', 'value'))
def update_x_values_input(department):
    if department == 'sewing':
        x_vars = ['over_time', 'incentive', 'quarter_cat', 'wip']
    elif department == 'finishing':
        x_vars = ['team', 'targeted_productivity', 'smv', 'over_time', 'incentive', 'idle_time', 'no_of_workers', 'quarter_cat']
    inputs = [dcc.Input(id=f"x-{var}", type='number', placeholder=var, style={'margin': '5px'}) for var in x_vars]
    return inputs
#----------------------------------------------------
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
#----------------------------------------------------
# Callback pero para la regresión
@app.callback(
    Output('output-container-button', 'children'),
    Input('submit-val', 'n_clicks'),
    Input('department-dropdown', 'value'),
    Input('x-values-input', 'children'))
def update_output(n_clicks, department, x_values_inputs):
    if n_clicks > 0:
        if department == 'sewing':
            x_vars = ['over_time', 'incentive', 'quarter_cat', 'wip']
            data = sewing_data
        elif department == 'finishing':
            x_vars = ['team', 'targeted_productivity', 'smv', 'over_time', 'incentive', 'idle_time', 'no_of_workers', 'quarter_cat']
            data = finishing_data
        x_values = [float(input_elem['props']['value']) for input_elem in x_values_inputs if input_elem['props']['id'].startswith('x-')]
        
        #------------------------------------------------------------------------------------
        #Incluir la part de Ciencia de Datos -- Parte: Usando StatsModels
        X = sm.add_constant(data[x_vars])
        y = data['actual_productivity']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = sm.OLS(y_train, X_train).fit()
        predicted_y = model.predict([1] + x_values)
        return f"Predicted Y value: {predicted_y[0]}"
print("GOING LIVE")
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

