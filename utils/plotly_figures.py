import plotly.graph_objs as go

def histograma_genero(df, coluna, niveis_obesidade):
    fig = go.Figure()
    for genero, cor in zip(['Masculino', 'Feminino'], ['#1f77b4', '#e377c2']):
        dados = df[(df['Gênero'] == genero) & (df['Nível de Obesidade'].isin(niveis_obesidade))][coluna]
        fig.add_trace(go.Histogram(x=dados, name=genero, opacity=0.7, marker_color=cor))
    fig.update_layout(barmode='overlay', title=f'Distribuição de {coluna} por Gênero')
    return fig