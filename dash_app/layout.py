# import dash_bootstrap_components as dbc
# from dash import html, dcc
# from utils.scatter import gerar_scatter

# def criar_layout(colunas_numericas, colunas_categoricas, niveis_obesidade, df):
#     # CARD DE CONTROLES (filtros)
#     card_controles = dbc.Card([
#         dbc.CardHeader("Controles"),
#         dbc.CardBody([
#             html.Label("Níveis de Obesidade:"),
#             dcc.Checklist(
#                 id='obesidade-checklist',
#                 options=[{'label': nivel, 'value': nivel} for nivel in niveis_obesidade],
#                 value=list(niveis_obesidade),
#                 inline=True
#             ),
#             html.Br(),
#             html.Label("Variável Numérica:"),
#             dcc.Dropdown(
#                 id='coluna-dropdown',
#                 options=[{'label': col, 'value': col} for col in colunas_numericas],
#                 value=colunas_numericas[0]
#             ),
#             html.Br(),
#             html.Label("Variável Categórica:"),        
#             dcc.Dropdown(
#                 id='dropdown-categoria-x',
#                 options=[{'label': col, 'value': col} for col in colunas_categoricas],
#                 value=colunas_categoricas[0]
#             ),
#             html.Br(),
#             dcc.Checklist(
#                 id='fixar-eixo-y-toggle',
#                 options=[{'label': 'Fixar eixo Y', 'value': 'fixo'}],
#                 value=['fixo'],
#                 inline=True
#             )
#         ])
#     ], className="mb-4")

#     # CARD HISTOGRAMA
#     card_histograma = dbc.Card([
#         dbc.CardHeader("Histograma"),
#         dbc.CardBody([
#             dcc.Graph(id='histograma')
#         ])
#     ], className="mb-4")

#     # CARD BOXPLOT
#     card_boxplot = dbc.Card([
#         dbc.CardHeader("Boxplot por Categoria"),
#         dbc.CardBody([
#             dcc.Graph(id='boxplot-categoria-x')
#         ])
#     ], className="mb-4")

#     # CARD SCATTER
#     card_scatter = dbc.Card([
#         dbc.CardHeader("Gráfico de Dispersão"),
#         dbc.CardBody([
#             dcc.Graph(id='meu-grafico', figure=gerar_scatter(df))
#         ])
#     ], className="mb-4")
    
#     # CARD STACKED BARS
#     card_stacked = dbc.Card([
#         dbc.CardHeader("Distribuição de Variáveis Categóricas por Nível de Obesidade"),
#         dbc.CardBody([
#             dcc.Graph(
#                 id='stacked-categoricas',
#                 config={'displayModeBar': True},
#                 style={'height': '600px'}
#             )
#         ])
#     ])
#     # ], className="mb-4")

#     # ORGANIZAÇÃO DO LAYOUT EM GRID
#     return dbc.Container(
#         [
#             html.H1("Meu Dashboard"),
#             html.Hr(),
#             dbc.Row(
#                 [
#                     dbc.Col(card_controles, md=12),
#                 ], 
#                 align="center"),
#             dbc.Row(
#                 [
#                     dbc.Col(card_scatter, md=6),
#                     dbc.Col(card_histograma, md=6)
#                 ], 
#                 align="center"),
#             dbc.Row(
#                 [
#                     dbc.Col(card_stacked, md=8),
#                     dbc.Col(card_boxplot, md=4),
#                 ]
#             ),
#         ], 
#         fluid=False
#     )


import dash_bootstrap_components as dbc
from dash import html, dcc
from utils.scatter import gerar_scatter

