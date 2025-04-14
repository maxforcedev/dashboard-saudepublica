import dash
import os
from dash import html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import requests


###========= MAPA =========###
geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
geojson_estados = requests.get(geojson_url).json()


###========= CONFIGS =========###
FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX, dbc_css])
server = app.server

df = pd.read_csv("dataset_saude.csv")
hoje = datetime.today()
inicio_padrao = hoje - timedelta(days=15)
fim_padrao = hoje

###========= ESTILOS =========###

card_style = {'height': '100%', "width": "100%"}
dropdown_style = {"marginTop": "10px", "color": "black", "height": "40px", "fontSize": "14px", "padding": "0px 8px", "lineHeight": "20px", "width": "100%"}

###========= LAYOUT =========###


app.layout = dbc.Container(children=[

    ### LINHA 1: TITULO + CONTROLADORES
    dbc.Row([

        ### COLUNA 1: TITULO 
        dbc.Col([
            html.H3("Painel de Gestão Hospitalar Pública"),
            html.H6("Dados operacionais, financeiros e de qualidade"),
        ], sm=12, md=12, lg=4),

        ### COLUNA 2: CONTROLADOR ESTADO 
        dbc.Col([
            html.H5("Estado"),
            dcc.Dropdown(
                id="dropdown-estado",
                placeholder="Selecionar estado.",
                options= [{"label": x, "value": x} for x in df["estado"].dropna().unique()],
                value= df["estado"].iloc[0],
                style={
                    "marginTop": "10px",
                    "color": "black",
                    "height": "35px",          
                    "fontSize": "14px",        
                    "padding": "0px 8px",      
                    "lineHeight": "20px",      
                    "width": "100%"
                }
            ),
        ], sm=12, md=6, lg=2),

        ### COLUNA 3: CONTROLADOR GESTÃO
        dbc.Col([
            html.H5("Tipo de gestão"),
            dcc.Dropdown(
                id="dropdown-gestao",
                options= [{"label": x, "value": x} for x in df["tipo_gestao"].dropna().unique()],
                value= df["tipo_gestao"].iloc[0],
                style=dropdown_style
            ),
        ], sm=12, md=6, lg=2),

        ### COLUNA 4: CONTROLADOR TIPO. HOSPITAL
        dbc.Col([
            html.H5("Tipo de Hospital"),
            dcc.Dropdown(
                id="dropdown-tipohosp",
                options= [{"label": x, "value": x} for x in df["tipo_unidade"].dropna().unique()],
                value= df["tipo_unidade"].iloc[0],
                style=dropdown_style
            ),
        ], sm=12, md=6, lg=2),

    ], style={"backgroundColor": "#108FEA", "padding": "10px", "color": "white", "marginBottom": "15px"}),
    
    ### LINHA 2: INDICADORES KPIs
    dbc.Row([

        ### COLUNA 1: INDICADOR QTND. HOSPITAIS
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Img(src="/assets/hospital.svg", style={"width": "40px","height": "30px", "marginBottom": "5px"}),
                    html.H3("100", id="indicador-qntdHospital", style={"fontWeight": "bold", "fontSize": "28px", "margin": "0"}),
                    html.Span("Hospitais", style={"fontSize": "13px", "whiteSpace": "nowrap", "textAlign": "center"})
                ], className= "d-flex flex-column justify-content-center align-items-center")
            ], style=card_style)
        ], sm= 6, md= 6, lg=2),

        ### COLUNA 4: INDICADOR TEMPO MEDIO DE ESPERA
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Img(src="/assets/relogio.svg", style={"width": "40px","height": "30px", "marginBottom": "5px"}),
                    html.H3("100", id="indicador-tempoMedio", style={"fontWeight": "bold", "fontSize": "28px", "margin": "0"}),
                    html.Span("Tempo médio de espera (hrs)", style={"fontSize": "13px", "whiteSpace": "nowrap", "textAlign": "center"}),
                ], className= "d-flex flex-column justify-content-center align-items-center")
            ], style=card_style)
        ], sm= 6, md= 6, lg=2),

        ### COLUNA 3: INDICADOR QTND. ATENDIMENTOS
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Img(src="/assets/att.svg", style={"width": "40px","height": "30px", "marginBottom": "5px"}),
                    html.H3("100", id="indicador-qntdAtendimento", style={"fontWeight": "bold", "fontSize": "28px", "margin": "0"}),
                    html.Span("Atendimentos", style={"fontSize": "13px", "whiteSpace": "nowrap", "textAlign": "center"})
                ], className= "d-flex flex-column justify-content-center align-items-center")
            ], style=card_style)
        ], sm= 6, md= 6, lg=2),
        
        ### COLUNA 4: INDICADOR QTND. LEITOS
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        ### COLUNA 1: INDICADOR LEITOS TOTAIS
                        dbc.Col([
                            html.Div([
                                html.Img(src="/assets/leitos.svg", style={"width": "60px", "height": "50px", "marginBottom": "5px"}),
                                html.H3("12654", id="indicador-leitosTotais", style={"fontWeight": "bold", "fontSize": "28px", "margin": "0"}),
                                html.Span("Leitos totais", style={"fontSize": "15px", "marginBottom": "10px"})
                            ], className="d-flex flex-column justify-content-center align-items-center")
                        ], sm=12, md=12, lg=6),

                        ### COLUNA 2: INDICADOR QNTD (DISPONIVEL / OCUPADO)
                        dbc.Col([
                            html.Div([
                                html.Div([
                                    html.Div(id="indicador-leitoDisp" ,style={"color": "green", "fontWeight": "bold"}),
                                    html.Small("Disponíveis")
                                ], className="mb-2"),
                                html.Div([
                                    html.Div(id="indicador-leitoOcup", style={"color": "red", "fontWeight": "bold"}),
                                    html.Small("Ocupados")
                                ], className="mb-2"),
                            ], className="d-flex flex-column justify-content-center align-items-start")
                        ], sm=6, md=6, lg=5),

                        ### COLUNA 23: GRAFICO LATERAL LEITOS                   
                        dbc.Col([
                            html.Div(id="graph-leitos") 
                        ], sm=6, md=1, lg=1),

                    ], align="center"),
                ])
            ], style=card_style)
        ], sm= 6, md= 6, lg=3),
        
        ### COLUNA 5: INDICADOR GASTOS
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3("R$ 461.365,01", id="indicador-gastorepasse1", style={"color": "#2A86C7", "fontWeight": "bold", "fontSize": "32px", "margin": "0"}),
                    html.H3("R$ 345.666,22", id="indicador-gastorepasse2", style={"color": "#5BA2D4", "fontWeight": "bold", "fontSize": "28px", "margin": "0"}),
                    dbc.Row([
                        html.Span("Gastos x Repasses do SUS", style={"fontSize": "13px", "whiteSpace": "nowrap", "textAlign": "center"})
                    ])
                ], className= "d-flex flex-column justify-content-center align-items-center")
            ], style=card_style)
        ], sm= 6, md= 6, lg=3),
    ], className='g-2 my-auto', style={'margin-top': '7px'}, justify='center'),
    
    ### LINHA 3: MAPA + TABELA 
    dbc.Row([
        ### COLUNA 1: MAPA
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dcc.Dropdown(
                                id="filtrar-mapa",
                                placeholder="Filtrar mapa",
                                value="tempo_medio_espera_min",
                                options=[
                                        {"label": "Ocupação", "value": "ocupacao_perc"},
                                        {"label": "Tempo de Espera", "value": "tempo_medio_espera_min"},
                                        {"label": "Mortalidade", "value": "taxa_mortalidade_%"}
                                ],
                            ),
                        dcc.Graph(id="mapa", config={"displayModeBar": False})
                    ])
                ])
            ], style=card_style),
        ], sm=12, md=12, lg=5),
        
        ### COLUNA 2: TABELA
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div(id="tabela-hospitais")
                ])
            ], style=card_style),
        ], sm=12, md=12, lg=7),
        
    ], className='g-2 my-auto', style={'margin-top': '7px'}, justify='center'),
    
    ### LINHA 3: GRAFICOS
    dbc.Row([
        ### COLUNA 1: GRAFICO DISPERSAO
        dbc.Col([
            dbc.Card([
                dbc.CardBody([dcc.Graph(id="medico-espera", config={"displayModeBar": False})])
            ], style=card_style),
        ], sm=12, md=12, lg=3),

        ### COLUNA 2: GRAFICO BARRA
        dbc.Col([
            dbc.Card([
                dbc.CardBody([dcc.Graph(id="gestao-ocupacao", config={"displayModeBar": False})])
            ], style=card_style),
        ], sm=12, md=12, lg=4),
        
        ### COLUNA 3: GRAFICO BARRA
        dbc.Col([
            dbc.Card([
                dbc.CardBody([dcc.Graph(id="filadeespera", config={"displayModeBar": False})])
            ],  style=card_style),
        ], sm=12, md=12, lg=5),

    ], className='g-2 my-auto', style={'margin-top': '7px'}, justify='center'),

], fluid=True, style={"backgroundColor": "#D9D9D9",'height': '100%'})



