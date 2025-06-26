import plotly.graph_objs as go

def gerar_boxplot_frequencia(df, coluna_categorica):
    categorias = df[coluna_categorica].dropna().unique()
    # Garante ordem se for Categorical
    if hasattr(df[coluna_categorica].dtype, 'categories'):
        categorias = df[coluna_categorica].cat.categories

    boxplots = []
    for categoria in categorias:
        y_data = df.loc[df[coluna_categorica] == categoria, 'Frequência de Atividade Física']
        if not y_data.empty:
            boxplots.append(
                go.Box(
                    y=y_data,
                    name=str(categoria),
                    boxmean='sd'
                )
            )
    fig = go.Figure(data=boxplots)
    fig.update_layout(
        title=f'Boxplot da Frequência de Atividade Física por {coluna_categorica}',
        xaxis_title=coluna_categorica,
        yaxis_title='Frequência de Atividade Física',
        xaxis_tickangle=20,
        template='plotly_white',
        xaxis=dict(categoryorder='array', categoryarray=list(categorias)),
        margin=dict(t=70, b=120)
    )
    return fig