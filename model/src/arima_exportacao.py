import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from itertools import product

# Função para carregar os dados de exportação
def carregar_dados_exportacao():
    caminho_exportacao = r"C:\Users\lucas\Documents\GitHub\api-etl-pipeline\etl\output\dados_exportacao.csv"
    df_exportacao = pd.read_csv(caminho_exportacao)

    # Transformar 'ano' em datetime e verificar duplicatas
    df_exportacao['ano'] = pd.to_datetime(df_exportacao['ano'], format='%Y')
    
    # Remover duplicatas somando valores de 'quantidade_kg' para o mesmo ano
    df_exportacao = df_exportacao.groupby('ano').agg({'quantidade_kg': 'sum'}).reset_index()

    # Definir 'ano' como índice e garantir a frequência anual
    df_exportacao.set_index('ano', inplace=True)
    df_exportacao = df_exportacao.asfreq('YS')  # Definir a frequência anual
    
    return df_exportacao

# Testar se a série é estacionária com o ADF Test
def testar_estacionariedade(serie):
    resultado_adf = adfuller(serie)
    print(f"Estatística de Teste ADF: {resultado_adf[0]}")
    print(f"Valor-p: {resultado_adf[1]}")
    if resultado_adf[1] <= 0.05:
        print("A série é estacionária.")
    else:
        print("A série não é estacionária.")

# Função para diferenciar a série
def diferenciar_serie(df):
    df['y_diff'] = df['quantidade_kg'].diff().dropna()
    return df.dropna()

# Função para normalizar os dados
def normalizar_dados(df):
    scaler = MinMaxScaler()
    df[['y_diff']] = scaler.fit_transform(df[['y_diff']])
    return df, scaler

# Função para treinar o modelo ARIMA
def treinar_arima(df, order):
    modelo = ARIMA(df['y_diff'], order=order)
    modelo_fit = modelo.fit()
    previsoes = modelo_fit.forecast(steps=10)
    return modelo_fit, previsoes

# Calcular SMAPE
def calcular_smape(y_true, y_pred):
    return 100 / len(y_true) * np.sum(2 * np.abs(y_pred - y_true) / (np.abs(y_true) + np.abs(y_pred)))

# Função para realizar grid search
def grid_search_arima(df, p_values, d_values, q_values):
    best_mae, best_order, best_rmse, best_smape = float("inf"), None, float("inf"), None
    
    for order in product(p_values, d_values, q_values):
        try:
            modelo_fit, previsoes = treinar_arima(df, order)
            
            y_teste = df['y_diff'].tail(10).values  # Últimos 10 valores reais
            y_pred = previsoes[:len(y_teste)]
            
            mae = mean_absolute_error(y_teste, y_pred)
            rmse = np.sqrt(mean_squared_error(y_teste, y_pred))
            smape = calcular_smape(y_teste, y_pred)
            
            if mae < best_mae:
                best_mae, best_order, best_rmse, best_smape = mae, order, rmse, smape
                print(f"Melhor ordem atual {order} com MAE: {mae}, RMSE: {rmse}, SMAPE: {smape:.2f}%")
        
        except Exception as e:
            print(f"Erro ao ajustar o modelo ARIMA para ordem {order}: {e}")
    
    if best_order is None:
        print("Nenhum modelo foi ajustado com sucesso.")
    else:
        print(f"Melhores parâmetros encontrados: {best_order} com MAE: {best_mae}, RMSE: {best_rmse}, SMAPE: {best_smape:.2f}%")

# Função para plotar ACF e PACF
def plot_acf_pacf(df):
    plt.figure(figsize=(10, 5))
    plt.subplot(121)
    plot_acf(df['y_diff'], lags=20, ax=plt.gca())
    plt.title('ACF')
    
    plt.subplot(122)
    plot_pacf(df['y_diff'], lags=20, ax=plt.gca())
    plt.title('PACF')
    
    plt.tight_layout()
    plt.show()

# Função principal
def main():
    df_exportacao = carregar_dados_exportacao()

    # Testar estacionariedade antes e depois da diferenciação
    print("Antes da diferenciação:")
    testar_estacionariedade(df_exportacao['quantidade_kg'])

    df_exportacao = diferenciar_serie(df_exportacao)

    print("\nApós a diferenciação:")
    testar_estacionariedade(df_exportacao['y_diff'])

    # Normalizar os dados
    df_exportacao, scaler = normalizar_dados(df_exportacao)

    # Plotar ACF e PACF
    plot_acf_pacf(df_exportacao)

    # Realizar grid search para ARIMA
    p_values = range(0, 4)
    d_values = range(0, 2)
    q_values = range(0, 4)

    grid_search_arima(df_exportacao, p_values, d_values, q_values)

if __name__ == "__main__":
    main()
