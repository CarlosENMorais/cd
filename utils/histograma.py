import plotly.graph_objs as go
import numpy as np

def gerar_histograma(df, coluna, niveis_selecionados, generos, fixar_eixo_y=True):
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