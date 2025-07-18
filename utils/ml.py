# Importações das bibliotecas
import pandas as pd
import plotly.express as px

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split


def gerar_tendencia():
    # Carregamento do dataset
    df = pd.read_csv("data/dataframe.csv")

    # Remoção das colunas IMC e Peso
    df = df.drop(columns=["Weight", "BMI"], errors="ignore")

    # Criação do alvo binário: Obeso (1) ou Não Obeso (0)
    classes_obeso = [
        'Obesidade Tipo I', 
        'Obesidade Tipo II', 
        'Obesidade Tipo III'
    ]
    df["Obeso"] = df["Nível de Obesidade"].apply(lambda x: 1 if x in classes_obeso else 0)

    # Separação em variáveis independentes e alvo
    X = df.drop(columns=["Nível de Obesidade", "Obeso"])
    y = df["Obeso"]

    # Define manualmente as variáveis categóricas e numéricas
    cat_cols = [
        "Gênero",
        "Histórico Familiar de Sobrepeso",
        "Consumo Frequente de Alimentos Calóricos",
        "Consumo Entre Refeições",
        "Fumante",
        "Controle de Calorias",
        "Consumo de Álcool",
        "Meio de Transporte Principal"
    ]

    num_cols = [
        "Idade",
        "Altura (m)",
        "Frequência de Consumo de Verduras",
        "Número de Refeições Principais por Dia",
        "Frequência de Atividade Física",
        "Tempo em Tecnologias",
        "Consumo Diário de Água"
    ]

    # Garante que colunas removidas não estejam em X
    X = df[cat_cols + num_cols]
    y = df["Obeso"]

    # Criação do pré-processador: escala os numéricos e aplica one-hot nos categóricos
    preprocessor = ColumnTransformer(transformers=[
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", drop='if_binary'), cat_cols)
    ])

    # Aplica o pré-processador ao conjunto de entrada X
    X_processed = preprocessor.fit_transform(X)
    feature_names = preprocessor.get_feature_names_out()

    # 5. Treinamento do modelo Random Forest
    model = RandomForestClassifier(random_state=42)
    model.fit(X_processed, y)

    # # Cria o explainer baseado no modelo de árvore
    # explainer = shap.TreeExplainer(model)

    # # Calcula os valores SHAP no mesmo X_processado que você treinou
    # shap_values = explainer.shap_values(X_processed)

    # shap_values_class1 = shap_values[1]  # impacto para classe Obeso = 1

    # plt.figure()
    # shap.summary_plot(
    #     shap_values_class1,  # valores SHAP para a classe obeso
    #     X_processed,          # dados após preprocessamento
    #     feature_names=preprocessor.get_feature_names_out()
    # )
    # plt.savefig("shap.png")


    # 6. Extrai vetor de importâncias das variáveis
    importances = model.feature_importances_

    # 8. Cria um DataFrame com nomes e importâncias
    df_dados = pd.DataFrame({
        "Variável": feature_names,
        "Importância": importances
    })

    # 9. Ordena da mais importante para a menos importante
    
    df_dados = df_dados.sort_values(by="Importância", ascending=False)

    # 10. Exibe os 10 primeiros (opcional)
    # print(importancia_df.head(10))

    # Imprime o cabeçalho de importanci_df
    # print(df_dados.head())

    # calculo da tendencia para cada importância
    dados = []
    for _, row in df_dados.iterrows():
        var_cat = row["Variável"]
        importancia = row["Importância"]

        # Captura o tipo (prefixo antes do primeiro __)
        if "__" in var_cat:
            tipo, resto = var_cat.split("__", 1)
        else:
            tipo = None
            resto = var_cat

        # Separa nome da variável e categoria pelo último underline
        if "_" in resto:
            var_name, categoria = resto.rsplit("_", 1)
        else:
            var_name = resto
            categoria = None

        dados.append({
            "Tipo": tipo,
            "Variável": var_name,
            "Categoria": categoria,
            "Importância": importancia
        })
        # print(f"Tipo: {tipo}, Variável: {var_name}, Categoria: {categoria}, Importância: {importancia}")

    df_dados =pd.DataFrame(dados)
    # print(df_dados.head())


    def calcula_tendencia_num(df, y, variavel):
        # calcula a média para obesos e não obesos
        media_obeso = df.loc[y == 1, variavel].mean()
        media_nao_obeso = df.loc[y == 0, variavel].mean()
        if media_obeso > media_nao_obeso:
            return "Obeso"
        else:
            return "Não Obeso"

    def calcula_tendencia_cat(df, y, variavel, categoria):
        # Total de obesos e não obesos
        total_obeso = (y == 1).sum()
        total_nao_obeso = (y == 0).sum()

        # Proporção da categoria em cada grupo
        prop_obeso = df.loc[y == 1, variavel].eq(categoria).sum() / total_obeso
        prop_nao_obeso = df.loc[y == 0, variavel].eq(categoria).sum() / total_nao_obeso

        return "Obeso" if prop_obeso > prop_nao_obeso else "Não Obeso"

    tendencias = []
    for _, row in df_dados.iterrows():
        tipo = row["Tipo"]
        variavel = row["Variável"]
        categoria = row["Categoria"]
        
        if tipo == "num":
            tendencia = calcula_tendencia_num(df, y, variavel)
        elif tipo == "cat":
            tendencia = calcula_tendencia_cat(df, y, variavel, categoria)
        else:
            tendencia = None  # segurança, mas não deve ocorrer

        tendencias.append(tendencia)

    df_dados["Tendência"] = tendencias

    # Cria uma nova coluna 'Importância Espelhada'
    df_dados["Importância Espelhada"] = df_dados.apply(
        lambda row: -row["Importância"] if row["Tendência"] == "Obeso" else row["Importância"],
        axis=1
    )
    df_dados["Categoria"] = df_dados.apply(
        lambda row: f"{row['Variável']} - {row['Categoria']}" if row["Tipo"] == "cat" else row["Variável"],
        axis=1
    )

    # Cria uma coluna de cor com base na tendência
    df_dados["Cor"] = df_dados["Tendência"].map({
        "Obeso": "goldenrod",       # amarelado
        "Não Obeso": "steelblue"    # azulado
    })
    # # Visualizar as primeiras linhas para conferir
    # print(df_dados.head(10))

    # Cria o gráfico
    fig = px.bar(
        df_dados,
        x="Importância Espelhada",
        y="Categoria",
        orientation="h",
        color="Tendência",
        color_discrete_map={
            "Obeso": "goldenrod",
            "Não Obeso": "steelblue"
        },
        # title="Importância das Variáveis por Tendência",
        height=800
    )

    # Inverte a ordem das variáveis para manter a mais importante no topo
    fig.update_layout(
        autosize=True,  # desabilita redimensionamento automático
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis=dict(autorange="reversed"),
        xaxis_title="Importância (Negativo = Obeso, Positivo = Não Obeso)"
    )

    return fig