@app.callback(
    Output("indicador-qntdHospital", "children"),
    Output("indicador-leitoOcup", "children"),
    Output("indicador-leitoDisp", "children"),
    Output("indicador-leitosTotais", "children"),
    Output("indicador-qntdAtendimento", "children"),
    Output("indicador-tempoMedio", "children"),
    Output("indicador-gastorepasse1", "children"),
    Output("indicador-gastorepasse2", "children"),
    Output("graph-leitos", "children"),

    Input("dropdown-estado", "value"),
    Input("dropdown-gestao", "value"),
    Input("dropdown-tipohosp", "value"),


)
def atualizar_indicadores(estado, gestao, tipohosp):

    if estado and gestao and tipohosp:
        df_filtrado = df[(df["estado"] == estado) & (df["tipo_unidade"] == tipohosp) & (df["tipo_gestao"] == gestao)]

        ### INDICADOR: QNTD DE HOSPITAIS
        qnt_hospitais = len(df_filtrado)

        ### INDICADOR: TEMPO MEDIO
        media = df_filtrado["tempo_medio_espera_min"].mean()
        if pd.isna(media):
            tempo_medio = "00:00"
        else:
            total_minutos = int(media)
            horas = total_minutos // 60
            minutos = total_minutos % 60
            tempo_medio = f"{horas:02d}:{minutos:02d}"

        ### INDICADORES: QNTD ATENDIMENTOS E GASTOS: 

        qntd_atendimentos = df_filtrado['qtd_atendimentos_mes'].sum()
        gastos_locais = f"R$ {df_filtrado['gastos_mensais_R$'].sum()/100:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        gasto_sus = f"R$ {df_filtrado['repasses_sus_R$'].sum()/100:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


        ### INDICADOR: QNTD LEITO + GRAFICO
        qntd_leitos = df_filtrado["qtd_leitos"].sum()

        df_filtrado["ocupados"] = df_filtrado["qtd_leitos"] * (df_filtrado["ocupacao_perc"] / 100)
        df_filtrado["disponiveis"] = df_filtrado["qtd_leitos"] - df_filtrado["ocupados"]

        qntd_leitos_ocupados = round(df_filtrado["ocupados"].sum())
        qntd_leitos_disponiveis = round(df_filtrado["disponiveis"].sum())

        disponiveis_str = f"▲ {int(qntd_leitos_disponiveis)}"
        ocupados_str = f"▼ {int(qntd_leitos_ocupados)}"

        graficoleitos = dcc.Graph(
            figure=go.Figure(data=[
                    go.Bar(name='Disponíveis', x=["Leitos"], y=[qntd_leitos_disponiveis], marker_color='green'),
                    go.Bar(name='Ocupados', x=["Leitos"], y=[qntd_leitos_ocupados], marker_color='red')
                ]
            ).update_layout(
                barmode='stack',
                height=120,
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showticklabels=False, showgrid=False),
                yaxis=dict(showticklabels=False, showgrid=False)
            ),
            config={"displayModeBar": False},
            style={"width": "100%"}
        )

        return [qnt_hospitais, ocupados_str, disponiveis_str, qntd_leitos,  qntd_atendimentos, tempo_medio, gastos_locais,  gasto_sus, graficoleitos]
    else:
        return ["0", "▼ 0%", "▲ 0%", "0", "0", "00:00", "R$ 000.000,00", "R$ 000.000,00", dcc.Graph(     # graph-leitos (vazio)
            figure=go.Figure().update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showticklabels=False),
                yaxis=dict(showticklabels=False),
                margin=dict(l=0, r=0, t=0, b=0)
            ),
            config={"displayModeBar": False},
            style={"height": "120px"}
        )
    ]


