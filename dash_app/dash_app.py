import dash
from dash import dcc, html, Output, Input
import plotly.graph_objs as go
import pandas as pd
import numpy as np

df = pd.read_csv('data/dataframe.csv')
colunas_numericas = [col for col in df.select_dtypes(include=['float64', 'int64']).columns]
niveis_obesidade = df['Nível de Obesidade'].dropna().unique()
generos = ['Masculino', 'Feminino']

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='coluna-dropdown',
        options=[{'label': col, 'value': col} for col in colunas_numericas],
        value=colunas_numericas[0]
    ),
        html.Div([
        dcc.Checklist(
            id='fixar-eixo-y-toggle',
            options=[{'label': 'Fixar eixo Y', 'value': 'fixo'}],
            value=['fixo'],
            inline=True
        )
    ], style={'textAlign': 'center'}),
    dcc.Graph(id='histograma'),
    html.Div([
        dcc.Checklist(
            id='obesidade-checklist',
            options=[{'label': nivel, 'value': nivel} for nivel in niveis_obesidade],
            value=list(niveis_obesidade),
            inline=True
        )
    ], style={'textAlign': 'center', 'margin': '10px'}),
])

@app.callback(
    Output('histograma', 'figure'),
    Input('coluna-dropdown', 'value'),
    Input('obesidade-checklist', 'value'),
    Input('fixar-eixo-y-toggle', 'value')
)
def atualizar_grafico_callback(coluna, niveis_selecionados, fixar_eixo_y_lista):
    fixar_eixo_y = 'fixo' in fixar_eixo_y_lista if fixar_eixo_y_lista else False
    return atualizar_grafico(coluna, niveis_selecionados, fixar_eixo_y)

def atualizar_grafico(coluna, niveis_selecionados, fixar_eixo_y=True):
    fig = go.Figure()

    df_completo_para_bins = df[coluna]
    start = df_completo_para_bins.min()
    end = df_completo_para_bins.max()
    num_bins = 30
    bin_size = (end - start) / num_bins
    bins = np.arange(start, end + bin_size, bin_size)

    y_max = 0
    if fixar_eixo_y:
        for genero in generos:
            dados = df[df['Gênero'] == genero][coluna].dropna()
            counts, _ = np.histogram(dados, bins=bins)
            y_max = max(y_max, counts.max())

    for genero, cor in zip(generos, ['#1f77b4', '#e377c2']):
        dados_filtrados = df[
            (df['Gênero'] == genero) &
            (df['Nível de Obesidade'].isin(niveis_selecionados))
        ][coluna].dropna()

        fig.add_trace(go.Histogram(
            x=dados_filtrados,
            name=genero,
            opacity=0.7,
            marker_color=cor,
            xbins=dict(start=start, end=end, size=bin_size)
        ))

    fig.update_layout(
        barmode='overlay',
        title=f'Distribuição de {coluna} por Gênero',
        xaxis_title=coluna,
        height=400
    )
    fig.update_xaxes(range=[start, end])
    if fixar_eixo_y:
        fig.update_yaxes(range=[0, y_max])

    return fig

if __name__ == '__main__':
    app.run(debug=True)