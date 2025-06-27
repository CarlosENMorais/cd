import plotly.graph_objs as go
import pandas as pd

def gerar_scatter(df, numeric_varX, numeric_varY, categoric_var, niveis_selecionados):
    categorias = df[categoric_var].dropna().unique()

    scatters = []
    for categoria in categorias:
        y_data = df.loc[(df[categoric_var] == categoria) & 
                        (df['Nível de Obesidade'].isin(niveis_selecionados)), numeric_varY]
        x_data = df.loc[(df[categoric_var] == categoria) &
                        (df['Nível de Obesidade'].isin(niveis_selecionados)), numeric_varX]
        if (not y_data.empty) and (not x_data.empty):
            scatters.append(
                go.Scatter(
                    x=x_data,
                    y=y_data,
                    mode='markers',
                    name=categoria,
                    marker=dict(size=8, opacity=0.6)
                )
            )

    layout = go.Layout(
        xaxis=dict(title=numeric_varX),
        yaxis=dict(title=numeric_varY),
        legend=dict(x=0.02, y=0.98),
        template='plotly_white'
    )

    fig = go.Figure(data=scatters, layout=layout)

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        autosize=True,
    )
    
    return fig
