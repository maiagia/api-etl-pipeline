import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import numpy as np

# Função para carregar os dados de exportação e produção
def carregar_dados():
    # Carregando os dados de produção e exportação
    dados_exportacao = pd.read_csv('etl/output/dados_exportacao.csv')
    dados_producao = pd.read_csv('etl/output/dados_producao.csv')

    # Conversão de datas (se houver) e adequação de colunas
    # Aqui, assumo que o dataset contém colunas com nomes como 'Ano', 'Produto', 'Quantidade (L.)'
    dados_producao['Ano'] = pd.to_datetime(dados_producao['Ano'], format='%Y')
    dados_exportacao['Ano'] = pd.to_datetime(dados_exportacao['Ano'], format='%Y')

    return dados_producao, dados_exportacao

# Função para preparar os dados de produção para o Prophet
def preparar_dados_producao(dados_producao):
    # Aqui, selecionamos as colunas de interesse para o modelo (Ano e Quantidade)
    df_producao = dados_producao[['Ano', 'Quantidade (L.)']].rename(columns={'Ano': 'ds', 'Quantidade (L.)': 'y'})

    return df_producao

# Função para preparar os dados de exportação para o Prophet
def preparar_dados_exportacao(dados_exportacao):
    # Selecionando as colunas de interesse para o modelo de exportação
    df_exportacao = dados_exportacao[['Ano', 'Quantidade(Kg)']].rename(columns={'Ano': 'ds', 'Quantidade(Kg)': 'y'})

    return df_exportacao

# Função para treinar o modelo Prophet
def treinar_modelo(df):
    # Divisão treino/teste (80% treino e 20% teste)
    treino = df.iloc[:-int(len(df)*0.2)]
    teste = df.iloc[-int(len(df)*0.2):]

    # Instanciando e treinando o modelo Prophet
    modelo = Prophet()
    modelo.fit(treino)

    # Previsão no conjunto de teste
    futuro = modelo.make_future_dataframe(periods=len(teste), freq='Y')  # Previsão anual
    previsoes = modelo.predict(futuro)

    # Retornando o modelo e previsões
    return modelo, previsoes, treino, teste

# Função para calcular as métricas de avaliação
def calcular_metricas(teste, previsoes):
    # Selecionando apenas os valores de interesse do período de teste
    y_true = teste['y'].values
    y_pred = previsoes['yhat'][-len(teste):].values

    # Cálculo das métricas
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = mean_absolute_percentage_error(y_true, y_pred)

    return mae, rmse, mape

# Função principal
def main():
    # Carregar os dados
    dados_producao, dados_exportacao = carregar_dados()

    # Preparar os dados de produção e exportação
    df_producao = preparar_dados_producao(dados_producao)
    df_exportacao = preparar_dados_exportacao(dados_exportacao)

    # Treinar o modelo para produção
    modelo_producao, previsoes_producao, treino_producao, teste_producao = treinar_modelo(df_producao)
    # Calcular as métricas para o modelo de produção
    mae_producao, rmse_producao, mape_producao = calcular_metricas(teste_producao, previsoes_producao)

    # Exibir as métricas do modelo de produção
    print("Métricas de avaliação do modelo de Produção:")
    print(f"MAE: {mae_producao}")
    print(f"RMSE: {rmse_producao}")
    print(f"MAPE: {mape_producao * 100:.2f}%")

    # Treinar o modelo para exportação
    modelo_exportacao, previsoes_exportacao, treino_exportacao, teste_exportacao = treinar_modelo(df_exportacao)
    # Calcular as métricas para o modelo de exportação
    mae_exportacao, rmse_exportacao, mape_exportacao = calcular_metricas(teste_exportacao, previsoes_exportacao)

    # Exibir as métricas do modelo de exportação
    print("\nMétricas de avaliação do modelo de Exportação:")
    print(f"MAE: {mae_exportacao}")
    print(f"RMSE: {rmse_exportacao}")
    print(f"MAPE: {mape_exportacao * 100:.2f}%")

if __name__ == "__main__":
    main()
