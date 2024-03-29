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

# definir el app layout con CSS styling (style = {})
app.layout = html.Div([
    html.Img(src=logo_url, style={'width': '300px', 'margin': 'auto'}),
    html.H1("Dashboard para el departamento de Producción", style={'textAlign': 'center',"fontFamily":"Courier New"}),
    html.Label("Seleccione el departamento a evaluar:", style={'textAlign': 'center', 'fontWeight': 'bold', "fontFamily":"Courier New"}),
    dcc.Dropdown(
        id='department-dropdown',
        options=[
            {'label': 'Sewing Department', 'value': 'sewing'},
            {'label': 'Finishing Department', 'value': 'finishing'}
        ],
        value='sewing',
        style={'width': '50%', 'margin': 'auto'}
    ),
    html.Label("Ingrese los valores:", style={'textAlign': 'center', 'fontWeight': 'bold', "fontFamily":"Courier New"}),
    html.Div(id='x-values-input', style={'width': '50%', 'margin': 'auto'}),
    html.Button('Calcular', id='submit-val', n_clicks=0, style={'margin': '20px auto', 'display': 'block'}),
    html.Div(id='output-container-button', style={'textAlign': 'center', 'fontSize': '20px'}),
    html.Div([
        dcc.Graph(id='3d-plot')]),
    # Foto background watermark
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
        x_vars = ['team','targeted_productivity','smv','over_time','incentive','idle_time','idle_men','no_of_workers','day_Sunday','day_Saturday',"day_Monday",'day_Tuesday','day_Wednesday','day_Thursday']
    elif department == 'finishing':
        x_vars = ['smv', 'over_time', 'no_of_workers']
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
            x_vars = ['team','targeted_productivity','smv','over_time','incentive','idle_time','idle_men','no_of_workers','day_Sunday','day_Saturday',"day_Monday",'day_Tuesday','day_Wednesday','day_Thursday']
            data = sewing_data
        elif department == 'finishing':
            x_vars = ['smv', 'over_time', 'no_of_workers']
            data = finishing_data
        x_values = [float(input_elem['props']['value']) for input_elem in x_values_inputs if input_elem['props']['id'].startswith('x-')]
        
        #------------------------------------------------------------------------------------
        #Incluir la parte de Ciencia de Datos -- Parte: Usando StatsModels
        X = sm.add_constant(data[x_vars])
        y = data['actual_productivity']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = sm.OLS(y_train, X_train).fit()
        predicted_y = model.predict([1] + x_values)
        return f"Productividad estimada: {predicted_y[0]}"
    
import plotly.graph_objects as go

# Callback para la gráfica 3D
@app.callback(
    Output('3d-plot', 'figure'),
    Input('department-dropdown', 'value'))
def update_3d_plot(department):
    if department == 'sewing':
        x_data = sewing_data['incentive']
        y_data = sewing_data['targeted_productivity']
    elif department == 'finishing':
        x_data = finishing_data['smv']
        y_data = finishing_data['over_time']

    z_data = sewing_data['actual_productivity'] if department == 'sewing' else finishing_data['actual_productivity']
    if department == 'sewing':
        titulo_x = "Incentivo"
        titulo_y = "Prod. Objetivo"
    elif department == 'finishing':
        titulo_x = 'smv'
        titulo_y = 'over_time'

    fig = go.Figure(data=[go.Scatter3d(
        x=x_data,
        y=y_data,
        z=z_data,
        mode='markers',
        marker=dict(
            size=12,
            color=z_data,                
            colorscale='Viridis',   
            opacity=0.8
        )
    )])
    fig.update_layout(scene=dict(
        xaxis_title= titulo_x,
        yaxis_title= titulo_y,
        zaxis_title='Prod. actual'
    ),
    title = f"Gráfica productividad actual vs {titulo_x} y {titulo_y}")
    return fig


print("GOING LIVE")
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


