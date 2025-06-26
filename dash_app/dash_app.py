from dash import Dash, html, dcc, callback, Output, Input
from utils.plotly_figures import histograma_genero
import plotly.express as px
import pandas as pd

df = pd.read_csv('dados/dataframe.csv')
colunas_numericas = [col for col in df.select_dtypes(include=['float64', 'int64']).columns]
niveis_obesidade = df['Nível de Obesidade'].dropna().unique()

app = Dash(__name__)
# ... layout e callbacks usando histograma_genero(df, coluna, niveis_selecionados)