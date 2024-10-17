import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from itertools import product

# Função para carregar os dados
def carregar_dados():
    caminho_producao = r"C:\Users\lucas\Downloads\dados_producao.csv"
    df_producao = pd.read_csv(caminho_producao)

    # Transformar ano em datetime e verificar duplicatas
    df_producao['ano'] = pd.to_datetime(df_producao['ano'], format='%Y')
    
    # Remover duplicatas somando valores de 'total_litros' para o mesmo ano
    df_producao = df_producao.groupby('ano').agg({'total_litros': 'sum'}).reset_index()

    # Definir 'ano' como índice e garantir a frequência anual
    df_producao.set_index('ano', inplace=True)
    df_producao = df_producao.asfreq('YS')  # Definir a frequência anual
    
    return df_producao

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
    df['y_diff'] = df['total_litros'].diff().dropna()
    return df.dropna()

# Função para normalizar os dados
def normalizar_dados(df):
    scaler = MinMaxScaler()
    df[['y_diff']] = scaler.fit_transform(df[['y_diff']])
    return df, scaler

# Função para treinar o modelo ARIMA
def treinar_arima(df, order):
    modelo = ARIMA(df['y_diff'], order=order)
    modelo_fit = modelo.fit()  # Remover o solver que causava o erro
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
    df_producao = carregar_dados()

    # Testar estacionariedade antes e depois da diferenciação
    print("Antes da diferenciação:")
    testar_estacionariedade(df_producao['total_litros'])

    df_producao = diferenciar_serie(df_producao)

    print("\nApós a diferenciação:")
    testar_estacionariedade(df_producao['y_diff'])

    # Normalizar os dados
    df_producao, scaler = normalizar_dados(df_producao)

    # Plotar ACF e PACF
    plot_acf_pacf(df_producao)

    # Realizar grid search para ARIMA
    p_values = range(0, 4)
    d_values = range(0, 2)
    q_values = range(0, 4)

    grid_search_arima(df_producao, p_values, d_values, q_values)

if __name__ == "__main__":
    main()
