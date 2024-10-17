import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Função para carregar dados
def carregar_dados():
    caminho_producao = r"C:\Users\lucas\Downloads\dados_producao.csv"
    caminho_exportacao = r"C:\Users\lucas\Downloads\dados_exportacao.csv"

    dados_producao = pd.read_csv(caminho_producao)
    dados_exportacao = pd.read_csv(caminho_exportacao)

    print("Dados de Produção (Top 10):")
    print(dados_producao.head(10))
    print("\nDados de Exportação (Top 10):")
    print(dados_exportacao.head(10))

    return dados_producao, dados_exportacao

# Função para preparar os dados para o Prophet
def preparar_dados(df, tipo_dado):
    if tipo_dado == 'producao':
        df = df[['ano', 'total_litros']].rename(columns={'ano': 'ds', 'total_litros': 'y'})
    elif tipo_dado == 'exportacao':
        df = df[['ano', 'quantidade_kg']].rename(columns={'ano': 'ds', 'quantidade_kg': 'y'})
    
    # Filtrando valores muito pequenos
    df = df[df['y'] > 1e-2]
    return df

# Função para calcular o SMAPE (Symmetric Mean Absolute Percentage Error)
def calcular_smape(y_true, y_pred):
    denominator = (np.abs(y_true) + np.abs(y_pred)) / 2
    diff = np.abs(y_true - y_pred) / denominator
    smape = np.mean(diff) * 100
    return smape

# Função para calcular as métricas com SMAPE
def calcular_metricas(teste, previsoes):
    y_true = teste['y'].values
    y_pred = previsoes['yhat'][-len(teste):].values

    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))

    # Filtrar valores muito pequenos para evitar SMAPE distorcido
    mask = y_true > 1e-2
    y_true_filtered = y_true[mask]
    y_pred_filtered = y_pred[mask]

    if len(y_true_filtered) > 0:
        smape = calcular_smape(y_true_filtered, y_pred_filtered)
    else:
        smape = np.inf  # Se todos os valores forem muito pequenos, definir como infinito

    return mae, rmse, smape

# Função para treinar o modelo Prophet
def treinar_modelo(df):
    treino = df[:-10]  # Últimos 10 registros para teste
    teste = df[-10:]   # Teste nos últimos 10 registros

    modelo = Prophet(yearly_seasonality=False, changepoint_prior_scale=0.5)  # Ajuste de sensibilidade
    modelo.fit(treino)

    futuro = modelo.make_future_dataframe(periods=len(teste), freq='YE')
    previsoes = modelo.predict(futuro)

    return modelo, previsoes, treino, teste

# Função principal
def main():
    dados_producao, dados_exportacao = carregar_dados()

    # Preparar os dados para o Prophet
    df_producao = preparar_dados(dados_producao, 'producao')
    df_exportacao = preparar_dados(dados_exportacao, 'exportacao')

    # Treinar o modelo de produção
    modelo_producao, previsoes_producao, treino_producao, teste_producao = treinar_modelo(df_producao)

    # Calcular as métricas para o modelo de produção
    mae_producao, rmse_producao, smape_producao = calcular_metricas(teste_producao, previsoes_producao)
    print("\nMétricas de avaliação do modelo de Produção:")
    print(f"MAE: {mae_producao:.2f}")
    print(f"RMSE: {rmse_producao:.2f}")
    print(f"SMAPE: {smape_producao:.2f}%")

    # Treinar o modelo de exportação
    modelo_exportacao, previsoes_exportacao, treino_exportacao, teste_exportacao = treinar_modelo(df_exportacao)

    # Calcular as métricas para o modelo de exportação
    mae_exportacao, rmse_exportacao, smape_exportacao = calcular_metricas(teste_exportacao, previsoes_exportacao)
    print("\nMétricas de avaliação do modelo de Exportação:")
    print(f"MAE: {mae_exportacao:.2f}")
    print(f"RMSE: {rmse_exportacao:.2f}")
    print(f"SMAPE: {smape_exportacao:.2f}%")

if __name__ == "__main__":
    main()
