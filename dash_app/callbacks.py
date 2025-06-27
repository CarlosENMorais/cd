import numpy as np
from dash import Output, Input
from dash import callback  # Dash >=2.7.0
from utils.histograma import gerar_histograma
from utils.boxplot import gerar_boxplot_frequencia
from utils.stackedBars import plot_stacked_categoricas
from utils.scatter import gerar_scatter


def registrar_callbacks(app, df, colunas_categoricas, niveis_obesidade):
    @app.callback(
        [
            Output('histograma', 'figure'),
            Output('titulo-histograma', 'children'),

            Output('boxplot', 'figure'),
            Output('title-boxplot', 'children'),
        ],
        Input('dropdown-numeric', 'value'),
        Input('dropdown-categoric', 'value'),
        Input('obesidade-checklist', 'value'),
        Input('fixar-eixo-y-toggle', 'value')
    )
    def cb_boxplot_histogram(numeric_var, categoric_var, niveis_selecionados, fixar_eixo_y_lista):
        fixar_eixo_y = 'fixo' in fixar_eixo_y_lista if fixar_eixo_y_lista else False
        
        fig_hist = gerar_histograma(df,
                                numeric_var,
                                categoric_var,
                                niveis_selecionados,
                                fixar_eixo_y)
        title_hist = f'Histograma de {numeric_var} agrupado por {categoric_var}'
        
        fig_box = gerar_boxplot_frequencia(df, categoric_var, numeric_var)
        title_box = f'Boxplot da {numeric_var} agrupado por {categoric_var}'
        
        return fig_hist, title_hist, fig_box, title_box
       
    @app.callback(
        Output('stacked-categoricas', 'figure'),
        Input('obesidade-checklist', 'value')
    )
    def update_stacked_categoricas(niveis_selecionados):
        return plot_stacked_categoricas(df, 
                                        colunas_categoricas, 
                                        'Nível de Obesidade', 
                                        niveis_selecionados)
    
    @app.callback([
            Output('scatter','figure'),
            Output('titulo-scatter', 'children'),
        ],
        Input('dropdown-categoric', 'value'),
        Input('dropdown-scatter-axisX', 'value'),
        Input('dropdown-scatter-axisY', 'value'),
        Input('obesidade-checklist', 'value'),
    )
    def update_scatter(categoric_var, numeric_varX, numeric_varY, niveis_selecionados):
        fig_scatter = gerar_scatter(df, numeric_varX, numeric_varY, categoric_var, niveis_selecionados)
        title_scatter = f'Agrupamento de {categoric_var} dentro de {numeric_varX} vs {numeric_varY}'
        return fig_scatter, title_scatter
    
    @app.callback([
            Output("participantes", "children"),
            Output("media","children"),
            Output("corr-num", "children"),
            Output("corr-num-cat", "children"),
        ],
        Input('dropdown-categoric', 'value'),
        Input('dropdown-numeric', 'value'),
        Input('dropdown-scatter-axisX', 'value'),
        Input('dropdown-scatter-axisY', 'value'),
        Input('obesidade-checklist', 'value'),
    )
    def update_KPA(categoric_var, numeric_var, numeric_varX, numeric_varY, niveis_selecionados):
        df3 = df[df['Nível de Obesidade'].isin(niveis_selecionados)]
        total = len(df3)
        media = round(df[numeric_var].mean(),3)
        corr_num = round(df[numeric_varX].corr(df[numeric_varY], method='pearson'),3)
        corr_num_cat = round(eta_squared(df, categoric_var, numeric_var),3)
        return total, media, corr_num, corr_num_cat
    
    def eta_squared(df, categoric_col, numeric_col):
        categories = df[categoric_col].dropna().unique()
        overall_mean = df[numeric_col].mean()
        total_ss = ((df[numeric_col] - overall_mean) ** 2).sum()
        
        between_ss = 0
        for cat in categories:
            group = df[df[categoric_col] == cat][numeric_col]
            group_size = len(group)
            group_mean = group.mean()
            between_ss += group_size * (group_mean - overall_mean) ** 2

        eta2 = between_ss / total_ss if total_ss != 0 else np.nan
        return eta2