import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from aggdata import AggData, Remove_Suspect, IQR, plot_line_graph


# Fetch AggData
pm2 = AggData("PM2.5")
pm10 = AggData("PM10")
no2 = AggData("NO2")

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='variable-selector1',
        options=[
            {'label': 'PM2.5', 'value': 'PM2.5'},
            {'label': 'PM10', 'value': 'PM10'},
            {'label': 'NO2', 'value': 'NO2'}
        ],
        value='PM2.5'
    ),
    dcc.Dropdown(
        id='variable-selector2',
        options=[
            {'label': 'PM2.5', 'value': 'PM2.5'},
            {'label': 'PM10', 'value': 'PM10'},
            {'label': 'NO2', 'value': 'NO2'}
        ],
        value='PM10'
    ),
    html.Div(id='dashboard'),
])

@app.callback(
    Output('dashboard', 'children'),
    Input('variable-selector1', 'value'),
    Input('variable-selector2', 'value')
)
def update_dashboard(variable1, variable2):
    selected_data1 = None
    selected_data2 = None
    for instance in AggData.instances:
        if instance.data_params["data_variable"] == variable1:
            selected_data1 = instance
        if instance.data_params["data_variable"] == variable2:
            selected_data2 = instance
        if selected_data1 is not None and selected_data2 is not None:
            break

    if selected_data1 is not None and selected_data2 is not None:
        df1 = Remove_Suspect(selected_data1.df)
        dfIQR1 = IQR(df1)
        figure1 = plot_line_graph(dfIQR1, selected_data1.data_params)

        df2 = Remove_Suspect(selected_data2.df)
        dfIQR2 = IQR(df2)
        figure2 = plot_line_graph(dfIQR2, selected_data2.data_params)

        return [
            dcc.Graph(figure=figure1, id='graph1'),
            dcc.Graph(figure=figure2, id='graph2'),
        ]

if __name__ == '__main__':
    app.run_server(debug=True)