@app.callback(
    Output("tabela-hospitais", "children"),
    Input("dropdown-estado", "value"), 
)
def atualizar_tabela(estado):
    if estado: 
        df_filtrado = df[df["estado"] == estado] if estado else df
        df_visivel = df_filtrado[[
            "nome_hospital", "cidade", "qtd_leitos", "ocupacao_perc",
            "taxa_mortalidade_%", "tempo_medio_espera_min", "indice_satisfacao"
        ]].copy()

        df_visivel = df_visivel.rename(columns={
            "nome_hospital": "Hospital",
            "cidade": "Cidade",
            "qtd_leitos": "Leitos",
            "ocupacao_perc": "Ocupação (%)",
            "taxa_mortalidade_%": "Mortalidade (%)",
            "tempo_medio_espera_min": "Espera (min)",
            "indice_satisfacao": "Satisfação"
        })

        def cor_ocup(x):
            if x < 50: return f"🟢 {x:.0f}%"
            elif x < 80: return f"🟡 {x:.0f}%"
            else: return f"🔴 {x:.0f}%"

        def cor_mortal(x):
            if x < 1.5: return f"🟢 {x:.1f}%"
            elif x >= 1.5 and x <2: return f"🟡 {x:.1f}%"
            else: return f"🔴 {x:.1f}%"

        def tempo_fmt(m):
            try:
                m = float(m)
                return f"{int(m):02d}:{int((m - int(m)) * 60):02d}"
            except:
                return "00:00"

        def estrelas(nota):
            try:
                return f"{nota:.1f}/5 ⭐"
            except:
                return "N/A"

        df_visivel["Ocupação"] = df_visivel["Ocupação (%)"].apply(cor_ocup)
        df_visivel["Mortalidade"] = df_visivel["Mortalidade (%)"].apply(cor_mortal)
        df_visivel["Temp espera"] = df_visivel["Espera (min)"].apply(tempo_fmt)
        df_visivel["Satisfação"] = df_visivel["Satisfação"].apply(estrelas)
        df_final = df_visivel[["Hospital", "Cidade", "Leitos", "Ocupação", "Mortalidade", "Temp espera", "Satisfação"]]


        tabela = dash_table.DataTable(
            columns=[{"name": col, "id": col, "presentation": "markdown"} for col in df_final.columns],
            data=df_final.to_dict("records"),
            style_table={"overflowX": "auto"},
            page_size=8,
            style_cell={
                "textAlign": "center",
                "padding": "6px",
                "fontSize": "14px",
                "fontFamily": "Arial"
            },
            style_header={
                "backgroundColor": "#1E90FF",
                "color": "white",
                "fontWeight": "bold"
            }
        )

        return html.Div(tabela)



