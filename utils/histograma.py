import plotly.graph_objs as go
import numpy as np
from plotly.colors import DEFAULT_PLOTLY_COLORS

def gerar_histograma(df, numeric_var, categoric_var, niveis_selecionados, fixar_eixo_y=True):
    
    fig = go.Figure()
    categorias = df[categoric_var].dropna().unique()

    start = df[numeric_var].min()
    end = df[numeric_var].max()
    num_bins = 30
    if end == start:
        bin_size = 1
    else:
        bin_size = (end - start) / num_bins
    bins = np.arange(start, end + bin_size, bin_size)

    y_max = 0
    if fixar_eixo_y:
        for categoria in categorias:
            dados = df[
                (df[categoric_var] == categoria) &
                (df['Nível de Obesidade'].isin(niveis_selecionados))
            ][numeric_var].dropna()
            counts, _ = np.histogram(dados, bins=bins)
            if len(counts) > 0:
                y_max = max(y_max, counts.max())

    color_palette = DEFAULT_PLOTLY_COLORS  # ou defina sua lista de cores
    for i, categoria in enumerate(categorias):
        cor = color_palette[i % len(color_palette)]
        dados_filtrados = df[
            (df[categoric_var] == categoria) &
            (df['Nível de Obesidade'].isin(niveis_selecionados))
        ][numeric_var].dropna()
        fig.add_trace(go.Histogram(
            x=dados_filtrados,
            name=categoria,
            opacity=0.7,
            marker_color=cor,
            xbins=dict(start=start, end=end, size=bin_size)
        ))

    fig.update_layout(
        barmode='overlay',
        title=None,
        xaxis_title=numeric_var,
        # height=400,
        # width=800,  # largura fixa
        # height=500,  # altura fixa
        autosize=True,  # desabilita redimensionamento automático
        margin=dict(l=0, r=0, t=0, b=0),
    )
    fig.update_xaxes(range=[start, end])
    if fixar_eixo_y:
        fig.update_yaxes(range=[0, y_max])

    return fig