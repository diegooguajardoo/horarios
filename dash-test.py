import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from datetime import datetime

df = pd.read_csv("clip_transformed2.csv")



active_week = datetime.now().isocalendar()[1]-2


app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    children=[
        html.H1(children='Horario de clases'),
        html.Br(),
        html.P('Selecciona un maestro:'),
        dcc.Dropdown(id='my-dropdown', multi=False,
                     options=[{'label': x, 'value': x} for x in df["Maestro"].sort_values().unique()],
                     value=df["Maestro"].sort_values().unique()[0]),
        html.Br(),
        html.H6(id="week", children="Semana 1"),
        dbc.Pagination(id="pagination", max_value=17,active_page=active_week),
        dcc.Graph(id='graph-output', figure={},)], 
        style={'width': '90%', 'display': 'inline-block',"text-align": "left", 'padding': '50px'}
)


def produce_week2(data,week):
    if (data.Dias.nunique() == 5) & (data.Hora.nunique() == 5):
        output = data.pivot(index="Hora", columns="Dias", values=f"Info_Semana{week}").fillna(" ")
        output["Hora"] = output.index
        output = output[["Hora","Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]]
        return output
    else:
        blank = pd.DataFrame(columns=pd.Categorical(["Hora","Lunes", "Martes", "Miercoles", "Jueves", "Viernes"], ordered=True), index=pd.Series(range(1,6)))
        result = data.pivot(index="Hora", columns="Dias", values=f"Info_Semana{week}")
        output = result.combine_first(blank).fillna(" ")
        output = output[["Hora","Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]]
        return output
    

@app.callback(
    Output(component_id='graph-output', component_property='figure'),
    Output(component_id='week', component_property='children'),
    [Input(component_id='my-dropdown', component_property='value')],
    [Input(component_id='pagination', component_property='active_page')],
    prevent_initial_call=False
)

def update_my_graph(val_chosen, week_chosen):
    if len(val_chosen) > 0:
        #head = list(map(produce_week2, df.groupby(["Maestro"]).get_group(val_chosen)["Info"]))
        #dff = head.groupby(["Maestro"]).loc[val_chosen]
        dff = df.copy()
        tab = produce_week2(dff.groupby(["Maestro"]).get_group(val_chosen), week_chosen)
        tab["Hora"] = tab.index
        fig = go.Figure(data=[go.Table(
            header=dict(values=[x for x in tab.columns], align='center',font=dict(color='white', size=12)),
            cells=dict(values=[tab.Hora, tab.Lunes, tab.Martes, tab.Miercoles,tab.Jueves, tab.Viernes], align='center'),)]) 
                       #fill=dict({"color": [["white", "red", "red", "blue", "red"],["white", "red", "blue", "red", "red"]]})

        return fig, f"Semana {week_chosen}"
    elif len(val_chosen) == 0:
        return Dash.no_update, f"Semana {week_chosen}"


if __name__ == '__main__':
    app.run_server(debug=True)