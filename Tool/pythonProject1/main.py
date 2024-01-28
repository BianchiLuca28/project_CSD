import base64
import io
import pandas as pd
import dash
from dash import html, dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = 'Anomalies Detector'

# App layout
# App layout
app.layout = html.Div([
    html.H1("Anomalies Detector", style={'text-align': 'center', 'color': 'orange'}),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag or select a file',
            html.A(' or select from your files')
        ]),
        style={
            'width': '100%',
            'height': '100px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'color': 'white',
            'backgroundColor': '#333',
            'padding': '20px'
        },
        multiple=True
    ),
    dcc.Dropdown(
        id='model-selector',
        options=[
            {'label': 'Model One - Placeholder', 'value': 'MOD1'},
            {'label': 'Model Two - Placeholder', 'value': 'MOD2'},
            # Add other placeholder models here...
        ],
        value=None,
        placeholder="Select a model...",
        style={'backgroundColor': '#333', 'color': 'white', 'margin': '10px'}
    ),
    dcc.Graph(id='output-data-upload'),
], style={'backgroundColor': '#111', 'color': 'white', 'padding': '10px'})

# Helper function to parse uploaded data
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assuming the file is a CSV
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assuming the file is an Excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return html.Div(['File type not supported.'])
    except Exception as e:
        print(e)
        return html.Div(['Error in processing the file.'])

    return df

# Function to detect anomalies (customize as needed)
def detect_anomalies(df, method):
    # Implement your anomaly detection method here
    if method == 'SMM':
        window_size = 10
        df['moving_average'] = df['value'].rolling(window=window_size).mean()
        df['difference'] = abs(df['value'] - df['moving_average'])

        threshold = 2 * df['difference'].std()
        df['anomaly'] = df['difference'] > threshold
    # Add other methods here...

    return df

# Callback to update data
@app.callback(
    Output('output-data-upload', 'figure'),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename'),
     Input('model-selector', 'value')]
)
def update_output(list_of_contents, list_of_names, selected_model):
    if list_of_contents is not None:
        fig = go.Figure()

        for contents, name in zip(list_of_contents, list_of_names):
            df = parse_contents(contents, name)
            df = detect_anomalies(df, selected_model)
            # Add data to the graph
            fig.add_trace(go.Scatter(x=df.index, y=df['value'], mode='lines', name=name))
            fig.add_trace(go.Scatter(x=df[df['anomaly']].index, y=df[df['anomaly']]['value'], mode='markers', name=f'Anomalies in {name}'))

        # Make sure the graph fits the dark theme
        fig.update_layout(
            title='Anomaly Detection Results',
            paper_bgcolor='#111',  # Background color outside the plot
            plot_bgcolor='#111',   # Background color of the plot
            font=dict(
                color='white'      # Text color
            ),
            xaxis=dict(
                linecolor='white', # X-axis line color
                gridcolor='#444'   # X-axis grid color
            ),
            yaxis=dict(
                linecolor='white', # Y-axis line color
                gridcolor='#444'   # Y-axis grid color
            ),
            legend=dict(
                bgcolor='#111',    # Background color of the legend
                bordercolor='#444',# Border color of the legend
                font=dict(
                    color='white'  # Text color in the legend
                )
            )
        )
        return fig
    else:
        return go.Figure()

if __name__ == '__main__':
    app.run_server(debug=True)