def criar_layout(colunas_numericas, colunas_categoricas, niveis_obesidade, df):
    # CARD DE CONTROLES (filtros)
    card_controles = dbc.Card([
        dbc.CardHeader("Controles"),
        dbc.CardBody([
            html.Label("Níveis de Obesidade:"),
            dcc.Checklist(
                id='obesidade-checklist',
                options=[{'label': nivel, 'value': nivel} for nivel in niveis_obesidade],
                value=list(niveis_obesidade),
                inline=True
            ),
            html.Br(),
            html.Label("Variável Numérica:"),
            dcc.Dropdown(
                id='coluna-dropdown',
                options=[{'label': col, 'value': col} for col in colunas_numericas],
                value=colunas_numericas[0]
            ),
            html.Br(),
            html.Label("Variável Categórica:"),        
            dcc.Dropdown(
                id='dropdown-categoria-x',
                options=[{'label': col, 'value': col} for col in colunas_categoricas],
                value=colunas_categoricas[0]
            ),
            html.Br(),
            dcc.Checklist(
                id='fixar-eixo-y-toggle',
                options=[{'label': 'Fixar eixo Y', 'value': 'fixo'}],
                value=['fixo'],
                inline=True
            )
        ])
    ], className="mb-4")

    # CARD HISTOGRAMA - com largura E altura fixas
    card_histograma = dbc.Card([
        dbc.CardHeader("Histograma"),
        dbc.CardBody([
            dcc.Graph(
                id='histograma',
                style={
                    'height': '400px',
                    'width': '100%'  # 100% do container pai, não da tela
                },
                config={
                    'responsive': True,
                    'displayModeBar': True
                }
            )
        ])
    ], className="mb-4")

    # CARD BOXPLOT - com largura E altura fixas
    card_boxplot = dbc.Card([
        dbc.CardHeader("Boxplot por Categoria"),
        dbc.CardBody([
            dcc.Graph(
                id='boxplot-categoria-x',
                style={
                    'height': '400px',
                    'width': '100%'
                },
                config={
                    'responsive': True,
                    'displayModeBar': True
                }
            )
        ])
    ], className="mb-4")

    # CARD SCATTER - com largura E altura fixas
    card_scatter = dbc.Card([
        dbc.CardHeader("Gráfico de Dispersão"),
        dbc.CardBody([
            dcc.Graph(
                id='meu-grafico', 
                figure=gerar_scatter(df),
                style={
                    'height': '400px',
                    'width': '100%'
                },
                config={
                    'responsive': True,
                    'displayModeBar': True
                }
            )
        ])
    ], className="mb-4")
    
    # CARD STACKED BARS - com largura E altura fixas
    card_stacked = dbc.Card([
        dbc.CardHeader("Distribuição de Variáveis Categóricas por Nível de Obesidade"),
        dbc.CardBody([
            dcc.Graph(
                id='stacked-categoricas',
                style={
                    'height': '500px',
                    'width': '100%'
                },
                config={
                    'responsive': True,
                    'displayModeBar': True
                }
            )
        ])
    ], className="mb-4")

    # ORGANIZAÇÃO DO LAYOUT EM GRID - COM CONTROLE DE LARGURA
    return dbc.Container([
        html.H1("Meu Dashboard", className="text-center mb-4"),
        html.Hr(),
        
        # Linha dos controles
        dbc.Row([
            dbc.Col(card_controles, width=12)
        ], className="mb-3"),
        
        # Linha com scatter e histograma - FORÇANDO LARGURA
        dbc.Row([
            dbc.Col(
                card_scatter, 
                width=6,
                style={'maxWidth': '50%', 'flex': '0 0 50%'}  # Força 50% da largura
            ),
            dbc.Col(
                card_histograma, 
                width=6,
                style={'maxWidth': '50%', 'flex': '0 0 50%'}  # Força 50% da largura
            )
        ], className="mb-3", style={'display': 'flex', 'flexWrap': 'wrap'}),
        
        # Linha com stacked bar e boxplot - FORÇANDO LARGURA
        dbc.Row([
            dbc.Col(
                card_stacked, 
                width=8,
                style={'maxWidth': '66.66%', 'flex': '0 0 66.66%'}  # Força 2/3 da largura
            ),
            dbc.Col(
                card_boxplot, 
                width=4,
                style={'maxWidth': '33.33%', 'flex': '0 0 33.33%'}  # Força 1/3 da largura
            )
        ], className="mb-3", style={'display': 'flex', 'flexWrap': 'wrap'}),
        
    ], 
    fluid=True,
    style={
        'maxWidth': '1200px', 
        'margin': '0 auto',
        'padding': '20px'
    })