@app.callback(
    Output("mapa", "figure"),
    Input("filtrar-mapa", "value")
)
def atualizar_mapa(coluna):
    df_estado = df.copy()
            
    agrupado = df_estado.groupby("estado")[[coluna]].mean().reset_index()

    fig = go.Figure(go.Choropleth(
        geojson=geojson_estados,
        locations=agrupado["estado"],
        z=agrupado[coluna],
        featureidkey="properties.sigla",
        colorscale="Blues",
        hovertemplate="%{location}<br>" + f"{coluna.replace('_', ' ').title()}: " + "%{z}<extra></extra>",
        showscale=False
    )).update_layout(
        title=f"Mapa: {coluna.replace('_', ' ').title()}",
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        height=400,
    )

    fig.update_geos(fitbounds="locations", visible=False)
    
    return fig


@app.callback(
    Output("filadeespera", "figure"),
    Output("medico-espera", "figure"),
    Output("gestao-ocupacao", "figure"),

    Input("dropdown-estado", "value"),
    Input("dropdown-gestao", "value"),
)

def atualizar_graficos(estado, gestao):
    df_filtrado = df[(df["estado"] == estado) & (df["tipo_gestao"] == gestao)]

    ### GRAFICO BARRA FILA DE ESPERA POR UNIDADE
    df1 = df_filtrado.groupby(["tipo_unidade"])["tempo_medio_espera_min"].mean().reset_index()
    fig1 = px.bar(
        df1, 
        x="tipo_unidade", 
        y="tempo_medio_espera_min",
    ).update_layout(
        title="Fila de Espera X Unidade",
        xaxis_title="Tipo da Unidade",
        yaxis_title="Tempo de Espera (min)",
        xaxis_tickangle=0, 
        height=500,
        margin=dict(t=40, l=20, r=20, b=20)
    )   

    ### GRAFICO DISPERSAO MEDICOS X ESPERA
    df2 = df_filtrado.groupby(["qtd_medicos"])["tempo_medio_espera_min"].mean().reset_index()
    fig2 = px.scatter(
        df2, 
        x="qtd_medicos", 
        y="tempo_medio_espera_min",
    ).update_layout(
        title="Médicos X Tempo de espera",
        xaxis_title="Quantidade de Médicos",
        yaxis_title="Tempo de Espera (min)",
        xaxis_tickangle=0,
        height=500,
        margin=dict(t=40, l=20, r=20, b=20)
    )  

    ### GRAFICO BARRA OCUPAÇÃO X GESTAO
    df_filtrado = df[(df["estado"] == estado)]
    df3 = df_filtrado.groupby(["tipo_gestao"])["ocupacao_perc"].mean().reset_index()
    fig3 = px.bar(
        df3, 
        x="tipo_gestao", 
        y="ocupacao_perc",
    ).update_layout(
        title="Ocupação x Gestao",
        xaxis_title="Tipo de gestão",
        yaxis_title="Taxa de ocupação (%)",
        xaxis_tickangle=0,  
        height=500,
        margin=dict(t=40, l=20, r=20, b=20)
    )  
    return fig1, fig2, fig3


if __name__ == '__main__':
    app.run_server(debug=True, port=int(os.environ.get("PORT", 8050)), host='0.0.0.0')