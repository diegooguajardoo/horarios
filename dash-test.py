import pandas as pd
from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from datetime import datetime

df = pd.read_csv("https://raw.githubusercontent.com/diegooguajardoo/horarios/main/segundoclip_transformed3.csv")
dfweek = pd.read_csv("https://raw.githubusercontent.com/diegooguajardoo/horarios-additional-files/main/Fechas.csv")


active_week = datetime.now().isocalendar()[1]-1


app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    children=[
        html.H1(children='Horario de clases'),
        html.P('Nombre del maestro:'),
        dcc.Dropdown(id='my-dropdown', multi=False,
                     options=[{'label': x, 'value': x} for x in df["Maestro"].sort_values().unique()],
                     value=df["Maestro"].sort_values().unique()[0]),
        html.Legend(id="week", children="Semana 1"),
        html.H6(id= 'weekdescription',children=f'{dfweek.loc[active_week-1,["Inicio"]].str.strip() + " - " + dfweek.loc[active_week-1,["Fin"]].str.strip()}'),
        dbc.Pagination(id="pagination", max_value=17,active_page=active_week,fully_expanded=False,previous_next=True),
        dcc.Graph(id='graph-output', figure={},),
        dash_table.DataTable(id='tbl',data=None, columns=None, style_cell={'textAlign': 'center'}, style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'}, style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'}], style_table={'height': '300px', 'overflowY': 'auto'})
        ], style={'width': '100%', 'display': 'inline-block',"text-align": "left", 'padding': '50px'}
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
    Output(component_id='weekdescription', component_property='children'),
    [Input(component_id='my-dropdown', component_property='value')],
    [Input(component_id='pagination', component_property='active_page')],
    [Input(component_id='pagination', component_property='active_page')],
    prevent_initial_call=False
)

def update_my_graph(val_chosen, week_chosen, week):
    if len(val_chosen) > 0:
        #head = list(map(produce_week2, df.groupby(["Maestro"]).get_group(val_chosen)["Info"]))
        #dff = head.groupby(["Maestro"]).loc[val_chosen]
        dff = df.copy()
        tab = produce_week2(dff.groupby(["Maestro"]).get_group((val_chosen,)), week_chosen)
        tab["Hora"] = tab.index
        fig = go.Figure(data=[go.Table(
            header=dict(values=[x for x in tab.columns], align='center',font=dict(color='white', size=12)),
            cells=dict(values=[tab.Hora, tab.Lunes, tab.Martes, tab.Miercoles,tab.Jueves, tab.Viernes], align='center', height=40))])  
                       #fill=dict({"color": [["white", "red", "red", "blue", "red"],["white", "red", "blue", "red", "red"]]})
        fig.update_layout(height=600, width=1000)
        return fig, f"Semana {week_chosen}",f'{dfweek.loc[week-1,["Inicio"]][0].strip() + " - " + dfweek.loc[week-1,["Fin"]][0].strip()}'
    elif len(val_chosen) == 0:
        return Dash.no_update, f"Semana {week_chosen}", f'{dfweek.loc[week-1,["Inicio"]][0].strip() + " - " + dfweek.loc[week-1,["Fin"]][0].strip()}'


if __name__ == '__main__':
    app.run_server(debug=True)