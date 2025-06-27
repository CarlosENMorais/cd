import plotly.graph_objs as go

def gerar_boxplot_frequencia(df, categoric_var, numeric_var):
    categorias = df[categoric_var].dropna().unique()
    # Garante ordem se for Categorical
    # if hasattr(df[categoric_var].dtype, 'categories'):
    #     categorias = df[categoric_var].cat.categories

    boxplots = []
    for categoria in categorias:
        y_data = df.loc[df[categoric_var] == categoria, numeric_var]
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
        # title=f'Boxplot da Frequência de Atividade Física por {categoric_var}',
        xaxis_title=categoric_var,
        yaxis_title=numeric_var,
        xaxis_tickangle=20,
        template='plotly_white',
        xaxis=dict(categoryorder='array', categoryarray=list(categorias)),
        # margin=dict(t=70, b=120)
        margin=dict(l=0, r=0, t=0, b=0),
        autosize=True,
    )
    return fig