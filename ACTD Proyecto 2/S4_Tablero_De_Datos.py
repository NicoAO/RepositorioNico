import dash
from dash import html, dcc, Input, Output
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px

data = pd.read_csv("ACTD Proyecto 2/datosproyecto2")

#Caragar archivo de disco
model = joblib.load("ACTD Proyecto 2/modelo.joblib")

#Crear la Dash app
app = dash.Dash(__name__)

#Nombres de las variables x
x_vars = ["ID","LIMIT_BAL", "SEX", "EDUCATION", "MARRIAGE", "AGE", "PAY_0","PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6",
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
        html.H1("Mapa de Calor de Correlación", style={'textAlign': 'center'}),
        # Elementos de entrada para seleccionar variables
        html.Div([
        html.Label("Seleccione la primera variable:"),
        dcc.Dropdown(
            id='variable-dropdown-1',
            options=[{'label': var, 'value': var} for var in data.columns],
            multi=False
        ),]),
        html.Div([
        html.Label("Seleccione la segunda variable:"),
        dcc.Dropdown(
            id='variable-dropdown-2',
            options=[{'label': var, 'value': var} for var in data.columns],
            multi=False
        ),]),
        html.Div([
        html.Label("Seleccione la tercera variable:"),
        dcc.Dropdown(
            id='variable-dropdown-3',
            options=[{'label': var, 'value': var} for var in data.columns],
            multi=False
        ),]),
        html.Div([
        html.Label("Seleccione la cuarta variable:"),
        dcc.Dropdown(
            id='variable-dropdown-4',
            options=[{'label': var, 'value': var} for var in data.columns],
            multi=False
        ),]),
        dcc.Graph(id='correlation-heatmap')
    ]),

    html.Div([
        html.H1("Scatter Plot", style={'textAlign': 'center'}),
        html.Label("Seleccione la primera variable:"),
        dcc.Dropdown(
            id='variable-dropdown-11',
            options=[{'label': var, 'value': var} for var in x_vars],
            value=x_vars[0]
        ),
        html.Label("Seleccione la segunda variable:"),
        dcc.Dropdown(
            id='variable-dropdown-21',
            options=[{'label': var, 'value': var} for var in x_vars],
            value=x_vars[1]
        ),
        dcc.Graph(id='scatter-plot')
        ]),

        html.Div([
            html.H1("BoxPlot", style={'textAlign': 'center'}),
            html.Div([
            html.Label("Seleccione la variable para mostrar el boxplot:"),
            dcc.Dropdown(
                id='variable-dropdown',
                options=[{'label': var, 'value': var} for var in x_vars],
                multi=False),]),
            dcc.Graph(id='boxplot')
        ],),

    # Foto background watermark
    html.Div([
        html.Div(style={'position': 'absolute', 'top': '0', 'left': '0', 'width': '100%', 'height': '100%',
                        'background-image': 'url("https://www.elpais.com.co/resizer/W5OWOK0-li_y4FcdfLkYw0WEiG4=/1280x720/smart/filters:format(jpg):quality(80)/cloudfront-us-east-1.images.arcpublishing.com/semana/26W6AB74KVBZVKBUUHVHRPOPEE.jpg")',
                        'opacity': '0.4', 'z-index': '-1'}),
        html.Div(style={'position': 'relative', 'z-index': '0'})   
    ])
])

# Callback pero para la regresión
@app.callback(
    Output('output-container-button', 'children'),
    Input('submit-val', 'n_clicks'),
    [Input("x-{}".format(var), "value") for var in x_vars], prevent_intial_call=True)
def update_output(n_clicks, *x_values_inputs):
    if n_clicks > 0:        
        y_pred = model.predict([x_values_inputs])

        return f"Default payment next month: {y_pred[0]}"

# Callback para crear el mapa de calor de correlación
@app.callback(
    Output('correlation-heatmap', 'figure'),
    [Input('variable-dropdown-1', 'value'),
     Input('variable-dropdown-2', 'value'),
     Input('variable-dropdown-3', 'value'),
     Input('variable-dropdown-4', 'value')]
)
def create_correlation_heatmap(var1, var2, var3, var4):
    # Filtrar las variables seleccionadas
    selected_vars = [var for var in [var1, var2, var3, var4] if var]
    
    # Calcular la matriz de correlación
    correlation_data = data[selected_vars].corr()

    # Crear el mapa de calor de correlación
    fig = go.Figure(data=go.Heatmap(z=correlation_data.values,
                                     x=correlation_data.index,
                                     y=correlation_data.columns,
                                     colorscale='Viridis', zmin=-1, zmax=1))
    fig.update_layout(title="Matriz de Correlación (Variables Seleccionadas)")
    return fig


# Callback para actualizar el Scatter Plot
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('variable-dropdown-11', 'value'),
     Input('variable-dropdown-21', 'value')])
def update_scatter_plot(selected_var1, selected_var2):
    fig = px.scatter(data, x=selected_var1, y=selected_var2,
                     title=f"Scatter Plot: {selected_var1} vs. {selected_var2}",
                     labels={selected_var1: selected_var1, selected_var2: selected_var2})
    fig.update_traces(marker=dict(size=10, opacity=0.8))
    fig.update_layout(xaxis_title=selected_var1, yaxis_title=selected_var2)
    return fig

# Callback para mostrar el boxplot de la variable seleccionada por la variable objetivo
@app.callback(
    Output('boxplot', 'figure'),
    [Input('variable-dropdown', 'value')]
)
def update_boxplot(selected_var):
    if not selected_var:
        return {}

    fig = go.Figure()
    fig.add_trace(go.Box(x=data[data['default payment next month'] == 1][selected_var], name="Default = 1"))
    fig.add_trace(go.Box(x=data[data['default payment next month'] == 0][selected_var], name="Default = 0"))
    fig.update_layout(title=f"Box Plot de {selected_var} por Default Payment",
                      yaxis_title="Default Payment Next Month",
                      xaxis_title=selected_var)
    return fig


print("GOING LIVE")
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)