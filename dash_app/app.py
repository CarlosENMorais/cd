import pandas as pd
from dash import Dash
from dash_app.layout import criar_layout
from dash_app.callbacks import registrar_callbacks

# Carrega os dados
df = pd.read_csv('data/dataframe.csv')
df['IMC'] = df['Peso (kg)'] / (df['Altura (m)']**2)
colunas_numericas = [col for col in df.select_dtypes(include=['float64', 'int64']).columns]
niveis_obesidade = df['Nível de Obesidade'].dropna().unique()
colunas_categoricas = [col for col in df.columns
                       if (df[col].dtype == 'object' or str(df[col].dtype).startswith('category'))
                       and col != 'Frequência de Atividade Física']

# Inicializa o Dash
app = Dash(__name__)

# Define o layout
app.layout = criar_layout(colunas_numericas, 
                          colunas_categoricas, 
                          niveis_obesidade, 
                          df)

# Registra os callbacks
registrar_callbacks(app, 
                    df,
                    colunas_categoricas,
                    niveis_obesidade)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
