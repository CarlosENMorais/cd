from dash import Output, Input
from dash import callback  # Dash >=2.7.0
from utils.histograma import gerar_histograma
from utils.boxplot import gerar_boxplot_frequencia
from utils.stackedBars import plot_stacked_categoricas


def registrar_callbacks(app, df, generos, colunas_categoricas, niveis_obesidade):
    @app.callback(
        Output('histograma', 'figure'),
        Input('coluna-dropdown', 'value'),
        Input('obesidade-checklist', 'value'),
        Input('fixar-eixo-y-toggle', 'value')
    )
    def atualizar_grafico(coluna, niveis_selecionados, fixar_eixo_y_lista):
        fixar_eixo_y = 'fixo' in fixar_eixo_y_lista if fixar_eixo_y_lista else False
        return gerar_histograma(df, 
                                coluna, 
                                niveis_selecionados, 
                                generos, 
                                fixar_eixo_y)

    @app.callback(
        Output('boxplot-categoria-x', 'figure'),
        Input('dropdown-categoria-x', 'value')
    )   
    def atualizar_boxplot(categoria_x):
        return gerar_boxplot_frequencia(df, categoria_x)
    
    @app.callback(
        Output('stacked-categoricas', 'figure'),
        Input('obesidade-checklist', 'value')
    )
    def update_stacked_categoricas(niveis_selecionados):
        return plot_stacked_categoricas(df, 
                                        colunas_categoricas, 
                                        'Nível de Obesidade', 
                                        niveis_selecionados)
    