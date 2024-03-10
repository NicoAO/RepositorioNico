import pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
import dash
from dash import html, dcc, Input, Output

# Load datasets for sewing and finishing departments
sewing_data = pd.read_csv('datosproyecto1', index_col=0)
finishing_data = pd.read_csv('finishing_datos', index_col=0)

# Define features and target variable
features = ['team', 'targeted_productivity', 'smv', 'wip', 'over_time', 'incentive', 'idle_time', 'idle_men', 'no_of_style_change', 'no_of_workers', 'quarter_cat', 'day_Monday', 'day_Saturday', 'day_Sunday', 'day_Thursday', 'day_Tuesday']
target = 'actual_productivity'

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the Dash app
app.layout = html.Div([
    html.H1("Productivity Dashboard"),
    html.Label("Select Department:"),
    dcc.Dropdown(
        id='department-dropdown',
        options=[
            {'label': 'Sewing', 'value': 'sewing'},
            {'label': 'Finishing', 'value': 'finishing'}
        ],
        value='sewing'
    ),
    html.Label("Select Quarter:"),
    dcc.Dropdown(
        id='quarter-dropdown',
        options=[
            {'label': 'Quarter 1', 'value': 1},
            {'label': 'Quarter 2', 'value': 2}
        ],
        value=1
    ),
    html.Label("Enter x-values:"),
    *[dcc.Input(id=f'{feature}-input', type='number', placeholder=feature) for feature in features],
    html.Button('Calculate', id='calculate-button'),
    html.Div(id='output-container')
])

# Define callback to update output based on user input
@app.callback(
    Output('output-container', 'children'),
    [Input('calculate-button', 'n_clicks')],
    [Input(f'{feature}-input', 'value') for feature in features],
    Input('department-dropdown', 'value'),
    Input('quarter-dropdown', 'value')
)
def update_output(n_clicks, *values):
    if n_clicks:
        department = values[-2]
        quarter = values[-1]
        data = sewing_data if department == 'sewing' else finishing_data
        X = data[features]
        y = data[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
        X_train = sm.add_constant(X_train)
        model = sm.OLS(y_train, X_train).fit()
        X_pred = sm.add_constant([values[:-2]])
        y_pred = model.predict(X_pred)
        return f"Predicted productivity: {y_pred[0]}"


if __name__ == '__main__':
    app.run_server(debug=True)
