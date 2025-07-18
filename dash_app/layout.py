from dash import html, dcc
from utils.ml import gerar_tendencia

def criar_layout(col_numerics, col_categorics, levels_obesity, df):
    return html.Div([     
        html.Div([
            html.Div([
                html.H1("Hábitos Indicadores de Obesidade", style={'text-align': 'left', 'margin': '0px', 'flex': '0 0 auto'}),
                html.P("por: Carlos Morais", style={'text-align': 'left', 'margin': '0px', 'flex': '1'}),
            ],className="title"),
            
            html.P(["Este dashboard explora dados de 2.111 participantes para investigar correlações entre obesidade e hábitos de vida. Os dados são do Kaggle e integram um projeto academico de Data Science. As visualizações foram feitas com Plotly e o dashboard desenvolvido com Dash."
            ], style={'margin': '0', 'lineHeight': '1.4'})
        ], className="header"),   
        
        
        html.Div([
            # CONTROLES
            html.Div([
                html.H3("Controles", className="card-header"),
                html.Div([
                    html.Label("Níveis de Obesidade:", className="label"),
                    dcc.Checklist(
                        id='obesidade-checklist',
                        options=[{'label': nivel, 'value': nivel} for nivel in levels_obesity],
                        value=list(levels_obesity),
                        inline=False
                    ),
                    html.Br(),

                    html.Div([
                        html.Div([
                            html.Label("Variável Numérica:", className="label"),
                            dcc.Dropdown(
                                id='dropdown-numeric',
                                options=[{'label': col, 'value': col} for col in col_numerics],
                                value=col_numerics[0]
                            ),
                        ], className="dropdown-col"),

                        html.Div([
                            html.Label("Variável Categórica:", className="label"),
                            dcc.Dropdown(
                                id='dropdown-categoric',
                                options=[{'label': col, 'value': col} for col in col_categorics],
                                value=col_categorics[0]
                            ),
                        ], className="dropdown-col"),

                    ], className="dropdown-col"),

                    html.Div([
                        html.H3("Participantes", className="card-header"),
                        html.Div([
                            html.H1(id="participantes", className="card-header"),
                        ],className="card-body"),
                    ],className="card"),
                    html.Div([
                        html.H3("Média Var. Numérica", className="card-header"),
                        html.Div([
                            html.H1(id="media", className="card-header"),
                        ],className="card-body"),
                    ],className="card"),
                    html.Div([
                        html.H3(["Correlação", html.Br(), "Numéricas x Categóricas"], className="card-header"),
                        html.Div([
                            html.H1(id="corr-num-cat", className="card-header"),
                        ],className="card-body"),
                    ],className="card"),
                    html.Div([
                        html.H3(["Correlação", html.Br(), "Eixo X e Eixo Y"], className="card-header"),
                        html.Div([
                            html.H1(id="corr-num", className="card-header"),
                        ],className="card-body"),
                    ],className="card"),


                ], className="card-body")
            ], className="controls"),

            html.Div([
                # PRIMEIRA LINHA: SCATTER + HISTOGRAMA
                html.Div([
                    html.Div([
                        html.H3(id='title-boxplot', className="card-header"),
                        html.Div([
                            # dcc.Graph(id='boxplot', style={'height': '60vh'})
                            dcc.Graph(id='boxplot', config={"responsive": True})
                        ], className="card-body")
                    ], className="card col-one-third"),
                    
                    html.Div([
                        html.H3("Distribuição de Variáveis Categóricas por Nível de Obesidade", className="card-header"),
                        html.Div([
                            # dcc.Graph(id='stacked-categoricas', style={'height': '60vh'})
                            dcc.Graph(id='stacked-categoricas', config={"responsive": True})
                        ], className="card-body")
                    ], className="card col-two-thirds"),

                    

                ], className="row"),
                
                # SEGUNDA LINHA: STACKED + BOXPLOT
                html.Div([

                    html.Div([
                        html.H3(id='titulo-histograma', className="card-header"),
                        html.Div([
                            # dcc.Graph(id='histograma', style={'height': '40vh'}),
                            dcc.Graph(id='histograma', config={"responsive": True}),
                            dcc.Checklist(
                                id='fixar-eixo-y-toggle',
                                options=[{'label': 'Fixar eixo Y', 'value': 'fixo'}],
                                value=['fixo'],
                                inline=True
                            )
                        ], className="card-body")
                    ], className="card col-half"),

                    
                    html.Div([
                        html.H3("Importância das Variáveis por Tendência", className="card-header"),
                        html.Div([                   
                            # dcc.Graph(id='meu-grafico', figure=gerar_scatter(df), style={'height': '40vh'}),
                            dcc.Graph(figure=gerar_tendencia(), config={"responsive": True, 'displayModeBar': False,}),
                            
                        ], className="card-body")
                    ], className="card col-half"),

                ], className="row"),
            ],className="col"),
        ],className="row"),
        
    ], className="main-div")        
    # ], style={'max-width': 'auto', 'margin': '0 auto', 'padding': '20px'})