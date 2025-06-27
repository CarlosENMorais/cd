import plotly.graph_objects as go
import pandas as pd

def plot_stacked_categoricas(df, qualiVars, obesity_levels, selected_levels):
    """
    df: DataFrame original
    qualiVars: lista com o nome das variáveis categóricas a serem plotadas
    obesity_levels: nome da coluna dos níveis de obesidade
    selected_levels: lista dos níveis de obesidade selecionados pelo usuário
    palette: dict categoria->cor (como no seu exemplo)
    """
    palette = {
        'Sempre': '#4CAF50', 'Frequentemente': '#81C784', 'Raramente': '#FFEB3B',
        'Não': '#E57373', 'Sim': '#64B5F6',
        'Automóvel': '#9E9E9E', 'Motocicleta': '#795548', 'Bicicleta': '#66BB6A',
        'Caminhada': '#43A047', 'Transporte Público': '#03A9F4',
        'Masculino': '#2196F3', 'Feminino': '#E91E63',
        'Peso Insuficiente': '#81D4FA', 'Peso Normal': '#AED581',
        'Sobrepeso Nível I': '#FFF176', 'Sobrepeso Nível II': '#FFB74D',
        'Obesidade Tipo I': '#FF8A65', 'Obesidade Tipo II': '#E57373', 'Obesidade Tipo III': '#C62828',
    }
    # Filtra o DataFrame pelo(s) nível(is) de obesidade
    df_sub = df[df[obesity_levels].isin(selected_levels)]
    total = len(df_sub)

    # Prepara a estrutura dos dados
    # Dicionário: var -> Series com contagem por categoria, já normalizada em porcentagem
    var_percent = {}
    categories_all = set()
    for var in qualiVars:
        # Conta e normaliza para porcentagem
        counts = df_sub[var].value_counts(normalize=True) * 100
        var_percent[var] = counts
        categories_all.update(counts.index.tolist())

    categories_all = list(categories_all)
    # Ordena as categorias por sua paleta se quiser, ou alfabeticamente
    categories_all.sort(key=lambda x: str(x))

    # Cria um trace para cada categoria, para todas as variáveis
    traces = []
    for cat in categories_all:
        traces.append(
            go.Bar(
                x=[var_percent[var].get(cat, 0) for var in qualiVars],  # % daquela categoria em cada variável
                y=qualiVars,
                orientation='h',
                name=str(cat),
                marker=dict(color=palette.get(cat, '#cccccc')),
                text=[f"{var_percent[var].get(cat, 0):.1f}%" if var_percent[var].get(cat, 0) >= 3 else "" for var in qualiVars], # só mostra rótulo acima de 3%
                textposition="inside",
                insidetextanchor="middle",
                hovertemplate='%{y}<br>%{x:.1f}%<br>Categoria: '+str(cat)
            )
        )

    fig = go.Figure(traces)
    fig.update_layout(
        barmode="stack",
        # height=50 + 60 * len(qualiVars),
        xaxis=dict(
            title='Porcentagem (%)',
            range=[0, 100],
            showgrid=True,
            showline=True,
            showticklabels=True,
            tickformat=',.0f'
        ),
        yaxis=dict(
            title='Variáveis',
            automargin=True,
            categoryorder='array',
            categoryarray=qualiVars
        ),
        legend=dict(
            title='Categorias',
            traceorder="normal"
        ),
        template='plotly_white',
        margin=dict(l=0, r=0, t=0, b=0),
        # margin=dict(l=20, r=20, t=40, b=20),  # margens menores
        # padding=dict(l=1, r=1, t=1, b=1),   
        # width=800,  # largura fixa
        # height=500,  # altura fixa
        autosize=True  # desabilita redimensionamento automático
    )
    return fig