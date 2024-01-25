from dash import Dash, dcc, html, Output, Input, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.RadioItems(options=['car','house','ship'], value='ship', id='my-radio-btn'),
    dcc.Slider(10, 20, step=1, value=12, id='my-slider'),
    dcc.Markdown(children='', id='text-displayed', style={'fontSize':10}),
    dbc.Pagination(id="pagination", max_value=17),
])

@callback(
    Output(component_id='text-displayed', component_property='children'),
    Output(component_id='text-displayed', component_property='style'),
    Input(component_id='my-radio-btn', component_property='value'),
    Input(component_id='my-slider', component_property='value')

)
def update_text(selected_text, selected_font_size):  # the function argument comes from the component property of the Input
    print(selected_text)
    print(type(selected_text))
    print('-----------------------')
    print(selected_font_size)
    print(type(selected_font_size))
    return f"The Radio Button value you chose was: {selected_text}", {'fontSize':selected_font_size}  # the returned objects are assigned to the component properties of the Outputs

if __name__=='__main__':
    app.run(port=8003)