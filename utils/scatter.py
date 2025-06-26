import plotly.graph_objs as go
import pandas as pd

def gerar_scatter(df):
    # Supondo que df já contém as colunas 'Idade', 'Tempo em Tecnologias' e 'Gênero'
    # Exemplo de valores possíveis para 'Gênero': 'Masculino', 'Feminino'

    # Separe os dados por gênero
    df_masc = df[df['Gênero'] == 'Masculino']
    df_fem = df[df['Gênero'] == 'Feminino']

    # Calcule a média de Tempo em Tecnologias por idade para cada gênero
    media_masc = df_masc.groupby('Idade')['Tempo em Tecnologias'].mean().reset_index()
    media_fem = df_fem.groupby('Idade')['Tempo em Tecnologias'].mean().reset_index()

    # Scatter Masculino
    scatter_masc = go.Scatter(
        x=df_masc['Idade'],
        y=df_masc['Tempo em Tecnologias'],
        mode='markers',
        name='Masculino - Dados Individuais',
        marker=dict(color='blue', size=8, opacity=0.6)
    )

    # Linha Média Masculino
    linha_masc = go.Scatter(
        x=media_masc['Idade'],
        y=media_masc['Tempo em Tecnologias'],
        mode='lines+markers',
        name='Masculino - Média',
        line=dict(color='blue', width=3, dash='solid'),
        marker=dict(color='blue', size=10, symbol='circle-open')
    )

    # Scatter Feminino
    scatter_fem = go.Scatter(
        x=df_fem['Idade'],
        y=df_fem['Tempo em Tecnologias'],
        mode='markers',
        name='Feminino - Dados Individuais',
        marker=dict(color='red', size=8, opacity=0.6)
    )

    # Linha Média Feminino
    linha_fem = go.Scatter(
        x=media_fem['Idade'],
        y=media_fem['Tempo em Tecnologias'],
        mode='lines+markers',
        name='Feminino - Média',
        line=dict(color='red', width=3, dash='solid'),
        marker=dict(color='red', size=10, symbol='diamond-open')
    )

    layout = go.Layout(
        title='Idade vs Tempo em Tecnologias por Gênero',
        xaxis=dict(title='Idade'),
        yaxis=dict(title='Tempo em Tecnologias'),
        legend=dict(x=0.02, y=0.98),
        template='plotly_white'
    )

    fig = go.Figure(data=[scatter_masc, linha_masc, scatter_fem, linha_fem], layout=layout)
    
    return fig
